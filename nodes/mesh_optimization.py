"""
@author: 807502278
@title: 3D Mesh Tool
@nickname: 3D Mesh Tool
@description: A simple 3D model processing tool within ComfyUI
"""

import numpy as np
import torch
from kiui.mesh_utils import clean_mesh, decimate_mesh
from ..moduel.MeshTool import meshclean

class mesh_Optimization:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh":("MESH",),
                "Optimization_to":("FLOAT",{"default":0.65,"min":0,"max":1.0,"step":0.05}),#优化面到此百分比
                "algorithm":("BOOLEAN",{"default":"True","label_on": "pymeshlab", "label_off": "pyfqmr"}),#选优化算法
                "remesh":("BOOLEAN",{"default":False}),#是否刷新网格
                "optimalplacement":("BOOLEAN",{"default":True}),#是否平滑
                },
            }
    CATEGORY = "3D_MeshTool/optimization"
    RETURN_TYPES = ("MESH","INT","INT",)
    RETURN_NAMES = ("Mesh_Out","Face_Before","Face_After",)
    FUNCTION = "mesh_edit_Optimization"
    def mesh_edit_Optimization(self,mesh,Optimization_to,algorithm,remesh,optimalplacement):
        #new_v,new_f = None,None
        v = mesh.v.detach().cpu().numpy()
        f = mesh.f.detach().int().cpu().numpy()
        nv=v.shape[0];nf=f.shape[0]
        f1=int(nf*Optimization_to)
        print("Mesh has %d vertices and %d faces." % (nv, nf))
        print("Optimization to %d faces." % (f1))
        if algorithm:algorithm="pymeshlab"
        else:algorithm="pyfqmr"
        if Optimization_to > 0.0 and Optimization_to <= 1.0:
            new_v,new_f=decimate_mesh(v,f,f1,algorithm,remesh,optimalplacement)
            mesh.v = torch.from_numpy(new_v).contiguous().float().to(mesh.device)
            mesh.f = torch.from_numpy(new_f).contiguous().float().to(mesh.device)
            meshclean.revf3(mesh)
        return (mesh,nf,f1)

class mesh_Cleanup:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh":("MESH",),
                "Cleanup_block_nf":("FLOAT",{"default":0.05,"min":0,"max":1.0,"step":0.05}),#清理掉面小于此百分比(相对于总面数)的块
                "Cleanup_block_sc":("INT",{"default":20,"min":0,"max":100,"step":1}),#清理掉小于此直径的块
                "Merge_vertex_threshold":("INT",{"default":1,"min":1,"max":1000,"step":1}),#合并顶点阈值
                "repair_face":("BOOLEAN",{"default":True}),#是否修复非流形面
                #"re_mesh":("BOOLEAN",{"default":True}),#是否重新执行网格划分
                #"remesh_size":("FLOAT",{"default":0.01,"min":0.001,"max":1.0,"step":0.01}),#重新执行网格划分的大小
                #"remesh_iters":("INT",{"default":10,"min":1,"max":100,"step":1}),#重新执行网格划分的迭代次数
                },
            }
    CATEGORY = "3D_MeshTool/optimization"
    RETURN_TYPES = ("MESH","INT","INT",)
    RETURN_NAMES = ("Mesh_Out","Face_Before","Face_After",)
    FUNCTION = "mesh_edit_Cleanup"
    def mesh_edit_Cleanup(self,
                          mesh,
                          Cleanup_block_nf,
                          Cleanup_block_sc,
                          Merge_vertex_threshold,
                          repair_face
                          ):
        v = mesh.v.detach().cpu().numpy()
        f = mesh.f.detach().int().cpu().numpy()
        nf=len(f)
        f1=int(nf*Cleanup_block_nf)
        if Cleanup_block_nf > 0.0 and Cleanup_block_nf <= 1.0:
            new_v,new_f=clean_mesh(v,
                                   f,
                                   v_pct = Merge_vertex_threshold,
                                   min_f = f1,
                                   min_d = Cleanup_block_sc,
                                   repair = repair_face,
                                   remesh = False,
                                   )
            mesh.v = torch.from_numpy(new_v).contiguous().float().to(mesh.device)
            mesh.f = torch.from_numpy(new_f).contiguous().float().to(mesh.device)
            meshclean.revf3(mesh)
        return (mesh,nf,f1)

class mesh_subdivide:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh":("MESH",),
                "repair_face":("BOOLEAN",{"default":True}),#是否修复非流形面
                "re_mesh":("BOOLEAN",{"default":True}),#是否重新执行网格划分
                "remesh_size":("FLOAT",{"default":0.01,"min":0.001,"max":1.0,"step":0.01}),#重新执行网格划分的大小
                "remesh_iters":("INT",{"default":10,"min":1,"max":100,"step":1}),#重新执行网格划分的迭代次数
                "Merge_vertex_threshold":("INT",{"default":1,"min":1,"max":1000,"step":1}),#合并顶点阈值
                },
            }
    CATEGORY = "3D_MeshTool/optimization"
    RETURN_TYPES = ("MESH",)
    RETURN_NAMES = ("mesh_subdivide",)
    FUNCTION = "mesh_subdivide"
    def mesh_subdivide(self,mesh,repair_face,re_mesh,remesh_size,remesh_iters,Merge_vertex_threshold):
        v = mesh.v.detach().cpu().numpy()
        f = mesh.f.detach().int().cpu().numpy()
        new_v,new_f=clean_mesh(v,
                               f,
                               v_pct = Merge_vertex_threshold,
                               min_f = 32,
                               min_d = 5,
                               repair = repair_face,
                               remesh = re_mesh,
                               remesh_size = remesh_size,
                               remesh_iters = remesh_iters,
                               )
        mesh.v = torch.from_numpy(new_v).contiguous().float().to(mesh.device)
        mesh.f = torch.from_numpy(new_f).contiguous().float().to(mesh.device)
        meshclean.revf3(mesh)
        return (mesh,)

NODE_CLASS_MAPPINGS={
    "Mesh_Optimization":mesh_Optimization,
    "Mesh_Cleanup":mesh_Cleanup,
    "Mesh_Subdivide":mesh_subdivide,
    }
NODE_DISPLAY_NAMES_MAPPINGS={
    "Mesh_Optimization":"Mesh Optimization",
    "Mesh_Cleanup":"Mesh Cleanup",
    "Mesh_Subdivide":"Mesh Subdivide",
    }