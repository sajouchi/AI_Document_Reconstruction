from pydantic import BaseModel

class ValidationResult(BaseModel):
    passed:bool
    errors:list