from fastapi import Depends, HTTPException, status, Response,APIRouter
from typing import Optional, List
from .. import schemas, models,oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func


router=APIRouter()


@router.get("/posts",response_model=List[schemas.PostOut])
#@router.get("/posts")
def get_post(db:Session=Depends(get_db),get_current_user:
                 int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0, search: Optional[str]=""):
    #cursor.execute("select * from posts")
    #posts=cursor.fetchall()
    
    #   posts=db.query(models.Post).limit(limit)
    posts=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.name.contains(search)).limit(limit).offset(skip).all()
    
    
    
    return posts

@router.get("/posts/{id}",response_model=schemas.PostOut)
def get_one_post(id: int, db:Session=Depends(get_db),get_current_user:
                 int=Depends(oauth2.get_current_user)):
    #cursor.execute("select * from posts where id=%s",str(id))
    #post=cursor.fetchone()
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    print(post)
    #post=find_post(id)
    return post


@router.post("/createposts", response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db), get_current_user:
                 int=Depends(oauth2.get_current_user)):
    #cursor.execute(""" insert into posts(name,age,city) values(%s,%s,%s)RETURNING *""", (post.name,post.age,post.city))
    #new_post=cursor.fetchone()
    #print(**post.dict())
    print(get_current_user.id)
    new_post=models.Post(owner_id=get_current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #conn.commit()
    return new_post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),get_current_user:
                 int=Depends(oauth2.get_current_user)):
    print("This is",get_current_user)

    #cursor.execute("""DELETE FROM posts WHERE id= %s returning *""", (str(id)))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    

    post_query=db.query(models.Post).filter(models.Post.id==id)
    print(post_query)
    post=post_query.first()
    print(post)
    print(post.owner_id)
    print(type(post.owner_id))
    print(get_current_user.id)
    print(type(get_current_user.id))

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id!=int(get_current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

