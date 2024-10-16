

CATEGORY_str1 = "3D_MeshTool/Array/"#

#---------------Basics class---------------
CATEGORY_str2 = "list"

class array_is_null:# 输入数组，输出是否为空, 开发中...
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{"array_input": ("LIST",),}}    
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("BOOL",) 
    RETURN_NAMES = ("IsNull",)
    FUNCTION = "array6"
    def array6(self,array_input):
        if not isinstance(array_input,list):return (True,)
        if array_input == []:return (True,)
        else:return (False,)