import torch

class setmeshdata:#待开发
    def __init__(self):
        pass
    @classmethod
    def name(cls, mesh, name):
        mesh.name = name
    @classmethod
    def f(cls, mesh, f):
        mesh.f = f

class meshclean:
    def __init__(self):
        pass
    @classmethod
    def revf3(cls, mesh):#用于增删顶点/面后清除不匹配的法线/UV/顶点色
        mesh.fn=None;mesh.fv=None;mesh.ft=None
        mesh.vn=None;mesh.vt=None;mesh.ft=None

class meshtexturing:
    def __init__(self):
        pass
    @classmethod
    def vctotexture(vertex_colors, uv_coords, texture_size=(256, 256)):#顶点色到纹理(待测试)
        # 将 UV 坐标归一化到 [0, texture_size - 1] 范围内
        uv_coords = uv_coords * torch.tensor([texture_size[0] - 1, texture_size[1] - 1], dtype=torch.float32)
        # 处理边界情况
        uv_coords = torch.clamp(uv_coords, 0, torch.tensor([texture_size[0] - 1, texture_size[1] - 1], dtype=torch.float32))
        # 初始化纹理
        texture = torch.zeros((texture_size[1], texture_size[0], 3), dtype=torch.float32)
        # 双线性插值计算纹理颜色
        u_floor = torch.floor(uv_coords[:, 0]).long()
        v_floor = torch.floor(uv_coords[:, 1]).long()
        u_ceil = torch.ceil(uv_coords[:, 0]).long()
        v_ceil = torch.ceil(uv_coords[:, 1]).long()
        u_weight = uv_coords[:, 0] - u_floor
        v_weight = uv_coords[:, 1] - v_floor
        for i in range(len(uv_coords)):
            # 四个相邻点的颜色
            color00 = vertex_colors[i]
            color01 = vertex_colors[i] if v_ceil[i] < texture_size[1] else color00
            color10 = vertex_colors[i] if u_ceil[i] < texture_size[0] else color00
            color11 = vertex_colors[i] if (u_ceil[i] < texture_size[0] and v_ceil[i] < texture_size[1]) else color00
            # 双线性插值
            texture[v_floor[i], u_floor[i]] += (1 - u_weight[i]) * (1 - v_weight[i]) * color00
            texture[v_floor[i], u_ceil[i]] += u_weight[i] * (1 - v_weight[i]) * color10
            texture[v_ceil[i], u_floor[i]] += (1 - u_weight[i]) * v_weight[i] * color01
            texture[v_ceil[i], u_ceil[i]] += u_weight[i] * v_weight[i] * color11
        return texture
    
    @classmethod
    def UVmapping(cls,mesh,vt1,vt2):#UV映射(待开发)
        pass