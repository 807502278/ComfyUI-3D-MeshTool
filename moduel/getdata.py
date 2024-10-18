import os
import json
import cv2
import numpy as np
import torch
from PIL import Image
from typing import Union
from tqdm import tqdm

"""
Load files and read data through keys or items...
加载文件,通过key或item读取数据...
"""


def read_file(file_path, key=None):
    with open(file_path, 'r') as f:
        data = json.loads(f.read())
    if key is None:
        return data
    elif isinstance(key, (str, int)):
        return data[key]
    elif isinstance(key, list):
        data_k = []
        for k in key:
            data_k.append(data[k])
        return data_k
    elif isinstance(key, dict):
        data_k = []
        for k, v in key.items():
            data_k.append(data[k][v])
        return data_k
    else:
        print("Error: read_file[1] - Entered a type that does not match")
        return None


def get_device_list():
    device_str = ["default", "cpu"]
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            device_str.append(f"cuda:{i}")
    if torch.backends.mps.is_available():
        device_str.append("mps:0")
    n = len(device_str)
    if n > 2:  # default device 默认设备
        device_default = torch.device(device_str[2])
    else:
        device_default = torch.device(device_str[1])
    # Establish a device list dictionary 建立设备列表字典
    device_list = {device_str[0]: device_default, }
    for i in range(n-1):
        device_list[device_str[i+1]] = torch.device(device_str[i+1])

    return [device_list, device_default]
#
# from ..moduel.getdata import get_device_list
# device_list, device_default = get_device_list()


# 从路径加载图像为torch.tensor
def load_image_to_tensor(image_path: Union[str, list, np.ndarray]):
    order = (0, 1, 2)
    if type(image_path) == str:
        if os.path.isfile(image_path):
            image = Image.open(image_path)
            img_np = np.array(image).transpose(*order)
            tensor = torch.from_numpy(img_np).float() / 255.0
            return tensor.repeat(1, 1, 1, 1)
        else:
            print("Error: load_image_to_tensor - File not found")
            return None
    if type(image_path) == list:
        image_path = np.array(image_path)
    if type(image_path) == np.ndarray:
        images = []
        print("Loading images bath:")
        for i in tqdm(range(np.size(image_path))):
            path=image_path[i]
            if isinstance(path, str) and os.path.isfile(path):
                image = Image.open(path)
                img_np = np.array(image).transpose(*order)
                images.append(torch.from_numpy(img_np).float() / 255.0)
            elif isinstance(path, np.ndarray): #如果是二维
                for j in range(len(path)):
                    if isinstance(path[j], str) and os.path.isfile(path[j]):
                        image = Image.open(path[j])
                        img_np = np.array(image).transpose(*order)
                        images.append(torch.from_numpy(img_np).float() / 255.0)
        if images:
            return torch.stack(images)
        else:
            print("Error: load_image_to_tensor - File not found")
            return None
