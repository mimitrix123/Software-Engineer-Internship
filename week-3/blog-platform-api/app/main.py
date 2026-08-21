from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from .auth import create_token, current_user, hash_password, verify_password
from .database import Base, Comment, Like, Post, SessionLocal, User, engine, get_db
from .schemas import CommentCreate, CommentOut, PostCreate, PostOut, Token, UserCreate

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Blog Platform API", version="1.0.0", description="Week 3 internship mini-project")
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(or_(User.username == data.username, User.email == data.email)).first():
        raise HTTPException(409, "Username or email already registered")
    user = User(username=data.username, email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return Token(access_token=create_token(user.id))


@app.post("/auth/login", response_model=Token)
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return Token(access_token=create_token(user.id))


@app.get("/posts", response_model=list[PostOut])
def list_posts(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), search: str | None = Query(None, max_length=100), db: Session = Depends(get_db)):
    query = db.query(Post)
    if search:
        term = f"%{search}%"
        query = query.filter(or_(Post.title.ilike(term), Post.content.ilike(term)))
    return query.order_by(Post.id.desc()).offset((page - 1) * size).limit(size).all()


@app.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    post = Post(**data.model_dump(), author_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    return post


@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, data: PostCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != user.id:
        raise HTTPException(403, "Only the author can update this post")
    post.title, post.content = data.title, data.content
    db.commit()
    db.refresh(post)
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != user.id:
        raise HTTPException(403, "Only the author can delete this post")
    db.delete(post)
    db.commit()


@app.post("/posts/{post_id}/like")
def like_post(post_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not db.get(Post, post_id):
        raise HTTPException(404, "Post not found")
    if db.query(Like).filter_by(post_id=post_id, user_id=user.id).first():
        return {"liked": True, "message": "Already liked"}
    db.add(Like(post_id=post_id, user_id=user.id))
    db.commit()
    return {"liked": True}


@app.delete("/posts/{post_id}/like")
def unlike_post(post_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    like = db.query(Like).filter_by(post_id=post_id, user_id=user.id).first()
    if like:
        db.delete(like)
        db.commit()
    return {"liked": False}


@app.get("/posts/{post_id}/comments", response_model=list[CommentOut])
def list_comments(post_id: int, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    if not db.get(Post, post_id):
        raise HTTPException(404, "Post not found")
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.id.desc()).offset((page - 1) * size).limit(size).all()


@app.post("/posts/{post_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: int, data: CommentCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not db.get(Post, post_id):
        raise HTTPException(404, "Post not found")
    comment = Comment(content=data.content, author_id=user.id, post_id=post_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@app.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(404, "Comment not found")
    if comment.author_id != user.id:
        raise HTTPException(403, "Only the comment author can delete it")
    db.delete(comment)
    db.commit()
