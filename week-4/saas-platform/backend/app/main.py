import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import Base, Project, User, engine, get_db

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer()
app = FastAPI(title="SaaS Platform API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
Instrumentator().instrument(app).expose(app)
Base.metadata.create_all(bind=engine)


class AuthIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class ProjectIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=5000)


class ProjectOut(ProjectIn):
    id: int
    owner_id: int


class ConnectionManager:
    def __init__(self):
        self.connections: set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.add(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.discard(ws)

    async def broadcast(self, message: dict):
        dead = []
        for ws in self.connections:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

manager = ConnectionManager()


def token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(hours=2)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def user_from_token(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        user = db.get(User, int(payload["sub"]))
    except (jwt.PyJWTError, KeyError, ValueError):
        user = None
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid authentication credentials")
    return user


@app.get("/health")
def health():
    return {"status": "ok", "service": "saas-platform-api"}


@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    db.execute(select(User).limit(1))
    return {"status": "ready"}


@app.post("/auth/register", status_code=201)
def register(data: AuthIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(409, "Email already registered")
    user = User(email=data.email, password_hash=pwd.hash(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token": token(user.id), "token_type": "bearer"}


@app.post("/auth/login")
def login(data: AuthIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not pwd.verify(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": token(user.id), "token_type": "bearer"}


@app.get("/projects", response_model=list[ProjectOut])
def projects(user: User = Depends(user_from_token), db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.owner_id == user.id).order_by(Project.id.desc()).all()


@app.post("/projects", response_model=ProjectOut, status_code=201)
async def create_project(data: ProjectIn, user: User = Depends(user_from_token), db: Session = Depends(get_db)):
    project = Project(**data.model_dump(), owner_id=user.id)
    db.add(project); db.commit(); db.refresh(project)
    await manager.broadcast({"event": "project.created", "project_id": project.id, "owner_id": user.id})
    return project


@app.get("/projects/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, user: User = Depends(user_from_token), db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project or project.owner_id != user.id:
        raise HTTPException(404, "Project not found")
    return project


@app.put("/projects/{project_id}", response_model=ProjectOut)
async def update_project(project_id: int, data: ProjectIn, user: User = Depends(user_from_token), db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project or project.owner_id != user.id:
        raise HTTPException(404, "Project not found")
    project.name, project.description = data.name, data.description
    db.commit(); db.refresh(project)
    await manager.broadcast({"event": "project.updated", "project_id": project.id, "owner_id": user.id})
    return project


@app.delete("/projects/{project_id}", status_code=204)
async def delete_project(project_id: int, user: User = Depends(user_from_token), db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project or project.owner_id != user.id:
        raise HTTPException(404, "Project not found")
    db.delete(project); db.commit()
    await manager.broadcast({"event": "project.deleted", "project_id": project_id, "owner_id": user.id})


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            message = await ws.receive_text()
            await ws.send_json({"type": "ack", "message": message})
    except WebSocketDisconnect:
        manager.disconnect(ws)
