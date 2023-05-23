from pydantic import BaseModel


class CredentialModel(BaseModel):
    login: str
    password: str


class UserModel(BaseModel):
    id_client: int
    login: str
    telegramm_id: int = 0
    password: str

class AccessTokenModel(BaseModel):
    token: str

class RecordingModel(BaseModel):
    id_rec: int
    id_client: int
    id_time: int
    service: int
    extra_service_id: int

class NewRecordingModel(BaseModel):
    login: int
    time: str
    data: str
    service: int
    extra_service_ids: str

class ServiceModel(BaseModel):
    id_service: int
    name_service: str
    type: str
    price: int
    time: int

class Data(BaseModel):
  id_time: int
  data: str
  time: int


