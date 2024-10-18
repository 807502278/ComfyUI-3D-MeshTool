import os
import json
import numpy as np
import torch
import torchvision.transforms.functional
from PIL import Image
from collections import deque
from loguru import logger
from ..moduel.getdata import load_image_to_tensor
from ..moduel.file import split_path

log_file_path = "app.log"
logger.add(log_file_path, level="INFO")
# from ..moduel.paint3d import TexturedMeshModel

CATEGORY_str1 = "3D_MeshTool/Convert"


class array_to_camposes:  # 输入数组，输出转化为CAMPOSES格式的数组
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":
            {
                "array_input": ("LIST", {"default": []}),
            }
        }
    CATEGORY = CATEGORY_str1
    # [orbit radius, elevation, azimuth, orbit center X, orbit center Y, orbit center Z]
    RETURN_TYPES = ("ORBIT_CAMPOSES",)
    RETURN_NAMES = ("CamPoses",)
    INPUT_IS_LIST = (True,)
    FUNCTION = "array8"

    def array8(self, array_input):
        if array_input == []:
            print(
                "warning1:The input array does not meet the requirements!Output basic camera array")
            return ([[5, 0, 0, 0, 0, 0],],)
        array_input = np.array(array_input[0])
        if array_input.ndim != 2 or array_input.shape[1] != 6:
            print(
                "warning2:The input array does not meet the requirements!Output basic camera array")
            return ([[5, 0, 0, 0, 0, 0],],)
        else:
            return (array_input.tolist(),)


class RT_to_camposes:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "rotation": ("Tensor",),
                "translation": ("Tensor",),
            },
            "optional": {
                "orbit_radius": ("LIST")
            }
        }
    CATEGORY = CATEGORY_str1
    RETURN_TYPES = ("ORBIT_CAMPOSES",)
    RETURN_NAMES = ("CamPos",)
    FUNCTION = "cam_pos"

    def cam_pos(self, rotation, translation, orbit_radius=None):
        n = translation.shape[0]
        m = rotation.shape[0]
        if n != m:
            print(
                "Error-RT_to_camposes: The number of rotation and position data is not equal !")
            return None
        if orbit_radius is None:
            orbit_radius = torch.zeros(1, n, dtype=torch.float32)
            orbit_radius[0, :] = 1.75
        elif orbit_radius.shape[0] != n:
            print("Error-RT_to_camposes: The amount of data for orbital radius needs to be the same as that for transformation data !")
            return None

        rotation[:, 2] = rotation[:, 1]
        rotation[:, 1] = rotation[:, 0]
        rotation[:, 0] = orbit_radius[0, :]

        cam_poses = np.hstack((rotation, translation))
        return (cam_poses.tolist(),)


class List_to_Tensor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "array": ("LIST",),
            },
        }
    CATEGORY = CATEGORY_str1
    RETURN_TYPES = ("Tensor",)
    RETURN_NAMES = ("Tensor",)
    FUNCTION = "to_Tensor"

    def to_Tensor(self, array):
        return (torch.tensor(array),)


class Tensor_to_List:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Tensor": ("Tensor",),
            },
        }
    CATEGORY = CATEGORY_str1
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("array",)
    FUNCTION = "to_Tensor"

    def to_Tensor(self, Tensor):
        return (Tensor.tolist(),)


class Tensor_Exchange_dim:  # 待开发
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Tensor": ("Tensor",),
                "dim1": ("INT", {"default": 0}),
                "dim2": ("INT", {"default": 1}),
            },
        }
    CATEGORY = CATEGORY_str1
    RETURN_TYPES = ("Tensor",)
    RETURN_NAMES = ("Tensor",)
    FUNCTION = "exchange_dim"

    def exchange_dim(self, Tensor, dim1, dim2):
        return (Tensor.transpose(dim1, dim2),)


class Tensor_Exchange_element:  # 待开发
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Tensor": ("Tensor",),
                "index1": ("INT", {"default": 0}),
                "index2": ("INT", {"default": 1}),
            },
        }
    CATEGORY = CATEGORY_str1
    RETURN_TYPES = ("Tensor",)
    RETURN_NAMES = ("Tensor",)
    FUNCTION = "exchange_element"

    def exchange_element(self, Tensor, index1, index2):
        Tensor[index1], Tensor[index2] = Tensor[index2], Tensor[index1]
        return (Tensor,)


