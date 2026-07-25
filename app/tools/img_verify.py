from PIL import Image, UnidentifiedImageError
from langchain.tools import tool

# @tool
def img_verifier(img_path):
    """
    Checks if the images taken as an parameter is a valid image or not.
    """
    try:
        with Image.open(img_path)as img:
            img.verify()
        return {
            "valid_img":True
        }
    except (UnidentifiedImageError, Exception):
        return {
            "valid_img":False
        }