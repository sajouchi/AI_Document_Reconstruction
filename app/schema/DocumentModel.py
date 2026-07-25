from typing import List, Literal, Optional

from pydantic import BaseModel
from enum import StrEnum

class DocumentType(StrEnum):
    PRINTED = "printed"
    HANDWRITTEN = "handwritten"

class type_format(StrEnum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    TABLE = "table"
    IMAGE = "image"
    UNKNOWN = "unknown"
    QUOTE = "quote"
    CODE = "code"
    BULLETED_LIST = "bulleted_list"
    NUMBERED_LIST = "numbered_list"

class DocumentElements(BaseModel):
    id:int
    type:type_format
    page_no:int
    text:str
    bbox:List[List[int]]
    confidence_score:float
    reading_order:int
    
class DocumentPage(BaseModel):
    page_no:int
    width:int
    height:int
    elements:List[DocumentElements]

class DocumentMetadata(BaseModel):
    document_type:Optional[DocumentType]
    language:str
    creator:str
    created_at:str

class DocumentModel(BaseModel):
    pages:List[DocumentPage]
    metadata:Optional[DocumentMetadata]
    

    