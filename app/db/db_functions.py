from sqlmodel import Field, Session, create_engine, SQLModel, select
from typing import Any

from app.db.db_engine import engine
from app.db.db_schema import Img_db_schema

def update_db(img_id:str,**update_param:Any) -> Img_db_schema:
    """
    Update one or more columns of the img_id in the db.

    Example:
        update_job(
            img_id,
            status="ocr_done",
            ocr_text=text
        )
    """
    with Session(engine) as session:
        img = session.exec(select(Img_db_schema).where(Img_db_schema.img_id==img_id)).first()
    
        if img is None:
            raise ValueError(f"Img id {img_id} not found in the database!")
        
        for param,value in update_param.items():
            
            if hasattr(img,param): # if img_id feteched schema has paramerter field update with the value provided
                setattr(img,param,value)
        
        session.add(img)
        session.commit()
        session.refresh(img)
    
        return img # returns the latest img_id updated row