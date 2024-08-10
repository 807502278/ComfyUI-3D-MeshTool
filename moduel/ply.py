import numpy as np
import os
from plyfile import PlyData , PlyElement
from .file import move_file

"""
    **********ply说明**********
    提供comfyui-3d-pack标准的ply文件导入和简单编辑
    1:导入xyz/color数据的ply文件,
    2:导入xyz/color数据的txt文件,颜色映射/坐标处理(待开发)
    3:保存/缓存ply文件
    Provide standard PLY file import and simple editing for ComfyUI-3D-PACK.
    1: Import PLY files that only contain xyz/color data.
    2: Import TXT files that only contain xyz/color data, with color mapping/coordinate processing.
    3: Save/cache PLY files.
"""
#----------------------------cls----------------------------

class ply_options:
    """comfyui-3d-pack标准ply文件所需的属性以及默认值"""
    standard_options={#ply_options为comfyui-3d-pack标准ply文件所需的属性以及默认值，可根据需变动自行修改
            "x":0.0,"y":0.0,"z":0.0,                #坐标,范围约-1~1
            "nx":0.0,"ny":0.0,"nz":0.0,             #法向量
            "f_dc_0":0.0, "f_dc_1":0.0,"f_dc_2":0.0,#颜色,精确范围-1.77~1.77
            "opacity":3.0,                          #透明度,范围约-5~3
            "scale_0":-6.0,"scale_1":-6.0,"scale_2":-6.0,#缩放,范围约-2~-12
            "rot_0":0.0,"rot_1":0.0,"rot_2":0.0,"rot_3":1.0#旋转
            }
    type_mapping = {
            'e': 'float16',
            'f4': 'float32',
            'f': 'float32',
            'f8': 'float64',
            'd': 'float64',
            'i1': 'int8',
            'i2': 'int16',
            'i4': 'int32',
            'i': 'int32',
            'i8': 'int64',
            'l': 'int64',
            'u1': 'uint8',
            'uchar': 'uint8',
            'u2': 'uint16',
            'u4': 'uint32',
            'u8': 'uint64',
            'b': 'bool',
            's': 'char',
            }
    def __init__(self):
        self.options=self.standard_options.copy()#标准属性列表
        self.dtype=None
        self.init_type()#初始化dtype
        
    def init_type(self,type=None):#初始化dtype
        """初始化dtype"""
        key1=dict();typename=None
        if type==None : type="f4" #没有指定类型则全部默认"f4"
        if isinstance(type,str): #如果指定一个类型
            if type in self.type_mapping.keys():typename=self.type_mapping[type]#如果是类缩写则转化为类名
            if type in self.type_mapping.values():typename=type
            if typename!=None:
                for key,value in self.options.items():
                    key1[key]=type
                    self.options[key] = np.dtype(typename).type(value)#转换.options内的数据类型
                self.dtype = list(key1.items())
            else:print("Error(ply_options_dtype): Unrecognized class/class abbreviation entered")
        elif isinstance(type,dict):#指定类型，待开发
            pass
        else:print("Error(ply_options_dtype): During initialization, the type can only be str")

    def init_value(self,init=False,dict1=None):
        """重置ply_options为None,init为初始化,若dict1不为None则更新ply_options"""
        if init:
            for i in ["x","y","z"]:self.options[i]=None
        else:
            for i in self.options : self.options[i] = None
        if dict1 != None :#自定义属性(待开发)
            self.options=dict1

    #------------------(待开发)
        #def setvalue(self,k_value):
        #    """输入字典，设置指定属性的值"""
        #    if type(k_value)==dict:
        #        if set(self.options.keys())==set(self.options.keys()):
        #            if type(k_value.values()[0]) in [str,int,float]:
        #                self.options=k_value.items()
        #            return self.options


