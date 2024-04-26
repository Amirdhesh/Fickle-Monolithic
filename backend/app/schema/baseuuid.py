from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class baseUUID(SQLModel):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column_kargs={"onupdate": datetime.now}
    )
