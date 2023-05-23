import hashlib
from typing import List
from io import BytesIO
import random
import string
import ctypes
import secrets

from psycopg2 import *
from dependencies import Database, Authentication, JWTBearerAccess
from models import CredentialModel, UserModel, RecordingModel, ServiceModel, NewRecordingModel, Data, AccessTokenModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/api")

@router.post("/register", response_model= UserModel)
async def register(
        creds: CredentialModel,
        database: Database = Depends(Database)
):
    cursor = database.execute('''insert into "Client" 
                                ("login", "password") 
                                values (%s, %s)
                                returning "id_client" as id_client, "login" as login, "password" as password''',
    (creds.login, str(hashlib.sha256(creds.password.encode()).hexdigest())))
    client_creds = UserModel(**cursor.fetchone())
    database.connection.commit()
    return client_creds


@router.post("/recording_client", response_model= RecordingModel)
async def create_recording(
        recording: NewRecordingModel,
        database: Database = Depends(Database)
):
     cursor = database.execute('''insert into "Data" 
                                ("data", "time") 
                                values (%s, %s)
                                returning "id_time" as id_time, "data" as data, "time" as time''',
    (recording.data, recording.time))
     data = Data(**cursor.fetchone())
     data = data.id_time
     extra = recording.extra_service_ids.split(',')
     database.connection.commit()
     return recording

@router.post("/login", response_model=AccessTokenModel)
async def login(
        creds: CredentialModel,
        auth: Authentication = Depends(Authentication)
):
    is_registered = auth.check_reg(creds.username, str(hashlib.sha256(creds.password.encode()).hexdigest()))
    if is_registered:
        return AccessTokenModel(token=auth.get_auth_token(is_registered[1], is_registered[0]))
    else:
        raise HTTPException(404, "User not found")



@router.get("/show_services", response_model = List[ServiceModel])
async def show_services(
         database: Database = Depends(Database)
):
    cursor = database.execute('''SELECT * FROM "Service"''')
    return [ServiceModel(id_service = element[0],
                         name_service = element[1],
                         type = element[2],
                         price = element[3],
                         time = element[4]) for element in cursor.fetchall()]


@router.post("/add_service",response_model= ServiceModel)
async def add_service(
    service: ServiceModel,
    database: Database = Depends(Database)
):
    cursor = database.execute('''insert into "Service" 
                                ("name_service", "type", "price", "time") 
                                values (%s, %s, %s, %s)
                                returning "id_service" as id_service,"name_service" as name_service, "type" as type, "price" as price, "time" as time''',
    (service.name_service, service.type, service.price, service.time))
    database.connection.commit()
    return service


@router.post("/add_extra_service",response_model= ServiceModel)
async def add_extra_service(
    service: ServiceModel,
    database: Database = Depends(Database)
):
    cursor = database.execute('''insert into "Extra_service" 
                                ("name_service", "type", "price", "time") 
                                values (%s, %s, %s, %s)
                                returning "id_service" as id_service,"name_service" as name_service, "type" as type, "price" as price, "time" as time''',
    (service.name_service, service.type, service.price, service.time))
    database.connection.commit()
    return service

@router.post("/delete_service",response_model= ServiceModel)
async def delete_service(
    service: ServiceModel,
    database: Database = Depends(Database)
):
    database.execute('''delete from "Service" where id_service = %s''', (service.id_service,))
    database.connection.commit()
    cursor = database.execute('''SELECT * FROM "Service"''')
    print(cursor.fetchall())
    database.connection.commit()
    return service

@router.post("/delete_extra_service",response_model= ServiceModel)
async def delete_extra_service(
    service: ServiceModel,
    database: Database = Depends(Database)
):
    database.execute('''delete from "Extra_service" where id_extra_service = %s''', (service.id_service,))
    database.connection.commit()
    cursor = database.execute('''SELECT * FROM "Extra_service"''')
    print(cursor.fetchall())
    database.connection.commit()
    return service