class xyz:
    """
    --------xyz/rgb数据类操作--------
    """
    def __init__(self,xyz_data):
        self.xyz_data=xyz_data
        self.xyz_data=self.detector()                   #坐标数据
        self.xyz_min, self.xyz_max = self.pos_m()       #坐标最值范围
        self.xyz_center , self.xyz_scale = self.center()#当前坐标

        self.o_xyz_min = self.xyz_min 
        self.o_xyz_max = self.xyz_max       #原最值，用于获取原始大小信息
        self.o_xyz_center = self.xyz_center #原坐标，用于获取原始位置
        self.o_xyz_size = np.linalg.norm(self.xyz_max-self.xyz_min)   #原大小，用于获取原始大小信息

        #self.k_renew=True #是否在数据修改后马上更新数据，防止数据过多时精简不必要的计算--待开发--
        self.k_history=True #是否打开移动旋转缩放的历史记录，目前历史数据仅记录1次
        self.xyz_center0 = None #坐标记录，xyz_data减去此坐标后 恢复原位
        self.xyz_scale0 = None #缩放记录，xyz_data 乘此值的倒数后 恢复原大小

    #-----------re-----------
    def __re_minmax__(self):#更新最值坐标
        self.xyz_min, self.xyz_max = self.pos_m()
    def __re_transform__(self,center=False,scale=False,center0=None,scale0=None):#选择更新位置数据
        if center or scale: transform=self.center()
        if center: self.xyz_center = transform[0]
        if scale: self.xyz_scale = transform[1]
        if center0 is not None and self.k_history: self.xyz_center0 = center0
        if scale0 is not None and self.k_history: self.xyz_scale0 = scale0

    #-----------get-----------
    def detector(self):#检查xyz数据格式
        if type(self.xyz_data)==list:
            self.xyz_data=np.array(self.xyz_data)
        if type(self.xyz_data)==np.ndarray:
            if len(self.xyz_data.shape)==2:
                if self.xyz_data.shape[1]==3: 
                    self.xyz_data=np.array([self.xyz_data["vertex"]["x"],
                                            self.xyz_data["vertex"]["y"],
                                            self.xyz_data["vertex"]["z"]]).T
                if self.xyz_data.shape[0]==3: return self.xyz_data
                else:
                    print("Error(xyz_normalize):The input data should be an array of 3 x N or N x 3")#某一维度不为3
                    return None
            else:
                print("Error(xyz_normalize):The dimension of the input array should be 2")#维度错误
                return None
        else:
            print("Error(xyz_normalize):The input data type should be a 2D array")#数据类型错误
            return None

    def pos_m(self):#计算xyz的最小值最大值
        min_pos , max_pos = np.array([]) , np.array([])
        for i in self.xyz_data:
            min_pos=np.append(min_pos,np.min(i))
            max_pos=np.append(max_pos,np.max(i))
        return min_pos[:,np.newaxis],max_pos[:,np.newaxis]#增加1个维度以广播到任意长度

    def center(self):#计算中心坐标和大小
        m1=self.pos_m()
        center=(m1[0]+m1[1])/2
        scale=np.max(self.xyz_max)-np.min(self.xyz_min)
        return center,scale

    #-----------edit-----------
    def move(self,pos=[0,0,0]):#移至指定坐标
        if isinstance(pos,list):pos=np.array(pos)
        if isinstance(pos,np.ndarray):
            if pos.shape==(3,): pos=pos[:,np.newaxis]
            center=pos-self.xyz_center
            self.xyz_data=self.xyz_data + center
            self.__re_minmax__()
            self.__re_transform__(center=True,scale=True,center0=center)#更新位置数据

        else:print("Error(xyz_move): Cannot support input data type, requires an array type xyz coordinate")

    def scale(self,scale=1.0):#以原点为中心缩放到指定尺寸
        v=np.max(self.xyz_max)-np.min(self.xyz_min)
        scale=scale/self.xyz_scale#缩放比例
        self.xyz_data=self.xyz_data*scale
        self.__re_minmax__()
        self.__re_transform__(center=True,scale=True)#更新缩放数据

    def lin_mapping(self,data=None,min=-1.77,max=1.77):#线性映射,默认将颜色映射到标准ply范围(xyz对应rgb)---暂无历史记录，需重构
        if data == None:data=self.xyz_data
        self.xyz_data = min + (self.xyz_data - self.xyz_min) * (max - min) / (self.xyz_max - self.xyz_min)
        self.__re_minmax__()
        self.__re_transform__(scale=True,scale0=1.0/self.xyz_scale)#更新缩放数据

    def rotate_to(self,rotate=[0,0,0]):#旋转到指定角度---------------待开发---------------
        pass

    #-----------组合操作-----------
    def normalize(self):#移动到原点，缩放到单位1大小
        self.move()#使用默认值移动到0点
        self.scale()#使用默认值缩放到范围1内
    
    def reduction(self,data=None):#按历史记录还原先还原缩放再还原位置,一般还原最终结果(还原obj的xyz)---------------待开发---------------
        pass

