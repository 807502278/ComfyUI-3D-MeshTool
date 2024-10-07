import numpy as np
#from ..moduel.paint3d import TexturedMeshModel

CATEGORY_str1="3D_MeshTool/Convert"


class array_to_camposes:#输入数组，输出转化为CAMPOSES格式的数组
    @classmethod
    def INPUT_TYPES(s): 
        return {
                "required":
                    {
                        "array_input": ("LIST",{"default":[]}),
                    }
                }
    CATEGORY = CATEGORY_str1
    RETURN_TYPES = ("ORBIT_CAMPOSES",)#[orbit radius, elevation, azimuth, orbit center X, orbit center Y, orbit center Z]
    RETURN_NAMES = ("CamPoses",)
    INPUT_IS_LIST = (True,)
    FUNCTION = "array8"
    def array8(self,array_input):
        if array_input == []:
            print("warning1:The input array does not meet the requirements!Output basic camera array")
            return ([[5,0,0,0,0,0],],)
        array_input=np.array(array_input[0])
        if array_input.ndim!= 2 or array_input.shape[1]!= 6:
            print("warning2:The input array does not meet the requirements!Output basic camera array")
            return ([[5,0,0,0,0,0],],)
        else:
            return (array_input.tolist(),)

class cam_pos_bus:#未完成
    @classmethod
    def INPUT_TYPES(s): 
        return {
                "required":
                    {
                        "cam_pos_int": ("ORBIT_CAMPOSES",{"default":[[5,0,0,0,0,0],]}),
                        "cam_pos_ext": ("LIST",{"default":[]}),
                    }
                }
    CATEGORY = "3D_MeshTool/Camera"
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("CamPosBus",)
    INPUT_IS_LIST = (False,)
    FUNCTION = "cam_pos_bus"
    def cam_pos_bus(self,cam_poses):
        return (cam_poses,)

class Paint3D_mesh_get:
    pass

class Paint3D_mesh_set:
    pass

NODE_CLASS_MAPPINGS = {
    "array-to-camposes": array_to_camposes,
    #"cam-pos-bus": cam_pos_bus,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "array-to-camposes": "array1 to camposes",
    #"cam-pos-bus": "cam pos bus",
}