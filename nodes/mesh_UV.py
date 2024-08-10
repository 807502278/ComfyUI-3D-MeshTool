import numpy as np
import torch
import xatlas
from kiui.op import safe_normalize, dot
from ..moduel.mesh_class import Mesh

class UnwrapUV_xatlas:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh":("MESH",),
                "UV_options":("chart_options",{"default":None}),
                },
            }
    CATEGORY = "3D_MeshTool/Edit"
    RETURN_TYPES = ("MESH","LIST")
    RETURN_NAMES = ("mesh","vmapping")
    FUNCTION = "mesh_UV_xatlas"
    def mesh_UV_xatlas(self,mesh,UV_options=None):
        if UV_options is None:
            UV_options = xatlas.ChartOptions()
        v_np = mesh.v.detach().cpu().numpy()
        f_np = mesh.f.detach().int().cpu().numpy()
        atlas = xatlas.Atlas()
        atlas.add_mesh(v_np, f_np)
        atlas.generate(chart_options=UV_options)
        vmapping, ft_np, vt_np = atlas[0]  # [N], [M, 3], [N, 2]
        vt = torch.from_numpy(vt_np.astype(np.float32)).to(mesh.device)
        ft = torch.from_numpy(ft_np.astype(np.int32)).to(mesh.device)
        mesh.vt = vt # Not adding intermediate variables will result in an error
        mesh.ft = ft
        return (mesh,vmapping)

class UnwrapUV_Auto_xatlas:#已弃用
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"mesh":("MESH",),
                },
            }
    CATEGORY = "3D_MeshTool/Edit"
    RETURN_TYPES = ("MESH","LIST")
    RETURN_NAMES = ("mesh","vmapping")
    FUNCTION = "auto_uv"
    def auto_uv(self, mesh):
        """auto calculate the uv coordinates.
        Args:
            cache_path (str, optional): path to save/load the uv cache as a npz file, this can avoid calculating uv every time when loading the same mesh, which is time-consuming. Defaults to None.
            vmap (bool, optional): remap vertices based on uv coordinates, so each v correspond to a unique vt (necessary for formats like gltf). 
                Usually this will duplicate the vertices on the edge of uv atlas. Defaults to True.
        """
        v_np = mesh.v.detach().cpu().numpy()
        f_np = mesh.f.detach().int().cpu().numpy()
        atlas = xatlas.Atlas()
        atlas.add_mesh(v_np, f_np)
        chart_options = xatlas.ChartOptions()
        # chart_options.max_iterations = 4
        atlas.generate(chart_options=chart_options)
        vmapping, ft_np, vt_np = atlas[0]  # [N], [M, 3], [N, 2]
        # save to cache
        vt = torch.from_numpy(vt_np.astype(np.float32)).to(mesh.device)
        ft = torch.from_numpy(ft_np.astype(np.int32)).to(mesh.device)
        mesh.vt = vt
        mesh.ft = ft
        return (mesh,vmapping,)

class UV_options:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "fix_winding":("BOOLEAN",{"default":False}),#打包孤岛
                "max_boundary_length":("FLOAT",{"default":0.0,"min":0.0,"max":1.0,"step":0.01,"display": "slider"}),#边界长度限制
                "max_chart_area":("FLOAT",{"default":0.0,"min":0.0,"max":1.0,"step":0.01,"display": "slider"}),#最大面积限制
                "max_cost":("FLOAT",{"default":2.0,"min":0.0,"max":10.0,"step":0.1,"display": "slider"}),#最大限制
                "max_iterations":("INT",{"default":1,"min":1,"max":64,"step":1,"display": "slider"}),#最大迭代次数
                "normal_deviation_weight":("FLOAT",{"default":2.0,"min":0.0,"max":10.0,"step":0.1,"display": "slider"}),#法线偏差权重
                "normal_seam_weight":("FLOAT",{"default":4.0,"min":0.0,"max":10.0,"step":0.1,"display": "slider"}),#法线缝合权重
                "roundness_weight":("FLOAT",{"default":0.01,"min":0.0,"max":1.0,"step":0.01,"display": "slider"}),#圆度权重
                "straightness_weight":("FLOAT",{"default":6.0,"min":0.0,"max":10.0,"step":0.1,"display": "slider"}),#直线度权重
                "texture_seam_weight":("FLOAT",{"default":0.5,"min":0.0,"max":1.0,"step":0.01,"display": "slider"}),#纹理缝合权重
                },
            }
    CATEGORY = "3D_MeshTool/Edit"
    RETURN_TYPES = ("chart_options",)
    RETURN_NAMES = ("UV_options",)
    FUNCTION = "mesh_UV_xatlas2"
    def mesh_UV_xatlas2(self,fix_winding,
                        max_boundary_length,
                        max_chart_area,
                        max_cost,
                        max_iterations,
                        normal_deviation_weight,
                        normal_seam_weight,
                        roundness_weight,
                        straightness_weight,
                        texture_seam_weight):
        chart_options = xatlas.ChartOptions()
        chart_options.fix_winding = fix_winding
        chart_options.max_boundary_length = max_boundary_length
        chart_options.max_chart_area = max_chart_area
        chart_options.max_cost = max_cost
        chart_options.max_iterations = max_iterations
        chart_options.normal_deviation_weight = normal_deviation_weight
        chart_options.normal_seam_weight = normal_seam_weight
        chart_options.roundness_weight = roundness_weight
        chart_options.straightness_weight = straightness_weight
        chart_options.texture_seam_weight = texture_seam_weight
        return (chart_options,)