class ply1:#新建comfyui-3d-pack标准ply，set方法
    def __init__(self):
        cls_options=ply_options()
        #cls_options.init_value()

        self.e=["vertex","face"]        #元素列表
        self.options=cls_options.options#dict属性列表的默认值字典
        self.dtype=cls_options.dtype    #list属性dtype
        self.filepath=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.plydata=None               #ply数据
        self.new()                      #新建标准ply(2个在原点的点)
        
    def _re_dtype(self):#更新dtype
        self.dtype=self.plydata[self.e[0]][0].dtype.descr

    #------------standard------------

    def to_ply(self,plydata1,e=0):#将list/numpy数组转为plydata,to_ply为True时返回ply,否则返回numpy数组
        if type(plydata1)==np.ndarray:
            to_plydata=PlyElement.describe(plydata1,self.e[e])
            self.plydata=PlyData([to_plydata])#np.array转PlyData
            return True
        if type(plydata1)==PlyElement:
            self.plydata=PlyData([plydata1])  #PlyElement转PlyData                 
            return True
        if type(plydata1)==PlyData:
            self.plydata=plydata1
            return True
        else:
            print("Error(ply_convert_plydata): input data type not supported")
            return False

    def new(self,length=2,options=None,dtype=None,e=0):#新建plydata,length为数据数量,keys为属性列表数组,type为属性类型数组(需重构)
        if options==None: options=self.options
        if dtype==None: dtype=self.dtype
        if set(options.keys())==set(np.array(dtype)[:,0]):
            new_ply=np.array(np.zeros((length)),dtype=dtype)
            self.to_ply(new_ply,e)
            for k,v in options.items():#初始值赋值
                self.plydata[self.e[e]][k]=v



    def is_standard(self,e=0):#判断plydata是否为标准plydata(暂未使用)
        if type(self.plydata)==PlyData:
            default_list=list(ply_options.keys())
            element_list=self.plydata[self.e[e]].data.dtype.names#获取plydata的属性列表
            if set(default_list).issubset(set(element_list)):
                return True
            else:return False
        else:return False

    #------------set------------
    def setvalue(self,new_value,plydata1=None,e=0,new_items=True):
        """
        输入字典设置ply数据,
        relen=True 长度不同时重置ply到合适的长度(会删除原数据,临时使用,待开发自动增加长度后relen值将取消)
        """
        if plydata1 is None: plydata1=self.plydata
        if type(plydata1) == PlyData:
            if isinstance(new_value,dict):
                none_value=dict()
                len0=2
                type_list=(list,tuple,np.ndarray,dict,np.memmap)
                for value in new_value.values():
                    if type(value) in type_list:
                        len0=(len(value)) ; break#获取输入数据new_value的长度
                len1=plydata1[self.e[e]].count
                if len1 != len0:#是否与原数据长度相同
                    self.new(len0)
                    plydata1=self.plydata
                    if len0==2:
                        print(f"Prompt(ply1_set): The original data is empty, and a new data with a length of {len0} has been created")
                    else:
                        print("Warning(ply1_set): The length of the input data is different from the current data. ")
                        print(f"   -The original data has been cleared and a data with a length of {len0} has been created")
                if new_items:#如果new_items=True，且输入的new_value有新属性，则有新key时增加新属性到plydata
                    for key,value in new_value.items():#遍历options赋值
                        if type(value) in type_list:
                            pass#跳过列表类型，避免遍历到值类型的时候报错
                        elif value == None: continue#跳过None值
                        if not key in self.options.keys(): none_value[key]=value#统计非标准属性
                        plydata1[self.e[e]][key] = value#如果输入的属性名在标准属性列表中则给新plydata赋值
                else:
                    for key,value in new_value.items():#遍历options赋值
                        if type(value) in type_list:
                            pass
                        elif value == None: continue
                        if not key in self.options.keys(): none_value[key]=value#统计非标准属性
                        else:plydata1[self.e[e]][key] = value#如果输入的属性名在标准属性列表中则给新plydata赋值
                if len(none_value)>0:print(f"warning(ply1_set): \n{none_value.keys()} \nThese attributes are non-standard and will be discarded!")
                self.plydata=plydata1
                return plydata1
            else:
                print("Error(ply1_set): The method setvalue-new_value must input a dictionary")
                return None
        else:
            print("Error(ply1_set): The method setvalue-plydata1 must input a PlyData object")
            return None

    def save(self,plydata=None,path=None,filename=None,ascii=False):#保存ply，若不输入路径则保存在默认缓存文件夹
        if plydata==None:plydata=self.plydata
        if filename==None:filename="ply_cache.ply" #保存文件名
        self.plydata.text=ascii
        self.plydata.write(filename)#如果debug测试开关为False则保存文件(貌似只能保存在当前父包路径)
        if path==None:#如果不输入路径则保存在默认缓存文件夹
            path=self.filepath
            path=os.path.join(path,"cache\ply_cache.ply")
        move_file(os.path.join(self.filepath,filename),path)#文件移动到指定路径覆盖保存
        return path


    #------------(待开发)
        #def ply_setplydata(get_a,set_b,*key,e="vertex"):#set ply数据
        #    error_key=[]
        #    set_key=[]
        #    if type(set_b)!=PlyData:
        #        print("Error(ply_set_data): set_b must be a PlyData object")
        #        return None
        #    if type(get_a)!=PlyData:
        #        print("Error(ply_set_data): get_a must be a PlyData object")
        #        return None
        #    if len(key)==0:
        #        print("Error(ply_set_data): no key input")
        #        return None
        #    key_name = set_b[e].data.dtype.names
        #    for i in key:
        #        if i in key_name : set_key.append(i)
        #        else : error_key.append(i)
        #    if len(error_key)==len(key):
        #        print("warning(ply_set_data): no key in the set_b element")
        #        return None
        #    for i in set_key:
        #        set_b[e][i]=get_a[e][i]
        #    if len(error_key)>0:print(f"warning(ply_set_data): \n{error_key} \nThese keys are not in the {e} element and will be discarded!")
        #    return set_b

        #def normalize(self,e_n=0):#增加3dpack ply所需的属性,使下载的ply能在3dpack中加载
        #    if type(self.plydata)!=PlyData: self.to_ply(self.plydata,e_n=e_n)
        #    default_list=list(ply_options.keys())
        #    element_list=self.plydata[self.e[e_n]].data.dtype.names#获取plydata的属性列表
        #    if not set(default_list).issubset(set(element_list)):#如果plydata不为标准plydata则标准化
        #        vertex = self.new(length=len(self.plydata[self.e[e_n]].data),keys=default_list)
        #        error_list=[]
        #        if type(self.plydata)==PlyData:
        #            for i in default_list:
        #                if i in element_list: vertex[i] = a['vertex'][i]
        #                else:error_list.append(i)#统计非标准属性
        #            if len(error_list)>0:print(f"warning(ply_normalize): \n{error_list} \nThese attributes are non-standard and will be discarded!")

