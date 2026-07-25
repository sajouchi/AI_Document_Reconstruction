from ..graphs.workflow import graph
from ..schema.ImageState import Image_state

def reconstructionInvoke(state:Image_state) -> Image_state:
    
    return graph.invoke(state)
