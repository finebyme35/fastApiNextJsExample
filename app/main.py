from typing import Union
from django.http import JsonResponse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bson.objectid import ObjectId
from models import User,db,Users
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/user')
async def read_root():
    users = []
    for user in db.users.find():
        users.append(Users(**user))
    if users.__len__() <= 0:
        return "Kullanıcılar listelenirken bir hata oluştu."
    return users

@app.post('/user/detail/{id}')
async def read_root(id):
    if not id:
        return "Kullanıcı profili yüklenirken bir hata oluştu."
    user = []
    userFind = db.users.find_one({"_id": ObjectId(id)})
    user.append(Users(**userFind))
    return user


@app.post('/user/create')
async def create_user(user: User):
    if not user.name or not user.email:
        return "Kullanıcı eklerken bir hata oluştu."
    db.users.insert_one(user.dict())
    return {'user': user}


@app.post('/user/update')
async def update_user(user: User):
    if not user.id:
        return "Kullanıcı güncellenirken bir hata oluştu."
    db.users.update_one({'_id': user.id}, {'$set': {"name": user.name, "email": user.email}})
    return {'user': user}


@app.post('/user/delete/{id}')
async def delete_user(id):
    if not id:
        return "Kullanıcı silerken bir hata oluştu."
    query = {'_id': ObjectId(id)}
    db.users.delete_one(query)
    return "ok"
