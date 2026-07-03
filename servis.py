from fastapi import FastAPI,Body,Query, HTTPException,Depends
from sqlalchemy import Column,String,Integer,create_engine,ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from fastapi.responses import FileResponse, RedirectResponse,Response, PlainTextResponse
import sqlite3
import bcrypt
import webbrowser
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt
from jose.exceptions import*
import bcrypt
import os
#uvicorn servis:app --reload
app=FastAPI()
SECRET='arv@h2so4'
ALGORITHM='HS256'
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///silka.db')
engine = create_engine(DATABASE_URL)
ouath=OAuth2PasswordBearer('reglog')
class Base(DeclarativeBase):pass

class User(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True,index=True)
    name=Column(String)
    password=Column(String)
    links=relationship('Link', back_populates='user')

class Link(Base):
    __tablename__='link'
    id=Column(Integer, primary_key=True,index=True)
    name=Column(String)
    value=Column(String)
    user_id=Column(Integer, ForeignKey('users.id'))
    user=relationship('User', back_populates='links')

Base.metadata.create_all(bind=engine)
def create(username:str):
    payload={
        'sub':username,
        'exp':datetime.now()+timedelta(hours=1)
    }
    return jwt.encode(payload,SECRET,ALGORITHM)

def get(token:str=Depends(ouath)):
    try:
        data=jwt.decode(token,SECRET, algorithms=[ALGORITHM])
        return data.get('sub')
    except ExpiredSignatureError:
        raise HTTPException(401)
    except JWTError:
        raise HTTPException(401)
    
@app.get('/')
def root():
    return FileResponse('mainpage.html')

@app.post('/reglog')
def reglog(data=Body()):
    try:
        username=data['name']
        Session=sessionmaker(autoflush=False,bind=engine)
        with Session() as db:
            user=db.query(User).filter(User.name==username).first()
            if not user:
                print('start')
                salt=bcrypt.gensalt(rounds=12)
                pas=str(data['age']).encode('utf-8')
                pas=bcrypt.hashpw(pas, salt).decode('utf-8')
                print('gugugugu')
                dummy=User(name=username, password=pas)
                db.add(dummy)
                db.commit()
            else:
                print(type(user.password))
                print('startes')
                checked=str(data['age']).encode('utf-8')
                checking=user.password.encode('utf-8')
                check=bcrypt.checkpw(checked, checking)
                if not check:
                    raise HTTPException(401)
                print('ended')
            n=create(username)
            return {
                "status": "ok",
                "redirect_url": f"/account?token={n}"
            }
    except Exception as e:
        print(e)

@app.get('/account')
def account(token:str=Query(...)):
    try:
        data=jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        print(data)
        print(token)
        return FileResponse('account.html')
    except:
        return RedirectResponse('/')

@app.post('/add')
def add(token:str=Depends(get), data=Body()):
    try:
        Session=sessionmaker(autoflush=False, bind=engine)
        with Session() as db:
            user=db.query(User).filter(User.name==token).first()
            thing=Link(name=data['username'], value=data['deletename'])
            user.links.extend([thing])
            db.commit()
            print('Success!')
    except Exception as e:
        print(e)

@app.post('/del')
def list(token:str=Depends(get)):
    n=create(token)
    return {"status": "ok","redirect_url": f"/list?token={n}"}

@app.get('/list')
def sp(token:str=Query(...)):
    try:
        data=jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        name=data.get('sub')
        text='Список:\n'
        Session=sessionmaker(autoflush=False,bind=engine)
        with Session() as db:
            user=db.query(User).filter(User.name==name).first()
            for i in user.links:
                text+=f'{i.name} - {i.value} \n'
            return PlainTextResponse(content=text)
    except Exception as e:
        print(e)

@app.post('/sending')
def val(token:str=Depends(get),value=Body()):
    try:
        naming=value['url']
        print(naming)
        Session=sessionmaker(autoflush=False, bind=engine)
        print('started')
        with Session() as db:
            link=db.query(Link).filter(Link.name==naming).first()
            if not link:
                raise HTTPException(404, "Link not found")
        return {'status':'ok', 'redirect_url':link.value}
    except Exception as e:
        print(e) 