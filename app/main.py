
from fastapi import FastAPI,Response, status, HTTPException, Depends
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel,ValidationError
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas,utils
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from . routers import post,user, auth,vote
from .config import settings


models.Base.metadata.create_all(bind=engine)

app=FastAPI()
origins=["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()




try:
    conn=psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="Navita@21",cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Database connection successful")
except Exception as error:
    print("Connection to database failed")
    print("Error:",error)


#def find_post(id):
    #for p in posts:
       # if p['id'] == id;
           # return p




app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return{"message":"hello world!"}

@app.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts

