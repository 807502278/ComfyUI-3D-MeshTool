import numpy as np
import ast
import re

class strtolist:
    DESCRIPTION = """
    str_to_list.convert_list(string_input, arrangement=True): Converts a string to a list.
        If arrangement=True, it cleans unnecessary characters by default.
    str_to_list.str_arrangement(user_input): Converts a string to a list-style string.
    """
    def __init__(self):
        pass
    @classmethod
    def convert_list(cls, string_input,arrangement=2):
        if string_input == "":
            return ([],)
        if arrangement==1:
            string_input = cls.tolist_v1(string_input)
        elif arrangement == 2 :
            string_input = cls.tolist_v2(string_input)
        if string_input[0] != "[":
            string_input = "[" + string_input + "]"
            return (ast.literal_eval(string_input),)
        else:
            return (ast.literal_eval(string_input),)
        
    def tolist_v1(cls,user_input):#Abandoned
        user_input = user_input.replace('{', '[').replace('}', ']')
        user_input = user_input.replace('(', '[').replace(')', ']')
        user_input = user_input.replace('，', ',')
        user_input = re.sub(r'\s+', '', user_input)
        user_input = re.sub(r'[^\d,.\-[\]]', '', user_input)
        return user_input
    @classmethod
    def tolist_v2(cls,str_input,to_list=True,to_oneDim=False,to_int=False,positive=False):#Convert to array/array format string
        str_input = re.sub(r'\s+|\"', '', str_input)#safe conversion
        if str_input == "":
            if to_list:return ([],)
            else:return ""
        else:
            str_input = str_input.replace('，', ',')#Replace Chinese comma
            if to_oneDim:
                str_input = re.sub(r'[\(\)\[\]\{\}（）【】｛｝]', "" , str_input)
                str_input = "[" + str_input + "]"
            else:
                str_input=re.sub(r'[\(\[\{（【｛]', '[', str_input)#Replace parentheses
                str_input=re.sub(r'[\)\]\}）】｝]', ']', str_input)#Replace reverse parentheses
                if str_input[0] != "[":str_input = "[" + str_input + "]"
            str_input = re.sub(r'[^\d,.\-[\]]', '', str_input)#Remove non numeric characters, but do not include,.-[]
            str_input = re.sub(r'(?<![0-9])[,]', '', str_input)#If "," is not preceded by a number, remove it
            str_input = re.sub(r'\.{2,}', '.', str_input)#去除多余的.
            if positive:
                str_input = re.sub(r'-','', str_input)#移除-
            else:
                str_input = re.sub(r'-{2,}', '-', str_input)#去除多余的-
            list1=np.array(ast.literal_eval(str_input))
            if to_int:
                list1=list1.astype(int)
            if to_list:
                return list1.tolist()
            else:
                return str_input
            
    def repair_brackets(cls,str_input):#括号补全(待开发)
        pass