class Tensor_slice:  # 待开发
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Tensor": ("Tensor",),
                "start": ("INT", {"default": 0}),
                "end": ("INT", {"default": 1}),
            },
        }
    CATEGORY = CATEGORY_str1
    RETURN_TYPES = ("Tensor",)
    RETURN_NAMES = ("Tensor",)
    FUNCTION = "slice_tensor"

    def slice_tensor(self, Tensor, start, end, step):
        return (Tensor[start:end:step],)


CATEGORY_str1 = "3D_MeshTool/Camera"


class json_to_campos:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_campos_dir": ("STRING", {}),
                "to_angle": ("BOOLEAN", {"default": True}),
            },
        }
    CATEGORY = CATEGORY_str1
    RETURN_TYPES = ("Tensor", "Tensor", "Tensor", "IMAGE")
    RETURN_NAMES = ("rotation", "translation", "coordinates", "Image")
    FUNCTION = "to_campos"

    def to_campos(self, json_campos_dir, to_angle):
        translation, rotation, coordinates, filelist = self.read_camdata(
            json_campos_dir)
        image_bath = load_image_to_tensor(filelist)
        if to_angle:
            rotation = rotation * 57.29577951308232
        print(f"debug---------translation {translation.shape}")
        print(f"debug---------rotation {rotation.shape}")
        print(f"debug---------coordinates {coordinates.shape}")
        return (rotation, translation, coordinates, image_bath)

    def read_camdata(self, dir, inspect_file=True):
        # read json file and extract data 读取json文件并提取数据
        with open(dir, 'r', encoding='utf-8') as file:
            content = file.read()
            try:
                c = json.loads(content)['features']
            except json.JSONDecodeError:
                print("Error-json_to_campos: The JSON data is not valid")

        # Create 4 all 0 tensors to store data 新建4个全0张量用于储存数据
        n = len(c)
        translation = torch.zeros(1, 3)
        rotation = torch.zeros(1, 3)
        coordinates = torch.zeros(1, 3)
        filelist = []
        dir_img, *p = split_path(dir)

        # Extract 4 pieces of data 提取4条数据
        for i in range(n):
            translation = torch.cat((translation, torch.tensor(
                c[i]["properties"]['translation']).unsqueeze(0)), 0)
            rotation = torch.cat((rotation, torch.tensor(
                c[i]["properties"]['rotation']).unsqueeze(0)), 0)
            coordinates = torch.cat((coordinates, torch.tensor(
                c[i]["geometry"]['coordinates']).unsqueeze(0)), 0)
            # Absolute path of synthesized image 合成图像的绝对路径
            filelist.append(c[i]["properties"]["filename"])
            filelist[i] = os.path.join(dir_img, filelist[i])

        # Remove the first all 0 tensor created during creation 移除创建时的第1个全0张量
        translation = translation[1:]
        rotation = rotation[1:]
        coordinates = coordinates[1:]

        # Check if the corresponding image exists 检查对应的图像是否存在
        if inspect_file:
            if len(filelist) == 0:
                print("Error-json_to_campos: No image file was found in the JSON data. ")
            else:
                del_list = []
                for i in range(len(filelist)):
                    if not os.path.isfile(filelist[i]):
                        del_list = del_list.append(i)
                del_n = len(del_list)
                if del_n >= len(filelist):  # All files do not exist 全部文件不存在
                    print(
                        "Error-json_to_campos: No corresponding image was found in the same directory as the JSON file. ")
                    print(
                        "Error-json_to_campos: Please check if the data corresponds to the image")
                elif del_n > 0:  # Some files do not exist 有部分文件不存在
                    set_all = set(range(len(filelist)))
                    set_del = set(del_list)
                    set_remain = set_all-set_del

                    translation = torch.tensor(np.array(translation)[filelist])
                    rotation = torch.tensor(np.array(rotation)[filelist])
                    filelist = np.array(filelist)[filelist]
                    del_filedata = np.array(list(set_remain))
                    print(
                        f"Warning-json_to_campos: There are {del_n} images not found")
                    print(
                        f"Warning-json_to_campos: The corresponding data of these images will be deleted: {del_filedata}")
                else:
                    print("All files are valid")
        return translation, rotation, coordinates, filelist


