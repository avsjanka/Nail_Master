import hashlib
from array import array
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extras import DictCursor
from dependencies import Database, Authentication
from models import CredentialModel, UserModel, RecordingModel, ServiceModel, NewRecordingModel, Data, AccessTokenModel

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


@router.post("/recording_client", response_model= NewRecordingModel)
async def create_recording(
        recording: NewRecordingModel,
        database: Database = Depends(Database)
):
    try:
         with database.connection.cursor(cursor_factory = DictCursor) as is_registered:
                is_registered.execute('''
                    SELECT "id_client", "login", "password"
                    FROM "Client"
                    WHERE "login"=%s''', (recording.login,))
                password = str(hashlib.sha256(recording.password.encode()).hexdigest())
                result = is_registered.fetchone()
                database.connection.commit()
                if (result.get('password') == password) :
                    id = result.get('id_client')
                    with database.connection.cursor(cursor_factory = DictCursor) as cursor:
                         cursor.execute('''insert into "Data" 
                                                    ("data", "time") 
                                                    values (%s, %s)
                                                    returning "id_time" as id_time, "data" as data, "time" as time''', (recording.data, recording.time))
                         data = cursor.fetchone()
                         database.connection.commit()
                         data = data.get('id_time')
                         print(data)
                         with database.connection.cursor(cursor_factory = DictCursor) as cursor:
                            cursor.execute('''insert into "Recording"
                                                        ("id_client","id_time","service")
                                                        values(%s,%s,%s) 
                                                        returning "id_rec" as id_rec,"id_client" as id_client,"id_time" as id_time,"service" as service''',(id,data,int(recording.service)))
                            cursor.connection.commit()
                            return recording
                else:
                    raise HTTPException(404, "User not found")

    except  Exception as e:
        print(e)
        raise HTTPException(404, "User not found")


@router.post("/login", response_model=AccessTokenModel)
async def login(
        creds: CredentialModel,
        auth: Authentication = Depends(Authentication)
):
    is_registered = auth.check_reg(creds.login, str(hashlib.sha256(creds.password.encode()).hexdigest()))
    if is_registered:
        return AccessTokenModel(token=auth.get_auth_token(is_registered[1], is_registered[0]))
    else:
        raise HTTPException(404, "User not found")

@router.post("/login_admin", response_model=AccessTokenModel)
async def login_admin(
        creds: CredentialModel,
        auth: Authentication = Depends(Authentication)
):
    is_registered = auth.check_admin(creds.login, str(hashlib.sha256(creds.password.encode()).hexdigest()))
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
                                ("name_service", "price") 
                                values (%s,  %s)
                                returning "id_service" as id_service,"name_service" as name_service, "price" as price''',
    (service.name_service, service.price))
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

@router.post("/update_service",response_model= ServiceModel)
async def update_service(
    service: ServiceModel,
    database: Database = Depends(Database)
):
    cursor = database.execute('''SELECT * FROM "Service" where id_service = %s''',(service.id_service,))
    old_service = ServiceModel(**cursor.fetchone())
    if old_service.price != service.price:
        database.execute('''update "Service" set price = %s where id_service = %s''',(service.price,old_service.id_service))
        database.connection.commit()

    elif old_service.name_service != service.name_service:
        database.execute('''update "Service" set name_service = %s where id_service = %s''',(service.name_service,old_service.id_service))
        database.connection.commit()

    cursor = database.execute('''SELECT * FROM "Service" where id_service = %s''',(service.id_service,))
    service = ServiceModel(**cursor.fetchone())
    return service


#@router.post("/show_recording",response_model = List[RecordingModel])
##):

