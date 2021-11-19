""" from flask import Flask, json,jsonify,request """
from s3bucket import S3Bucket
import os
from pydantic import BaseModel
from passlib.hash import pbkdf2_sha256
from db import get_database
from starlette.routing import request_response
from starlette.responses import JSONResponse
from json import decoder
from fastapi.responses import HTMLResponse
from typing import List

from typing import BinaryIO, Optional
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Body, File, Form, Header
from flask.json import dumps, jsonify
import jwt
from datetime import datetime
import json
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi import FastAPI, Header, Response, status, Request, UploadFile
from pydantic.errors import DateTimeError
from pydantic.types import FilePath, Json
from pymongo.read_preferences import _MODES
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, Security
import boto3
from botocore.exceptions import NoCredentialsError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
security = HTTPBearer()
# from starlette.responses import JSONResponse, Response
users = []
""" from flask_cors import CORS """
""" app = Flask(__name__)
CORS(app) """
global files
global var
var = False
origins = [
    "*"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    Name_with_Initials:str
    email: str
    firstname: str
    lastname: str
    password: str
    business_name: str
    business_type: str
    business_address: str


@app.post('/signup')
def signup(item: Item):
    try:
        users = get_database()["users"]

        user_details = item
        print(user_details)
        email = user_details.email

        password = user_details.password
        user_details.password = pbkdf2_sha256.encrypt(password)
        print(json.dumps(user_details.__dict__))

        if users.find_one({'email': email}):
            print("hi")
            return {"status": "error", "message": "Email address already in use"}, 400
        else:
            print("hi")

            ss = json.dumps(user_details.__dict__)
            print(ss)
            print(user_details)
            print(type(json.loads(ss)))
            data = json.loads(ss)
            print(data)
            user = users.insert_one(data)

            exp_time = int(time.time()) + 600000
            print(exp_time)
            token = jwt.encode({"firstname": user_details.firstname,"lastname": user_details.lastname,"Name_with_Initials":user_details.Name_with_Initials,
                               "email": email, "exp": exp_time}, "secret", algorithm="HS256")
            return {"status": "ok", "message": "successful", "accessToken": token, "user": user_details}
    except Exception as e:
        return e
    # if len(users)!=0:
    #     for user in users:
    #         if user["email"] == email:
    #             return {"status":"error","message":"user exist"},400

    # users.append(user_details)


class data_login(BaseModel):
    email: str
    password: str


@app.post('/api/login')
def login(value: data_login):
    print("")
    try:
        print(type(value))
        user = {}
        users = get_database()["users"]
        request_data = value
        print(request_data)
        email = request_data.email
        password = request_data.password
        print(password)

        if users.find_one({"email": email}):
            user = users.find_one({"email": email})
            print(user)
            print(type(user))

        else:
            return {"status": "ok", "message": "user does not exist, please do register"}, 404

        if pbkdf2_sha256.verify(password, user['password']):
            print(user['password'])
            exp_time = int(time.time()) + 600000000
            print(exp_time)
            token = jwt.encode({"firstname": user["firstname"], "lastname": user["lastname"],
                               "email": email, "exp": exp_time}, "secret", algorithm="HS256")

            response = {"status": "ok",
                        "message": "Logged in", "accessToken": token}
            print(response)
            return response
        else:
            return {"status": "error", "message": "login failed, invalid Credentials"}, 401
        # for user in users:
        #     if user["email"] == email:

        #         else:
        #             return {"status": "error","message": "Login failed"}
        # return {"status": "error","message": "user not found"}, 404
    except Exception as e:
        return {"status": "error", "message": e}, 400

@app.post('/auth/user')
async def user(request: Request):
    try:
        token = request.headers['authorization']
        print(token)
        print("valid token")
        print(token)
        user = jwt.decode(token, 'secret', algorithms="HS256")
        print(user)
        if var == False:
            return JSONResponse(status_code=200, content={"status": "OK", "user": user,"var":False})
        else:
            return JSONResponse(status_code=200, content={"status": "OK", "user": user,"var":True})
    except jwt.ExpiredSignatureError:
        return {"status": "error", "message": "Token expired. Get new one"}, 401
    except jwt.InvalidTokenError:
        return {"status": "error", "message": "Access Token Invalid"}, 403
    except Exception as e:
        return e


@app.post('/file/user')
async def user(user_name:str=Form(...), file:List[UploadFile]=File(...)):
    try:
        print(type(file[0]))
        
        print(user_name)
        files = [f.filename for f in file]
        print(files)
        values = []
        bucket = S3Bucket(user_name.replace(" ","_"))
        try:
            for f in file:
                print(f)
                content = await f.read()
                file_path = f.filename.replace(' ', '')
                print(f'file_path: {file_path}')
                with open(file_path, 'wb') as buffer:
                    buffer.write(content)
                    url = bucket.get_s3_url(file_path)
                    values.append(url)
                    print(url)
                bucket.remove_image()
            
        except Exception as e:
            print(e)
        
        # print(type(file[0]))
        # values =[]
        # filess = {"filenames": [file.filename for file in file]}
        # value =filess['filenames']
        # print(value)
         
        # bucket = S3Bucket("sushmithasherigar1998@gmail.com")
        # uploads_dir = os.path.join(os.getcwd(), 'uploads')
        # files = get_database()["files"]
        # for val in value:
        #     print(val)
        #     upload_file = os.path.join(os.getcwd(), val)
        #     url = bucket.get_s3_url(val)
        #     print(url)
        #     values.append(url)
        # filess = file.filename
        # print(filess)
        
        # value = filess.split(".")
        # filename = value[0] + \
        #     '_{}.'.format(datetime.now().strftime('%d%m%y-%H%M%S'))+value[1]
        # print(
        #     value[0]+'_{}.'.format(datetime.now().strftime('%d%m%y-%H%M%S'))+value[1])
        
        # print("upload file")
        # print(upload_file)
        # files.insert_one(
        #     {"filePath": upload_file, 'fileName': filename}).inserted_id
        # try:
        #     with open(upload_file, "wb+") as file_object:
        #         file_object.write(file.file.read())
        #     bucket = S3Bucket("sushmithasherigar1998@gmail.com")
        #     url = bucket.get_s3_url(upload_file)
        #     print(url)
        
        return JSONResponse(status_code=200, content={"status": "OK",  "url":values})
            
       
            

        

    except jwt.ExpiredSignatureError:
        return {"status": "error", "message": "Token expired. Get new one"}, 401
    except jwt.InvalidTokenError:
        return {"status": "error", "message": "Access Token Invalid"}, 403
    except Exception as e:
        return e

if __name__ == '__main__':
    app.run(debug=True)
