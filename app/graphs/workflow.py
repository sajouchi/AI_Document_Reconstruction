from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver

from ..schema.ImageState import Image_state
from .nodes import (docx_export, validate_img,validation_to_ocr,ocr_img, 
                    validation_check, decide_on_validation,
                    llm_reconstruct_format)

from IPython.display import Image, display

workflow = StateGraph(state_schema=Image_state)

workflow.add_node("img_validator_node",validate_img)
workflow.add_node("ocr_node",ocr_img)
workflow.add_node('validation_check_node',validation_check)
workflow.add_node("export_node",docx_export)
workflow.add_node("llm_output_node",llm_reconstruct_format)

workflow.add_edge(START,"img_validator_node")
workflow.add_conditional_edges("img_validator_node",validation_to_ocr,{
                                                                        "ocr":"ocr_node",
                                                                        END:END                                              
                                                                      })
workflow.add_edge("ocr_node","llm_output_node")
workflow.add_edge("llm_output_node","validation_check_node")
workflow.add_conditional_edges("validation_check_node",decide_on_validation,{
                                                                "export":"export_node",
                                                                "retry":"ocr_node",
                                                                "failed":END
                                                               })

graph = workflow.compile()

### display the graph visually
def see_graph(graph):
    display(Image(graph.get_graph().draw_mermaid_png()))