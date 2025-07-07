from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import SessionLocal
from typing import List
from app.utils import get_current_user
from fastapi import BackgroundTasks
from app.tasks import log_blog_view

router = APIRouter(prefix="/blogs", tags=["Blogs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.BlogOut)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = models.Blog(**blog.dict(), owner_id=1)  # Simulate user ID
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/{id}", response_model=schemas.BlogOut)
def get_blog(id: int,
             background_tasks: BackgroundTasks,
             db: Session = Depends(get_db),
             current_user: models.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    background_tasks.add_task(log_blog_view,id,current_user)
    return blog




@router.get("/", response_model=List[schemas.BlogOut])
def get_all_blogs(db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs