import numpy as np
import ast
import re
from ..moduel.str_edit import strtolist

CATEGORY_str1 = "3D_MeshTool/Array/"#

#---------------Basics class---------------
CATEGORY_str2 = "Basics"

class array_step:#输入初始值、步长、增量生成等差数列
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required":
                    {
                    "start": ("FLOAT", {"default": 0.0,"min": -99999.0,"max": 99999.0,"step": 0.5}),
                    "step": ("INT", {"default": 3,"min": 1,"max": 99999,"step": 1}),
                    "increment": ("FLOAT", {"default": 4.0,"min": -99999.0,"max": 99999.0,"step": 0.5}),
                    }
                }
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("array",)
    FUNCTION = "array1"
    def array1(self,start,step,increment):
        a1 = [start,]
        if step <= 1:
            return (a1,)
        else:
            i=1
            while i <= step-1:a1.append(start+i*increment);i+=1
            return (a1,)

class array_end_increment:#输入初始值、终值、增量生成等差数列
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required":
                    {
                    "start": ("FLOAT", {"default": 0.0,"min": -99999.0,"max": 99999.0,"step": 0.5}),
                    "end": ("FLOAT", {"default": 3.0,"min": 1.0,"max": 99999.0,"step": 0.5}),
                    "increment": ("FLOAT", {"default":0.5,"min": -99999.0,"max": 99999.0,"step": 0.5}),
                    }
                }    
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("LIST",) 
    RETURN_NAMES = ("array",)
    FUNCTION = "array2"
    def array2(self,start,end,increment):
        array1 = [start,]
        if increment  >= end-start or increment == 0 or start==end:
            return (array1,)
        else:
            i=1;k=int((end-start)/increment)
            while i <= k:array1.append(start+i*increment);i+=1
            return (array1,)

class array_end_step:#输入初始值、步长、终值生成等差数列
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required":
                    {
                    "start": ("FLOAT", {"default": 0.0,"min": -999999.0,"max": 999999.0,"step": 0.5}),
                    "step": ("INT", {"default": 3,"min": 1,"max": 999999,"step": 1}),
                    "end": ("FLOAT", {"default":0.5,"min": -999999.0,"max": 999999.0,"step": 0.5}),
                    }
                }    
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("array",)
    FUNCTION = "array3"
    def array3(self,start,step,end):
        array1 = [start,];i=1
        if step <= 1:
            return (array1,)
        elif start == end:
            while i < step:array1.append(start);i+=1
            return (array1,)
        else:
            k=(end-start)/(step-1)
            while i < step:array1.append(start+k*i);i+=1
            return (array1,)

class array_step_increment:#输入初始值、步长、增量生成等差数列
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required":
                    {
                    "start": ("FLOAT", {"default": 0.0,"min": -99999.0,"max": 99999.0,"step": 0.5}),
                    "step": ("INT", {"default": 3,"min": 1,"max": 99999,"step": 1}),
                    "increment": ("FLOAT", {"default": 4.0,"min": -99999.0,"max": 99999.0,"step": 0.5}),
                    }
                }
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("array",)
    FUNCTION = "array9"
    def array9(self,start,step,increment):
        a1 = [start,];i=1
        if step <= 1:
            return (a1,)
        elif increment == 0:
            while i < step:a1.append(start);i+=1
            return (a1,)
        else:
            while i < step:a1.append(start+i*increment);i+=1
            return (a1,)

class string_to_array:#输入字符串，输出字符串中每个字符组成的数组,(开发中)
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required":
                    {"string_input": ("STRING", {"default":"","multiline": True,}),
                    "arrangement":("BOOLEAN",{"default":True,})
                    }
                }
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("array",)
    FUNCTION = "string_to_array1"
    def string_to_array1(self,string_input,arrangement):
        string_input = re.sub(r'\s+|\"', '', string_input)
        if string_input == "":
            return ([],)
        if arrangement:
            string_input = strtolist.convert_list(string_input)
        if string_input[0] != "[":
            string_input = "[" + string_input + "]"
            return (ast.literal_eval(string_input),)
        else:
            return (ast.literal_eval(string_input),)


#---------------calculation class---------------
CATEGORY_str3 = "calculation"

class array_t:#输入数组，输出转置数组
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required":
                    {
                        "array_input": ("LIST", {"default": []}),
                    }
                }    
    CATEGORY = CATEGORY_str1+CATEGORY_str3
    RETURN_TYPES = ("LIST",) 
    RETURN_NAMES = ("array_output",)
    FUNCTION = "array4"
    def array4(self,array_input):
        if array_input == []:
            return ([],)
        array_input=np.array(array_input)
        if array_input.ndim == 1:
            array_input = np.array([array_input[i:i+1] for i in range(len(array_input))])
        else:
            array_input = np.transpose(np.array(array_input))
        return (array_input.tolist(),)

class array_number_to_angle:#将数组中每个元素转换成对应的角度
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required": 
                    {
                    "array":("LIST",),
                    "half_angle":("BOOLEAN",{"default":True,"label_on": "180°", "label_off": "360°"}),
                    }
                }
    CATEGORY = CATEGORY_str1+CATEGORY_str3
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("array_angle",)
    FUNCTION = "data_to_angle"
    def data_to_angle(self,array,half_angle):
        array = np.array(array)
        #half_angle=True
        array %= 360
        if half_angle:
            for i in np.nditer(array,op_flags=['readwrite']):
                if i > 180:i[...]=i-360
            return (array.tolist(),)
        else:
            return (array.tolist(),)

