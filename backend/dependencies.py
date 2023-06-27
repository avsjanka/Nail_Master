import hashlib
import os

import psycopg2
from psycopg2.extras import DictCursor
import jwt
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(user=os.environ.get("POSTGRES_USER") or 'postgres',
                                           password=os.environ.get("POSTGRES_PASSWORD") or 'postgresql' or 'postgres',
                                           host=os.environ.get("POSTGRES_HOST") or '127.0.0.1',
                                           port=5432,
                                           database=os.environ.get("POSTGRES_DB") or "Nails_DB",
                                           cursor_factory=DictCursor)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        try:
            create_table_client_query = '''CREATE TABLE IF NOT EXISTS  "Client" (
                                        "id_client" SERIAL PRIMARY KEY,
                                          "login" text UNIQUE,
                                          "telegramm_id" int,
                                          "role" text,
                                          "password" text
                                        );'''
            self.cursor.execute(create_table_client_query)

            create_table_recording_query = '''CREATE TABLE IF NOT EXISTS  "Recording" (
                                        "id_rec" SERIAL PRIMARY KEY,
                                            "id_client" int,
                                            "id_time" int,
                                            "service" int,
                                            "extra_service_id" int
                                        );'''
            self.cursor.execute(create_table_recording_query)

            create_table_service_query = '''CREATE TABLE IF NOT EXISTS  "Service" (
                                        "id_service" SERIAL PRIMARY KEY,
                                            "name_service" text UNIQUE,
                                            "price" int
                                        );'''
            self.cursor.execute(create_table_service_query)

            create_table_data_query = '''CREATE TABLE IF NOT EXISTS  "Data" (
                                        "id_time" SERIAL PRIMARY KEY,
                                          "data" text,
                                          "time" int
                                        );'''
            self.cursor.execute(create_table_data_query)

            create_table_extra_service_query = '''CREATE TABLE IF NOT EXISTS  "Extra_service" (
                                        "id_extra_service" SERIAL PRIMARY KEY,
                                          "name_service" text UNIQUE,
                                          "price" int,
                                          "time" int
                                        );'''
            self.cursor.execute(create_table_extra_service_query)

            create_table_extra_service_list_query = '''CREATE TABLE IF NOT EXISTS  "List_extra_services"(
                                        "id_extra_service" SERIAL PRIMARY KEY, 
                                        "list_extra_serrvice_id" int,
                                          "extra_service_id" int
                                        );'''
            self.cursor.execute(create_table_extra_service_list_query)

            create_table_dates_for_recordings_query = '''CREATE TABLE IF NOT EXISTS "Dates_for_recordings" (
                                          "id_time_rec" SERIAL PRIMARY KEY,
                                          "date_str" text,
                                          "time" int,
                                          "is_recorded" boolean
                                        );'''
            self.cursor.execute(create_table_dates_for_recordings_query)
            self.connection.commit()

        except:
            raise HTTPException(500)

    def execute(self, *args: object, **kwargs: object) -> object:
        try:
            self.cursor.execute(*args, **kwargs)
            return self.cursor
        except:
            raise HTTPException(500)



class Authentication:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database
        self.connection = database.connection

    def check_reg(self, username, password):
        try:
            with self.connection.cursor(cursor_factory = DictCursor) as is_registered:
                is_registered.execute('''
                    SELECT "id_client", "login", "password"
                    FROM "Client"
                    WHERE "login"=%s''', (username,))
                result = is_registered.fetchone()
                self.connection.commit()
                if (result.get('password') == password) :
                    return result
                else:
                    raise HTTPException(403)
        except Exception as e:
            raise HTTPException(403)

    def check_admin(self, username, password):
        try:
            with self.connection.cursor(cursor_factory = DictCursor) as is_registered:
                is_registered.execute('''
                    SELECT "id_client", "login", "password"
                    FROM "Client"
                    WHERE "login"=%s and "role" = %s''', (username,"administrator"))
                result = is_registered.fetchone()
                self.connection.commit()
                if (result.get('password') == password) :
                    return result
                else:
                    raise HTTPException(403)
        except Exception as e:
            raise HTTPException(403)

    def get_auth_token(self, username, user_id):
        try:
            key = os.environ.get("JWT_KEY") or "0db120c4bfd93e453dea115cd9079d709f452adee19e9600eedb0953d599e1b1"
            encoded = jwt.encode({"login": username, "id": user_id}, key, algorithm="HS256")
            return encoded
        except Exception as e:
            print(e)
            raise HTTPException(403)

    def verify_auth_token(self, token):
        try:
            key = os.environ.get("JWT_KEY") or "0db120c4bfd93e453dea115cd9079d709f452adee19e9600eedb0953d599e1b1"
            return jwt.decode(token, key, algorithms=["HS256"])
        except:
            raise HTTPException(403)


class JWTBearerAccess(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=True)

    async def __call__(self, request: Request, auth: Authentication = Depends(Authentication)) -> str:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(404, 'CredentialsNotFound')
        if not credentials.scheme == 'Bearer':
            raise HTTPException(404, 'SchemeTypeError')
        return auth.verify_auth_token(credentials.credentials)

