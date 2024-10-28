
import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ListenHistoryIn(BaseModel):
    user_id: Optional[int] = Field()
    items: Optional[List[int]] = Field()
    created_at: datetime.datetime = Field()
    updated_at: datetime.datetime = Field()
    # ingested_at: datetime.datetime = Field()
    # valid_until: Optional[datetime.datetime] = Field(None)

class UsersIn(BaseModel):
    id: int = Field()
    first_name: str = Field()
    last_name: str = Field()
    email: str = Field()
    gender: str = Field()
    favorite_genres: str = Field()
    created_at: datetime.datetime = Field()
    updated_at: datetime.datetime = Field()
    # ingested_at: datetime.datetime = Field()
    # valid_until: Optional[datetime.datetime] = Field(None)


class TracksIn(BaseModel):
    id: int = Field()
    name: str = Field()
    artist: str = Field()
    songwriters: str = Field()
    duration: str = Field()
    genres: str = Field()
    album: str = Field()
    created_at: datetime.datetime = Field()
    updated_at: datetime.datetime = Field()
    # ingested_at: datetime.datetime = Field()
    # valid_until: Optional[datetime.datetime] = Field(None)
