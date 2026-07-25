from enum import StrEnum

from typing import Annotated, List, TypedDict,Literal,Optional
from langgraph.graph.message import add_messages

from app.schema import DocumentModel
from app.schema.OCRstate import OCRresult, blocks_data_for_llm

class Status(StrEnum):
    uploaded = "uploaded"
    processing = "processing"
    completed = "completed"

class DocumentType(StrEnum):
    PRINTED = "printed"
    HANDWRITTEN = "handwritten"

class Image_state(TypedDict):
    
    img_id:str # uuid in the db
    
    file_name:str
    raw_file_path:str
    file_size:str
    final_file_path:Optional[str]
    
    valid_img:Optional[bool]
    ocr_result:Optional[OCRresult]
    llm_blocks:List[blocks_data_for_llm]
    document:Optional[DocumentModel] # type: ignore
     
    document_type: Optional[DocumentType]
    
    validation_passed:bool
    validation_error:list
    
    retry_attempts:int = 0
    max_retry:int = 3
    
    docx_path:Optional[str] = None
    pdf_path:Optional[str] = None
    
    status:Optional[Status]
    
    message:Annotated[list,add_messages]
    
    