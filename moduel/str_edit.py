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
    def convert_list(cls, string_input, to_list=True, arrangement=2):
        if string_input != "":
            if arrangement == 0:
                if string_input[0] != "[":
                    string_input = "[" + string_input
                if string_input[-1] != "]":
                    string_input = string_input + "]"
                if to_list:
                    string_input = ast.literal_eval(string_input)
            elif arrangement == 1:
                string_input = cls.tolist_v1(string_input, to_list=to_list)
            elif arrangement == 2:
                string_input = cls.tolist_v2(string_input, to_list=to_list)
            else:
                print("Currently, there are only two versions, v1 and v2.")
                string_input = None
        else:
            if to_list:
                string_input = []
        return string_input


    def tolist_v1(cls, user_input, to_list=True):  # Abandoned
        user_input = user_input.replace('{', '[').replace('}', ']')
        user_input = user_input.replace('(', '[').replace(')', ']')
        user_input = user_input.replace('，', ',')
        user_input = re.sub(r'\s+', '', user_input)
        user_input = re.sub(r'[^\d,.\-[\]]', '', user_input)
        user_input = "[" + user_input + "]"
        if to_list:
            user_input = ast.literal_eval(user_input)
        return user_input

    @classmethod
    # Convert to array/array format string
    def tolist_v2(cls, str_input, to_list=True, to_oneDim=False, to_int=False, positive=False):
        str_input = re.sub(r'\s+|\"', '', str_input)  # safe conversion
        if str_input == "":
            if to_list:
                return []
            else:
                return ""
        else:
            str_input = str_input.replace('，', ',')  # Replace Chinese comma
            if to_oneDim:
                str_input = re.sub(r'[\(\)\[\]\{\}（）【】｛｝]', "", str_input)
                str_input = "[" + str_input + "]"
            else:
                str_input = re.sub(
                    r'[\(\[\{（【｛]', '[', str_input)  # Replace parentheses
                # Replace reverse parentheses
                str_input = re.sub(r'[\)\]\}）】｝]', ']', str_input)
                if str_input[0] != "[":
                    str_input = "[" + str_input + "]"
            # Remove non numeric characters, but do not include,.-[]
            str_input = re.sub(r'[^\d,.\-[\]]', '', str_input)
            # If "," is not preceded by a number, remove it
            str_input = re.sub(r'(?<![0-9])[,]', '', str_input)
            str_input = re.sub(r'\.{2,}', '.', str_input)  # Remove excess .
            if positive:
                str_input = re.sub(r'-', '', str_input)  # Remove -
            else:
                str_input = re.sub(r'-{2,}', '-', str_input)  # Remove excess -

            # Convert the organized string into an array and output it
            list1 = ast.literal_eval(str_input)
            if to_list:
                return list1
            elif to_list and to_int:
                return list1.astype(int)
            else:
                return str_input

    # Parenthesical completion (to be developed) 括号补全(待开发)
    def repair_brackets(cls, str_input):
        pass
