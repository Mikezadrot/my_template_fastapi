from sqlmodel import SQLModel, Field
from datetime import datetime

class TokenSession(SQLModel, table=True):
    jti: str = Field(primary_key=True)
    user_id: int
    exp: datetime