#----------------------------def----------------------------
def point_edit(ply,keys):#编辑点云的点属性，目前支持点的大小/交换颜色/
    pass

class ply2:#编辑输入的ply-------------------待开发
    def __init__(self,plydata:PlyData):
        self.plydata=plydata


def getvalue(plydata:PlyData,key,e="vertex"):#获取plydata的属性值
    if type(key)==str : return [plydata[e][key]]
    elif type(key) in (list,tuple):
        type_list=plydata[e].data.dtype.names
        z_list=set(key) & set(type_list)
        e_list=set(key) - z_list
        data = [[]] * len(z_list)
        for i in range(len(z_list)):
            data[i]=plydata[e][list(z_list)[i]]
        if len(e_list)>0:print(f"warning(ply_get): \n{e_list} \nThese attributes are not in the current plydata")
        return data

def addkey(data,key):#将数组增加标签，返回字典
    type_list=(list,tuple,np.array,np.ndarray)
    if type(data) in type_list and type(key) in type_list:
        if len(data)==len(key):
            d=dict()
            for i in range(len(key)):
                d[key[i]]=data[i]
            return d
        else:
            print("Error(ply_get_value): The length of the input data is not the same as the current data")
            return None
    else:
        print("Error(ply_get_value): The input key must be a string or a list/tuple/numpy array")
        return None

def ply_debug(a,depth=1):
    if depth==1:
        print(f"数据数量:{len(a.elements)}")
        for i in range(len(a.elements)):
            print(a.elements[i])
    if depth==2:
        for i in range(len(a.elements)):
            print(a.elements[i])
            for j in range(len(a.elements[i])):
                print(a.elements[i][j])
    if depth==3:#查看plydata的元素属性列表
        print("------------")
        print(dir(a.elements[0]))
        str1=['comments', 'count', 'data', 'describe', 'dtype', 'header', 'name', 'ply_property', 'properties']
        for i in str1:
            print(f"属性：{i}")
            exec("print(a.elements[0]."+i+")")
            print("------------")

def sdir (obj):#自动打印对象的可调用方法名+返回类型+值
    list1=[];j=0
    for i in dir(obj):
        if not i.startswith('_'):list1.append(i)
    print("------------------------start dir------------------------")
    print(f"current object:{str(obj)}")
    print("---------------------------------------------------------")
    for i in list1:
        j += 1
        print(f"属性{j}:{i}")
        exec("print(f'类型名：{type(obj."+i+")}')")
        exec("print(f'属性值：{obj."+i+"}')")
        if j<len(list1):print(f"------------")
    print("------------------------end dir------------------------")

