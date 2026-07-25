from app.schema.DocumentModel import DocumentModel
from app.tools.validate_documents import validate_document
from app.export.export_doc import export_docx
from pathlib import Path

from ..tools.img_verify import img_verifier
from ..ocr.easy_ocr import ocr_image
from ..schema.ImageState import Image_state
from ..schema.OCRstate import OCRblock,OCRresult

from ..db.db_functions import update_db
from langgraph.graph import END

from ..llm.client import client
from ..llm.prompts import reconstruction_prompt

### NODE FUNCTIONS ###

def chatbot_func(state:Image_state,llm_with_tools) -> Image_state:
    return {
            "messages":[llm_with_tools.invoke(state["messages"])]
           }

def validate_img(state:Image_state) -> Image_state:
    
    result = img_verifier(state['raw_file_path'])
    
    update_db(img_id=state['img_id'],valid_img=result['valid_img'])
    
    state['valid_img'] = result['valid_img']
    
    return state

def validation_to_ocr(state:Image_state) -> Image_state:
    
    if state['valid_img']:
        return "ocr"
    
    return END

def ocr_img(state:Image_state) -> Image_state:
    
    img_path = state['raw_file_path']
    
    result = ocr_image(image=img_path)
    
    temp_blocks = []
    
    for id,detection in enumerate(result):
        bbox,words,prob = detection
        
        block = OCRblock(id=id,
                         confidence_score=prob,
                         raw_text=words,
                         bbox=bbox)
        
        temp_blocks.append(block) # adds to the blocks list formated schema
    
    average_confidence = sum(block.confidence_score for block in temp_blocks)/len(temp_blocks)
    raw_text = "\n".join(block.raw_text for block in temp_blocks)
    
    llm_blocks = [{"text":blocks.raw_text,
               "confidence_score":blocks.confidence_score,
               "bbox":blocks.bbox} for blocks in temp_blocks]
    
    ocr_result = OCRresult(engine="easyocr",
                           average_confidence=average_confidence,
                           blocks=temp_blocks,
                           plain_text=raw_text)
    
    state['ocr_result'] = ocr_result
    state['llm_blocks'] = llm_blocks
    
    update_db(img_id=state['img_id'],ocr_result=ocr_result)
    
    return state

def validation_check(state:Image_state) -> Image_state:
    
    passes,errors = validate_document(document=state['document'],
                                      ocr=state['ocr_result'])
    
    state['validation_passed']=passes
    state['validation_error']=errors
    
    if not passes:
        state['retry_attempts'] += 1
    
    return state

def decide_on_validation(state:Image_state) -> Image_state:
    if state['validation_passed']:
        return 'export'
    elif state['retry_attempts']>=state['max_retry']:
        return "failed"
    else:
        return "retry"
    
def docx_export(state:Image_state)-> Image_state:
    
    output_path = Path("export")/f"{state['img_id']}.docx"

    state['final_file_path']=export_docx(document=state['document'],
                                         output_path=output_path)
    
    return state

def llm_reconstruct_format(state:Image_state) -> Image_state:
    structured_llm = client.with_structured_output(DocumentModel)
    chain = reconstruction_prompt| structured_llm
    structured_output = chain.invoke({"blocks":state['llm_blocks']})
    
    state['document'] = structured_output
    
    return state
    
    