import easyocr

def ocr_image(image:str):
    reader = easyocr.Reader(['en']) # english 
    result = reader.readtext(image=image)
    
    return result
