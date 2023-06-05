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
     with database.connection.cursor(cursor_factory = DictCursor) as cursor:
         cursor.execute('''insert into "Data" 
                                    ("data", "time") 
                                    values (%s, %s)
                                    returning "id_time" as id_time, "data" as data, "time" as time''',
        (recording.data, recording.time))
         database.connection.commit()
         data = Data(**cursor.fetchone())
         data = data.id_time
         extra = recording.extra_service_ids.split(',')

     with database.connection.cursor(cursor_factory = DictCursor) as cursor:
         cursor.execute('''SELECT list_extra_service_id FROM "List_extra_services" ORDER BY list_extra_service_id DESC LIMIT 1''')
         result = cursor.fetchone()
         if result == None:
             list_extra_service_id = 1
         else:
             list_extra_service_id = result.get('list_extra_service_id')
             list_extra_service_id += 1
         database.connection.commit()
     for i in range( 0,len(extra)):
         with database.connection.cursor(cursor_factory = DictCursor) as cursor:
            cursor.execute('''insert into "List_extra_services"
                                        ("list_extra_service_id", "extra_service_id")
                                        values (%s,%s)
                                        returning "id_extra_service" as id_extra_service, "list_extra_service_id" as list_extra_service_id, "extra_service_id" as extra_service_id''',
            (list_extra_service_id,int(extra[i])))
            cursor.connection.commit()
     with database.connection.cursor(cursor_factory = DictCursor) as cursor:
          cursor.execute('''insert into ''')
          cursor.connection.commit()
     return recording

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

    elif old_service.time != service.time:
        database.execute('''update "Service" set time = %s where id_service = %s''',(service.time,old_service.id_service))
        database.connection.commit()

    cursor = database.execute('''SELECT * FROM "Service" where id_service = %s''',(service.id_service,))
    service = ServiceModel(**cursor.fetchone())
    return service

@router.post("/update_extra_service",response_model= ServiceModel)
async def update_extra_service(
    service: ServiceModel,
    database: Database = Depends(Database)
):
    cursor = database.execute('''SELECT * FROM "Extra_service" where id_extra_service = %s''',(service.id_service,))
    old_service = ServiceModel(**cursor.fetchone())
    if old_service.price != service.price:
        database.execute('''update "Extra_service" set price = %s where id_extra_service = %s''',(service.price,old_service.id_service))
        database.connection.commit()
    elif old_service.name_service != service.name_service:
        database.execute('''update "Extra_service" set name_service = %s where id_extra_service = %s''',(service.name_service,old_service.id_service))
        database.connection.commit()
    elif old_service.time != service.time:
        database.execute('''update "Extra_service" set time = %s where id_extra_service = %s''',(service.time,old_service.id_service))
        database.connection.commit()
    cursor = database.execute('''SELECT * FROM ""Extra_service" where id_extra_service = %s''',(service.id_service,))
    service = ServiceModel(**cursor.fetchone())
    return service


