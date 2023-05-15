from pydantic import BaseModel


class CredentialModel(BaseModel):
    login: str
    password: str


class UserModel(BaseModel):
    id_client: int
    login: str
    password: str
    telegramm_id: int

class RecordingModel(BaseModel):
    id_rec: int
    id_client: int
    id_time: int
    service: int
    extra_service_id: int

class ServiceModel(BaseModel):
    id_service: int
    name: str
    price: int

class Data(BaseModel):
  id_time: int
  data: str
  time: int