#----------------------------test----------------------------

def h_ply(path=None):#处理ply数据示例

    #准备ply数据
    if path==None: path=r"D:\AI\ComfyUI-3D\ComfyUI\custom_nodes\ComfyUI-3D-MeshTool\other\test\output_20240801B.ply"
    f=PlyData.read(path)
    a=ply1()#新建标准ply类

    #处理原ply坐标
    xyz_k=["x","y","z"]
    xyz_d=getvalue(f,xyz_k)#获取原ply的xyz
    xyz1=xyz(xyz_d)    #创建xyz类
    xyz1.normalize()   #归一化
    data=addkey(xyz1.xyz_data,xyz_k)#添加键值对
    a.setvalue(data)   #更新ply数据

    #处理原ply颜色
    rgb_k=["red","green","blue"]
    rgb_d=getvalue(f,rgb_k)#获取原ply的rgb
    rgb1=xyz(rgb_d)       #创建xyz类
    rgb1.lin_mapping()    #颜色映射
    rgb_k=["f_dc_0","f_dc_1","f_dc_2"]
    data=addkey(rgb1.xyz_data,rgb_k)#添加键值对
    a.setvalue(data)   #更新ply数据
    
    #转移原透明度
    opacity_k=["scalar_Intensity"]
    opacity_d=getvalue(f,opacity_k)#获取原ply的opacity
    opacity_k=["opacity"]
    data=addkey(opacity_d,opacity_k)#添加键值对
    a.setvalue(data)   #更新ply数据

    #print(a.plydata["vertex"].data)
    a.save()#保存ply文件,默认覆盖保存到缓存文件夹

    return a.plydata

"""
    **********plyfile read**********
    b.elements[0] #第1个PlyData元素,一般为vertex(此时与(b['vertex'])等效)
    b.elements[1] #第2个PlyData元素,一般为face
    b['vertex']   #vertex属性列表,若无vertex属性则触发PlyParseError

    **********plyfile set/get**********
    b['vertex'][0] #vertex的所有第1列(也是第1个key)的数据
    b["vertex"][0]['x'] #第一个vertex的x坐标
    b["vertex"]['x'] #所有vertex的x坐标
    b["vertex"].data #所有vertex数据
    b["vertex"].count #数据数量

    dtype属性列表(list可用类型) b["vertex"][0].dtype.descr = [('x', '<f8'), ('y', '<f8'), ('z', '<f8'),...]
    属性名列表   (可读写) b["vertex"].data.dtype.names 更改后data数组不受影响(注意顺序即可)
    第n组数据的类型(只读) b.["vertex"][0][n].dtype

    注释列表(与属性名顺序对应的字符串列表) b.comments 更改后其它数据不受影响
    保存ascii与binary格式(布尔值) plydata.text
    对象信息,包括文件名、作者、创建日期、对象描述等 plydata.obj_info

    **********plyfile case to**********
     np.ndarray,不支持set实例的name,否则会引发错误,建议使用新的np.ndarray转换为PlyElement
     plyfile.PlyElement:el = PlyElement.describe(np1,'vertex',comments=['explanatory note1','explanatory note2'])  comments为属性注释,可选
     plyfile.PlyData:ply = PlyData([el], comments=['header comment']) comments为元素注释,可选

    **********plyfile debug**********
    只读查看plydata属性列表(含byte_order): b["vertex"].data.dtype

    缩写与全称在dtype中内完全相同
    半精度浮点 float16 e            占用16-bit 范围6.1035156e-05~65504.0            有效数字: 4
    全精度浮点 float32 f4 f:         占用32-bit 范围1.175494351e-38~3.402823466e+38 有效数字: 7
    双精度浮点 float64 (double)f8 d : 占用64-bit 范围2.2250738585072014e-308~1.7976931348623157e+308 有效数字: 15
    整数 int8 i1    占用8-bit  范围-128~127
    整数 int16 i2   占用16-bit 范围-32768~32767
    整数 int32 i4 i 占用32-bit 范围-2147483648~2147483647
    整数 int64 i8 l 占用64-bit 范围-9223372036854775808~9223372036854775807
    无符号整数 uint8 uchar u1 占用8-bit 范围0~255
    无符号整数 uint16 u2 占用16-bit    范围0~65535
    无符号整数 uint32 u4 占用32-bit   范围0~4294967295
    无符号整数 uint64 u8 占用64-bit  范围0~18446744073709551615
    布尔 bool b     占用1-bit  范围False,True
    字符 char c    
    字符串 string s   固定长度的字符串: s20
"""