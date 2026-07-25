from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from fastapi.concurrency import asynccontextmanager
import shutil

from typing import Annotated, Literal, Optional, Union
from sqlmodel import Session

import os

from app.db.init_db import create_db_and_tables
from app.db.db_engine import get_session
from app.db.db_schema import Img_db_schema,Img_db,upload_response,Response

from app.tools.helper_funtions import reconstructionInvoke

@asynccontextmanager
async def lifespan(app:FastAPI): # defualt things to initialize at app startup
    create_db_and_tables() # creates all the tables if not existed before
    yield

app = FastAPI(root_path="/doc_api/v1",lifespan=lifespan) # version-1 of this api
SessionDep = Annotated[Session,Depends(get_session)]

MAX_IMG_SIZE_BYTES = 10 * (1024 * 1024) # 5 MB, (1mb = 1024 * 1024 bytes)
MAX_IMG_MB = 10

@app.get("/health")
async def sever_live():
    return {"api_status": "live👌"} # check if the api is live

@app.post("/upload",status_code=201, response_model=Response[upload_response]) # for uploading the img
async def post_img(session:SessionDep,
                   document_type:Annotated[str,Form],
                   file:UploadFile = File(...)):
    
        img = await file.read()
        file.file.seek(0)
        
        saving_path = f"images/{file.filename}"

        if len(img) <= MAX_IMG_SIZE_BYTES: # saving images to the images folder
            try:
                with open(f"{saving_path}","wb") as f:
                    shutil.copyfileobj(file.file,f,length=MAX_IMG_MB)
            except Exception:
                raise HTTPException(status_code=500, detail="something went wrong!")
            finally:
                file.file.close()
        else:
            return {"error" : f" image size exceeds {MAX_IMG_MB} limit"}
        
        if os.path.exists(path=saving_path):
            
            db_img = Img_db(file_name=str(file.filename),
                        file_size=int(len(img)),
                        raw_file_path=saving_path,
                        document_type=document_type.lower())
            
            db_img = Img_db_schema.model_validate(db_img)
            session.add(db_img)
            session.commit()
            session.refresh(db_img)
            
            # invoking the graph
            initial_state = {
                            "img_id": db_img.img_id,
                            "file_name": db_img.file_name,
                            "raw_file_path": db_img.raw_file_path,
                            "file_size": db_img.file_size,

                            "document_type": db_img.document_type,

                            "valid_img": None,
                            "ocr_result": None,
                            "llm_blocks": [],
                            "document": None,

                            "validation_passed": False,
                            "validation_error": [],

                            "retry_attempts": 0,
                            "max_retry": 3,

                            "status": db_img.status,

                            "final_file_path": None,
                            "message": []
                            }
            
            result = reconstructionInvoke(state=initial_state)
            
        return {
                "data": {"file_name":f"{db_img.file_name}",
                        "file_size":db_img.file_size,
                        "document_type":document_type,
                        "status":f"{db_img.status}"}
                }
