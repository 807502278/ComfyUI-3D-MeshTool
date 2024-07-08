"""
@author: 807502278
@title: 3D Mesh Tool
@nickname: 3D Mesh Tool
@description: A simple 3D model processing tool within ComfyUI
"""

import numpy as np

CATEGORY_str1 = "3D_MeshTool/" 

#---------------show class---------------
CATEGORY_str2 = "show"

class AnyType(str):
  """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""
  def __ne__(self, __value: object) -> bool:
    return False
any = AnyType("*")

class show_any:#未完成
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                    "Any":(any,{}),
                    "format":("BOOLEAN",{"default":True}),
                    },
                "optional": {
                    "Any": (any,),
                    }
               }
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("to_str",)
    OUTPUT_NODE = True
    FUNCTION = "show_any"
    def show_any(self,Any,format):
        Any_data=[];text="";n=""
        if type(Any_data) == tuple:Any_data=Any[0]
        else:Any_data=Any
        if format:n="\n"
        if isinstance(Any_data, np.ndarray):Any_data=Any_data.tolist()
        if type(Any_data) == list:
            for item in Any_data:
                try:
                    text += str(item) + n
                except Exception:
                    text += "source exists, but could not be serialized.\n"
        elif type(Any_data) == dict:
            for key, value in Any_data.items():
                try:
                    text += str(key) + ": " + str(value) + n
                except Exception:
                    text += "source exists, but could not be serialized.\n"
        elif type(Any_data) != str:
            text = str(Any_data)
        text1=text.replace("\n","")
        return {"ui": {"text": [text]}, "result": (text,)}

NODE_CLASS_MAPPINGS = {
    #"show_any": show_any,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    #"show_any": "Show Any",
}