class Auto_Normal:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh":("MESH",),
                },
            }
    CATEGORY = "3D_MeshTool/Edit"
    RETURN_TYPES = ("MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "auto_normal"
    def auto_normal(self,mesh):
        """auto calculate the vertex normals.
        """
        i0, i1, i2 = mesh.f[:, 0].long(), mesh.f[:, 1].long(), mesh.f[:, 2].long()
        v0, v1, v2 = mesh.v[i0, :], mesh.v[i1, :], mesh.v[i2, :]
        face_normals = torch.cross(v1 - v0, v2 - v0, dim=-1)
        vn = torch.zeros_like(mesh.v)# Splat face normals to vertices
        vn.scatter_add_(0, i0[:, None].repeat(1, 3), face_normals)
        vn.scatter_add_(0, i1[:, None].repeat(1, 3), face_normals)
        vn.scatter_add_(0, i2[:, None].repeat(1, 3), face_normals)
        vn = torch.where(# Normalize, replace zero (degenerated) normals with some default value
            dot(vn, vn) > 1e-20,
            vn,
            torch.tensor([0.0, 0.0, 1.0], dtype=torch.float32, device=vn.device),
        )
        vn = safe_normalize(vn)
        mesh.vn = vn
        mesh.fn = mesh.f
        return (mesh,)

#-----------unrealized-----------

class vc_to_texture:#开发中
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh":("MESH",),
                "texture_w":("INT",{"default":512,min:32,max:4096,"step":64}),
                "texture_h":("INT",{"default":512,min:32,max:4096,"step":64}),
                },
            }
    CATEGORY = "3D_MeshTool/Edit"
    RETURN_TYPES = ("MESH","IMAGE")
    RETURN_NAMES = ("mesh","texture")
    FUNCTION = "vertex_color_to_texture"
    def vertex_color_to_texture(self,mesh,texture_w,texture_h):
        texture_width = 512
        texture_height = 512
        texture = torch.zeros((texture_h, texture_w, 3), dtype=torch.float32)
        uv_coords = mesh.ft.detach().cpu().numpy()
        vertex_colors = mesh.vc.detach().cpu().numpy()
        # 根据 UV 坐标为纹理赋值
        for i in range(uv_coords.shape[0]):
            u, v = uv_coords[i]
            texture[int(v * texture_h), int(u * texture_w)] = vertex_colors[i]
        #mesh.texture = texture
        return (mesh,texture,)

class mesh_remap_cubvh:#remap-UV-cubvh,Compilation required DLL
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh":("MESH",),
                "new_vertex":("LIST",),
                },
            }
    CATEGORY = "3D_MeshTool/Edit"
    RETURN_TYPES = ("MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "remap_uv"
    def remap_uv(self,mesh,new_vertex):
        """ remap uv texture (vt) to other surface.
        Args:
            v (torch.Tensor): the target mesh vertices, float [N, 3].
        """
        import cubvh
        assert mesh.vt is not None
        if mesh.v.shape[0] != mesh.vt.shape[0]:
            mesh.align_v_to_vt()
        BVH = cubvh.cuBVH(mesh.v, mesh.f)# find the closest face for each vertex
        dist, face_id, uvw = BVH.unsigned_distance(new_vertex, return_uvw=True)
        faces = mesh.f[face_id].long()# get original uv
        vt0 = mesh.vt[faces[:, 0]]
        vt1 = mesh.vt[faces[:, 1]]
        vt2 = mesh.vt[faces[:, 2]]
        mesh.vt = vt0 * uvw[:, 0:1] + vt1 * uvw[:, 1:2] + vt2 * uvw[:, 2:3]# calc new uv
        return (mesh,)
    #def align_v_to_vt(self, vmapping=None):

NODE_CLASS_MAPPINGS={
    "UnwrapUV_xatlas":UnwrapUV_xatlas,
    "UV_options":UV_options,
    "Auto_Normal":Auto_Normal,
    #"UnwrapUV_Auto_xatlas":UnwrapUV_Auto_xatlas,
    #"vc_to_texture":vc_to_texture,
    #"mesh_remap_cubvh":mesh_remap_cubvh,
    }
NODE_DISPLAY_NAMES_MAPPINGS={
    "UnwrapUV_xatlas":"UnwrapUV xatlas",
    "UV_options":"UV Options",
    "Auto_Normal":"Auto Normal",
    #"UnwrapUV_Auto_xatlas":"UnwrapUV Auto xatlas",
    #"vc_to_texture":"Vertex Color to Texture",
    #"mesh_remap_cubvh":"Remap UV Cubvh",
    }