from  fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router
from models import CredentialModel
from dependencies import Database

app = FastAPI()
app.include_router(router)
Database().create_tables()

origins = [
   "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#master pas *pEcg@wgkja#y4vZ
