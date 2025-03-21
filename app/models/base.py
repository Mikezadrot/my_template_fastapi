from sqlmodel import SQLModel
from datetime import datetime

class BaseModel(SQLModel):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