class img_bath_rotationZ:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "rotation": ("Tensor",),
                "image_bath": ("IMAGE",),
                "flip_angle": ("BOOLEAN", {"default": True})
            },
        }
    CATEGORY = CATEGORY_str1
    RETURN_TYPES = ("Tensor", "IMAGE")
    RETURN_NAMES = ("rotation_Z0", "Image_z0")
    FUNCTION = "cam_pos"

    def cam_pos(self, image_bath, flip_angle, rotation):
        # 旋转图像
        bath = image_bath.shape[0]
        if bath > 1:
            if flip_angle:
                rotation_z = rotation[:, 2:] * -1
            else:
                rotation_z = rotation[:, 2:]
            n = len(rotation_z)
            if n == bath:
                for i in range(bath):
                    ro = float(rotation_z[i])
                    Tensor = image_bath[i].permute(2, 0, 1)
                    Tensor = torchvision.transforms.functional.rotate(
                        Tensor, ro, fill=0.5)
                    image_bath[i] = Tensor.permute(1, 2, 0)
                    print(f"The first {i} rotate {ro} degrees")
            else:
                print(
                    "Error-json_to_campos: The amount of JSON data is not equal to the batch of images")
                print(f"Error: Not rotated: bath={bath},json_data={n} ")
                print("Error: Please check if the data matches")
        else:
            print("""warning-json_to_campos:The input image does not meet the requirements and requires a batch greater than 1!
                  This time only outputs the basic camera array""")
        rotation[:, :2] = 0.0
        return (rotation, image_bath)


class img_bath_move:  # 待开发
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "translation": ("Tensor",),
                "image_bath": ("IMAGE",),
            },
        }
    CATEGORY = CATEGORY_str1
    RETURN_TYPES = ("Tensor", "IMAGE")
    RETURN_NAMES = ("translation", "Image")
    FUNCTION = "cam_pos"

    def cam_pos(self, image_bath, translation):
        # 平移图像
        bath = image_bath.shape[0]
        if bath > 1:
            n = len(translation)
            if n == bath:
                for i in range(bath):
                    tx = float(translation[i][0])
                    ty = float(translation[i][1])
                    tz = float(translation[i][2])
                    Tensor = image_bath[i].permute(2, 0, 1)
                    Tensor = torchvision.transforms.functional.affine(
                        Tensor, 0, (tx, ty), 1, 0, (0, 0), fillcolor=0.5)
                    image_bath[i] = Tensor.permute(1, 2, 0)
                    print(f"The first {i} move {tx}, {ty}, {tz}")
            else:
                print(
                    "Error-json_to_campos: The amount of JSON data is not equal to the batch of images")
                print(f"Error: Not moved: bath={bath},json_data={n} ")
                print("Error: Please check if the data matches")
        else:
            print("""warning-json_to_campos:The input image does not meet the requirements and requires a batch greater than 1!
                  This time only outputs the basic camera array""")
        return (translation, image_bath)


class Paint3D_mesh_get:  # 待开发
    pass


class Paint3D_mesh_set:  # 待开发
    pass


NODE_CLASS_MAPPINGS = {
    "array-to-camposes": array_to_camposes,
    "List_to_Tensor": List_to_Tensor,
    "Tensor_to_List": Tensor_to_List,

    "json-to-campos": json_to_campos,
    "img-bath-rotationZ": img_bath_rotationZ,
    "RT-to-camposes": RT_to_camposes,
    # "cam-pos-bus": cam_pos_bus,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "array-to-camposes": "array1 to camposes",
    "List_to_Tensor": "List to Tensor",
    "Tensor_to_List": "Tensor to List",

    "json-to-campos": "json to camposes",
    "img-bath-rotationZ": "img bath rotationZ",
    "RT-to-camposes": "RT to camposes",
    # "cam-pos-bus": "cam pos bus",
}
