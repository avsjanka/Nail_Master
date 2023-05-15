import hashlib
from typing import List
from io import BytesIO
import random
import string
import ctypes
import secrets

from models import CredentialModel, UserModel, RecordingModel, ServiceModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/api")

@router.post("/register", response_model= CredentialModel)
async def register(
        creds: CredentialModel,
        #database: Database = Depends(Database)
):
    client_creds = creds
    return client_creds


@router.post("/recording_client", response_model=RecordingModel)
async def create_recording(
        recording: RecordingModel,
        #database: Database = Depends(Database)
):

    return recording


@router.post("/add_service",response_model= ServiceModel)
async def add_service(
    service: ServiceModel,
):
    return service
