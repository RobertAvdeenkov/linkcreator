from fastapi import FastAPI, Cookie, Query, Body,Depends, HTTPException
from fastapi.responses import Response, FileResponse, RedirectResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import sqlite3
from sqlalchemy import Column,String,create_engine,ForeignKey, Integer
from sqlalchemy.orm import sessionmaker,DeclarativeBase,relationship
import webbrowser
from datetime import datetime,timedelta
import bcrypt
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import*
#uvicorn chern:app --reload
#uvicorn chern:app --reload
app = FastAPI()
ALGORITHM = "HS256"
SECRET='arv@h2so4'
engine=create_engine('sqlite:///todo.db')
class Base(DeclarativeBase):pass
ouath2=OAuth2PasswordBearer(tokenUrl='reglog')
class Thing(Base):
    __tablename__='things'
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    user_id=Column(Integer, ForeignKey('users.id'))
    user=relationship('User', back_populates='things')

class User(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    password=Column(String)
    role=Column(String, default='user')
    things=relationship('Thing', back_populates='user')

Base.metadata.create_all(bind=engine)
def create_token(username:str):
    payload={
        'sub':username,
        'exp':datetime.now()+timedelta(hours=1)
    }
    token=jwt.encode(payload, SECRET, ALGORITHM)
    return token

def get_user(token:str=Depends(ouath2)):
    try:
        data = jwt.decode(token, SECRET,algorithms=[ALGORITHM])
        return data.get('sub')
    except ExpiredSignatureError:
        raise HTTPException(401)
    except JWTError:
        raise HTTPException(401)

@app.get('/')
def root():
    return FileResponse('C:\\Users\\r8033\\OneDrive\\Desktop\\nexa\\setevoe\\mainpage.html')

@app.post('/reglog')
def reglog(data=Body()):
    if not data['name']:
        return HTTPException(401)
    n=create_token(data['name'])
    Session=sessionmaker(autoflush=False, bind=engine)
    with Session() as db:
        user=db.query(User).filter(User.name==data['name']).first()
        print(data['age'])
        if user == None or user is None:
            db.add(User(name=data['name'], password=data['age']))
            db.commit()
        elif user.password!=data['age']:
            raise HTTPException(401)
        return {
        "status": "ok",
        "redirect_url": f"/account?token={n}"
        }
@app.get('/account')
def account(token:str=Query(...)):
    try:
        data=jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        username=data.get('sub')
        return FileResponse('C:\\Users\\r8033\\OneDrive\\Desktop\\nexa\\setevoe\\account.html')
    except:
        raise HTTPException(401)
        
@app.post('/add')
def add(username:str=Depends(get_user), data=Body()):
    Session=sessionmaker(autoflush=False,bind=engine)
    name_task=data.get('name')
    with Session() as db:
        user=db.query(User).filter(User.name==username).first()
        thing=Thing(name=name_task)
        user.things.extend([thing])
        db.commit()

@app.get('/list')
def list(username:str=Depends(get_user)):
    Session=sessionmaker(autoflush=False,bind=engine)
    text='Ваш список задач:\n'
    with Session() as db:
        user=db.query(User).filter(User.name==username).first()
        for index,i in enumerate(user.things):
            text+=f'{index}. '+str(i.name)+'\n'
    return Response(content=text, media_type='text/plain')

    