"""
@author: 807502278
@title: 3D Mesh Tool
@nickname: 3D Mesh Tool
@description: A simple 3D model processing tool within ComfyUI
"""

import numpy as np
import os
import torch
import folder_paths as comfy_paths
import time
from ..moduel.mesh_class import Mesh
from kiui.typing import *

SUPPORTED_3D_EXTENSIONS = (
    '.obj',
    #'.ply',
    #'.glb',
)
CATEGORY_str1 = "3D_MeshTool/" 

#---------------Basics class---------------
CATEGORY_str2 = "Basics"

class load_mesh:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {
                        "mesh_file_path":("STRING",{"default":""}),
                        "reload":("BOOLEAN",{"default":False}),
                     },
                }
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "load_mesh"
    #def load_mesh(self, path,reload):
    #cls, path, resize=True, clean=False, renormal=True, retex=False, bound=0.9, front_dir='+z', **kwargs
    def load_mesh(self,mesh_file_path,reload):
        if reload:
            print(f"reload loading mesh time:{time.time()}")
        mesh = None
        if not os.path.isabs(mesh_file_path):
            mesh_file_path = os.path.join(comfy_paths.input_directory, mesh_file_path)
        if os.path.exists(mesh_file_path):
            folder, filename = os.path.split(mesh_file_path)
            if filename.lower().endswith(SUPPORTED_3D_EXTENSIONS):
                with torch.inference_mode(True):
                    mesh = Mesh.load(mesh_file_path)
            else:
                print(f"[{self.__class__.__name__}] File name {filename} does not end with supported 3D file extensions: {SUPPORTED_3D_EXTENSIONS}")
        else:
            print(f"[{self.__class__.__name__}] File {mesh_file_path} does not exist").error.print()
        return (mesh, )
    
class mesh_data:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{"mesh":("MESH",),},}
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("LIST","LIST","LIST","LIST","IMAGE","IMAGE","STRING")
    RETURN_NAMES = ("vertex+face","Normal(vn+fn)","UVs(vt+ft)","vertex_color[N3]","Texture_Diffuse","Texture_reflection","mesh_device")
    FUNCTION = "mesh_data"
    def mesh_data(self,mesh):
        vertex_face=[mesh.v,mesh.f]
        Normal = [mesh.vn,mesh.fn]
        UVs=[mesh.vt,mesh.ft]
        vertex_color=mesh.vc
        Texture_Diffuse=mesh.albedo
        Texture_reflection=mesh.metallicRoughness
        mesh_device=mesh.device
        return (vertex_face,Normal,UVs,vertex_color,Texture_Diffuse,Texture_reflection,mesh_device)

class mesh_data_Statistics:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{"mesh":("MESH",),},}
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("LIST","INT","INT","BOOLEAN","BOOLEAN","BOOLEAN","BOOLEAN","BOOLEAN","STRING")
    RETURN_NAMES = ("Output_Group","vertex_num","face_num","Normal_true","UVs_true","vertex_color_true","Texture_Diffuse_true","Texture_reflection_true","device")
    FUNCTION = "mesh_number"
    def mesh_number(self,mesh):
        v_num=mesh.v.shape[0]
        f_num=mesh.f.shape[0]
        Normal_true=mesh.vn is not None
        UVs_true=mesh.vt is not None
        vertex_color_true=mesh.vc is not None
        Texture_Diffuse_true=mesh.albedo is not None
        Texture_reflection_true=mesh.metallicRoughness is not None
        mesh_device_true=mesh.device
        Output_Group={"vertex":v_num,"face  ":f_num,"Normal":Normal_true,"UVs   ":UVs_true,"v_color":vertex_color_true,"T_Diffuse":Texture_Diffuse_true,"T_reflection":Texture_reflection_true,"mesh_device":mesh_device_true}
        return (Output_Group,v_num,f_num,Normal_true,UVs_true,vertex_color_true,Texture_Diffuse_true,Texture_reflection_true,mesh_device_true)

class mesh_data_bus:#未完成
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                            "mesh":("MESH",{"default":None}),
                            "vertex":("LIST",{"default":None}),
                            "face":("LIST",{"default":None}),
                            "Normal_v":("LIST",{"default":None}),
                            "Normal_f":("LIST",{"default":None}),
                            "UVs_v":("LIST",{"default":None}),
                            "UVs_f":("LIST",{"default":None}),
                            "vertex_color":("LIST",{"default":None}),
                            "Texture_Diffuse":("IMAGE",{"default":None}),
                            "Texture_reflection":("IMAGE",{"default":None}),
                            },}
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("LIST","LIST","LIST","LIST","LIST","LIST","LIST","IMAGE","IMAGE",)
    RETURN_NAMES = ("vertex[N3]","face[N2]","Normal_v[N3]","Normal_f[N2]","UVs_v[N3]","UVs_f[N2]","vertex_color[N3]","Texture_Diffuse","Texture_reflection",)
    FUNCTION = "mesh_data_bus"
    def mesh_data_bus(self,mesh,vertex,face,Normal_v,Normal_f,UVs_v,UVs_f,vertex_color,Texture_Diffuse,Texture_reflection):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        list1=[vertex,face,Normal_v,Normal_f,UVs_v,UVs_f,vertex_color]
        list2=["vertex","face","Normal_v","Normal_f","UVs_v","UVs_f","vertex_color"]
        for i in len(list1):
            if i is not None:
                if type(i)==torch.Tensor:
                    exec(f"mesh.{list2[i]}=vertex")
                if type(i)==list:
                    mesh.v=torch.tensor(vertex, dtype=torch.float32, device=mesh.device)

        return (mesh,vertex,face,Normal_v,Normal_f,UVs_v,UVs_f,vertex_color,Texture_Diffuse,Texture_reflection)

class mesh_clean_data:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
            "mesh":("MESH",),
            "normal":("BOOLEAN",{"default":False}),
            "uv":("BOOLEAN",{"default":False}),
            "v_color":("BOOLEAN",{"default":False}),
            "texture_diffuse":("BOOLEAN",{"default":False}),
            "texture_reflection":("BOOLEAN",{"default":False}),
                },
            }
    CATEGORY = CATEGORY_str1+CATEGORY_str2
    RETURN_TYPES = ("MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "mesh_clean_data"
    def mesh_clean_data(self,mesh,normal,uv,v_color,texture_diffuse,texture_reflection):
        if normal:
            mesh.vn = None
            mesh.fn = None
        if uv:
            mesh.vt = None
            mesh.ft = None
        if v_color:
            mesh.vc = None
        if texture_diffuse:
            mesh.albedo = None
        if texture_reflection:
            mesh.metallicRoughness = None
        return (mesh,)

NODE_CLASS_MAPPINGS={
    "Load_OBJ":load_mesh,
    "Mesh_Data":mesh_data,
    "Mesh_Data_Statistics":mesh_data_Statistics,
    #"mesh_data_bus":mesh_data_bus,
    "Mesh_Clean_Data":mesh_clean_data,
    }
NODE_DISPLAY_NAMES_MAPPINGS={
    "Load_OBJ":"Load OBJ",
    "Mesh_Data":"Mesh Data",
    "Mesh_Data_Statistics":"Mesh Data Statistics",
    #"mesh_data_bus":"mesh data bus",
    "Mesh_Clean_Data":"Mesh Clean Data",
    }