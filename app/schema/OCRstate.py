from pydantic import BaseModel
from typing import List

class blocks_data_for_llm(BaseModel):
    text:str
    confidence_score:float
    bbox:List[List[float]]

class OCRblock(BaseModel):
    id:int
    confidence_score:float
    raw_text:str
    bbox:List[List[float]]

class OCRresult(BaseModel):
    engine:str # OCR model used
    average_confidence:float
    page_count:int = None
    blocks: List[OCRblock]
    plain_text:str
    # blocks_data_for_llm:List[blocks_data_for_llm]
    