class array_append:#输入数组(1维或2维)、判断附加1或2维数组，输出合并后的数组、原数组剩余、附加数组剩余
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required":
                    {
                        "array_input": ("LIST", {"default": []}),
                        "append_input": ("LIST", {"default": []}),
                    }
                }    
    CATEGORY = CATEGORY_str1+CATEGORY_str3
    RETURN_TYPES = ("LIST","LIST","LIST",) 
    RETURN_NAMES = ("array_append","array_input_surplus","array_append_surplus")
    FUNCTION = "array5"
    def array5(self,array_input,append_input):
        array_input2 = append_input2 = output = list()
        if array_input == []:
            return (append_input,[],append_input)
        if append_input == []:
            return (array_input,array_input,[])
        array_input=np.array(array_input);append_input=np.array(append_input)#转换为numpy数组
        if array_input.ndim == 1 and append_input.ndim == 1:
            array_input=np.append(array_input,append_input)#原数组和附加的数组都为一维,直接合并
            return (array_input.tolist(),[0,],[0,])
        if array_input.ndim == 1 and append_input.ndim == 2:
            array_input=np.vstack(array_input)#若原数组为一维附加的数组为二维，则将原数组转为二维
        if append_input.ndim == 1 and array_input.ndim == 2:
            append_input=np.vstack(append_input)#若附加的数组为一维原数组为二维，则将附加的数组转为二维
        if array_input.ndim >=3 or append_input.ndim >=3:#若任意数组维数大于等于3，则报错
            print("Error:(E-5-1)The input is not a one-dimensional or two-dimensional array")
            return ([],)
        else:
            intput_len=len(array_input);append_len=len(append_input)
            if intput_len > append_len:#若原数组长度大于附加的数组长度，则截断
                #print(f"{array_input}\nto")#测试用
                array_input2=array_input[append_len:].tolist()#截断后的原数组
                array_input=array_input[:append_len]
                #print(f"{array_input}\n+\n{array_input2}")#测试用
            elif append_len > intput_len:#若附加的数组长度大于原数组长度，则截断
                #print(f"{append_input}\nto")#测试用
                append_input2=append_input[intput_len:].tolist()#截断后的附加的数组
                append_input=append_input[:intput_len]
                #print(f"{append_input}\n+\n{append_input2}")#测试用
            output=np.hstack((array_input,append_input)).tolist()#最终合并
            print("append2+2")
            return (output,array_input2,append_input2)

class array_is_null:#输入数组，输出是否为空
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{"array_input": ("LIST",),}}    
    CATEGORY = CATEGORY_str1+CATEGORY_str3
    RETURN_TYPES = ("BOOL",) 
    RETURN_NAMES = ("IsNull",)
    FUNCTION = "array6"
    def array6(self,array_input):
        if not isinstance(array_input,list):return (True,)
        if array_input == []:return (True,)
        else:return (False,)

class array_attribute:#输入数组，输出数组长度
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required":
                    {   "array_input": ("LIST",),                        
                    }
                } 
    CATEGORY = CATEGORY_str1+CATEGORY_str3
    RETURN_TYPES = ("INT","INT","INT",)
    RETURN_NAMES = ("length","size","dimension")
    FUNCTION = "array7"
    def array7(self,array_input):
        if array_input == []:return (0,0,0)
        else:
            array_input = np.array(array_input)
            return(len(array_input),array_input.size,array_input.ndim)

class array_convert:#输入数组，输出3种转换
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{"array_input": ("LIST",),}}    
    CATEGORY = CATEGORY_str1+CATEGORY_str3
    RETURN_TYPES = ("LIST","LIST","STRING",)
    RETURN_NAMES = ("array_int","array_abs","array_str")
    FUNCTION = "array_convert1"
    def array_convert1(self,array_input):
        if isinstance(array_input,list):
            array_input=np.array(array_input)
        return (array_input.astype(int).tolist(),
                np.abs(array_input).tolist(),
                str(array_input.tolist()))

class array_select_element:#输入数组、指定索引,输出数组中指定元素
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required":
                    {   "array_input": ("LIST",),                        
                        "index": ("STRING", {"default":"0,2,1",}),
                    }
                }
    CATEGORY = CATEGORY_str1+CATEGORY_str3
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("element_array",)
    FUNCTION = "array_select_element1"
    def array_select_element1(self,array_input,index):
        if array_input == []:return ([],)
        list1=np.array(strtolist.tolist_v2(index,to_oneDim=True,to_int=True))
        if len(list1) == 0:return ([],)
        list1[list1 >= len(array_input)] = len(array_input)-1
        array1=[]
        for i in list1: array1.append(array_input[i])
        return(array1,)

NODE_CLASS_MAPPINGS = {
    "array-step": array_step,
    "array-end-increment": array_end_increment,
    "array-end-step": array_end_step,
    "array-step-increment": array_step_increment,
    "string-to-array": string_to_array,

    "array-t": array_t,
    "array-number-to-angle": array_number_to_angle,
    "array-append": array_append,
    "array-is-null": array_is_null,
    "array-attribute": array_attribute,
    "array-convert": array_convert,
    "array-select-element": array_select_element,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "array-step": "array1 step",
    "array-end-increment": "array1 end increment",
    "array-end-step": "array1 end step",
    "array-step-increment": "array1 step increment",
    "string-to-array": "string to array1",

    "array-t": "array1 t",
    "array-number-to-angle": "array1 number to angle",
    "array-append": "array1 append",
    "array-is-null": "array1 is null",
    "array-attribute": "array1 attribute",
    "array-convert": "array1 convert",
    "array-select-element": "array1 select element",
}