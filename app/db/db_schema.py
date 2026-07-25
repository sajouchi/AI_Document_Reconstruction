from pydantic import BaseModel
from sqlmodel import SQLModel,Field
from typing import Generic, Optional, Literal, TypeVar, Union
from datetime import datetime, timezone

from enum import Enum, StrEnum
from uuid import uuid4

from app.schema.DocumentModel import DocumentModel
from app.schema.OCRstate import OCRresult

class Status(StrEnum):
    uploaded = "uploaded"
    processing = "processing"
    completed = "completed"

class DocumentType(StrEnum):
    PRINTED = "printed"
    HANDWRITTEN = "handwritten"

class Img_db_schema(SQLModel,table=True): # after uploading image this schema is used before processing is finished
    img_id:str = Field(default_factory=lambda: str(uuid4()),primary_key=True)
    file_name:str
    
    raw_file_path:str = None
    final_file_path:Optional[str] = Field(default=None,nullable=True)
    status:Status = Field(default_factory=Status.uploaded)
    
    document_type:Optional[DocumentType]
    valid_img:Optional[bool] = None

    # ocr_result:Optional[OCRresult] = Field(default=None)
    # document:Optional[DocumentModel] = Field(default=None)# type: ignore
    docx_path:Optional[str] = None
    pdf_path:Optional[str] = None

    uploaded_at:datetime = Field(default_factory=lambda:datetime.now(timezone.utc), nullable=True, index=True)
    file_size:int # bytes/mb

class Img_db(SQLModel): # schema (not a table) used to update into the main db
    file_name:str
    file_size:int # bytes/mb
    raw_file_path:str
    document_type:Optional[DocumentType]
    status:Status = Field(default=Status.uploaded)
    
class upload_response(SQLModel):
    file_name:str
    file_size:int
    document_type:Optional[DocumentType]
    status:Status = Field(default=Status.uploaded)

T = TypeVar("T")
class Response(BaseModel, Generic[T]): # output schema template to define any expected type for all responses
    data:T
