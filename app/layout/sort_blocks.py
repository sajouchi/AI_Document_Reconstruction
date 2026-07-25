from typing import List
from app.schema.OCRstate import OCRblock

def sort_blocks(blocks:list[OCRblock]) -> OCRblock:
    """
    Sort OCR blocks in reading order.

    Priority:
        1. Top to bottom (y)
        2. Left to right (x)
    """
    blocks = sorted(blocks,
                    key=lambda block:(block.bbox[0][1],
                                      block.bbox[0][0])) # sorted(block,key=(y,x))
    
    return blocks
