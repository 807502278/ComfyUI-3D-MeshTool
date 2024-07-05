ComfyUI-3D-MeshTool explain

Introduction:
A simple 3D model processing tool within ComfyUI

Partially referenced from everyone's plugins, if there is any inconvenience, please leave a message, and I will promptly remove the corresponding code.
For new features or suggestions, please provide feedback.

Update:
2024-0705：
3d_meshtool
    Array #Arrays can perform batch operations on certain properties, such as the of zero123, image batches, creating certain increments, etc.
        basics #Create an array
            array1 step #Generate an array with a starting value and step size.
            array1 end increment #Generate an array with a starting value, end value, and increment.
            array1 end step #Generate an array with a starting value, end value, and step size.
            array1 step increment #Generate an array with a starting value, step size, and increment.
            string to array #Convert a string to an array, including standardized brackets/removing non-numeric functions.
        calculation
            array1 T #Transpose the array
            array1 number to angle #Convert array numbers to angles, including semi-angles.
            array1 append #Concatenate arrays, automatically determining 1D and 2D addition.
            array1 is null #Check if the array is empty.
            array1 attribute #Retrieve array attributes.
            array1 convert #Convert data types within the array.
            array1 select element #Select array elements, including standardized brackets/removing non-numeric functions.
    Basics
        load_obj #Load an OBJ file.
        mesh_data #Retrieve mesh data.
        mesh_data_statistics #Statistics of mesh data, other than vertices and faces, other data is used to determine if it is empty.
        mesh_clean_data #Clean mesh data, can customize the removal of invalid or mismatched data.
    Camera
        array1 to camposes #Convert an array to 3dpack camera poses (requires a 6xNx3 array, refer to 3dpack's campos standard).
    Edit
        unwrapUV_xatlas #Latest (2023) UV unwrapping algorithm.
        UV_options # Settings for the unwrapUV_xatlas node, if not connected, default settings are used.
        Auto_Normal #Automatically calculate model normals.
    Optimization
        mesh_optimization #Mesh optimization, select optimization types and parameters.
        mesh_cleanup #Mesh cleanup, select cleaning up model debris.
        mesh_subdivide #Mesh subdivision, increases vertices without changing the shape.
    Show

Roadmap:
Basic Functions
✅ Array sequence (still needs optimization)
✅ Data conversion (may need to add other conversions)
✅ OBJ import (used code from 3dpack, still need to add whether the model is normalized and its data output to retain the original size and position when processing models in batch)
🟩 Simple direct preview window (no need to save first) + preview window for world normals/depth/mask/specified view (can be used for compositing)
🟩 Save, choose which data to save
Model Optimization
✅ Remove debris
✅ Reduce faces by percentage (vertices)
✅ Cut subdivision
🟩 Turbine smoothing
🟩 Convert to quads
🟩 ... (other optimizations)
Model Editing
✅ UV decomposition (xatlas)
✅ Automatic vertex normals
🟩 UV remap
🟩 Restore normalized vertices to their original state
🟩 High-poly to low-poly texture/bump baking, AO baking (attempt to convert Blender's code to Comfyui)
🟩 ... (other edits)
other
🟩 Display any data.

简介：
一个简单的comfyui内的3D模型处理工具

部分参考了大家的插件，若有不便请留言，我将及时移除相应代码。
有新功能或建议，请反馈留言。

更新：
2024-0705：
3d_meshtool
    array #数组可以批量操作某些属性，如zero123的视角，图像批次，制作某些增量等。
        basics #生成数组
            array1 step #起始值+步长生成数组
            array1 end increment #起始值+末尾+增量生成数组
            array1 end step #起始值+末尾+步长生成数组
            array1 step increment #起始值+步长+增量生成数组
            string to array #字符串转数组，含规范括号/去除非数字等功能
        calculation
            array1 T #数组转置
            array1 number to angle #数组数字转角度，含半角
            array1 append #数组拼接，自动判断1维和2维附加
            array1 is null #判断数组是否为空
            array1 attribute #获取数组属性
            array1 connert #数组内的数据类型转换
            array1 select element #数组元素选择，含规范括号/去除非数字等功能
    basics
        load_obj #加载obj文件
        mesh_data #获取网格数据
        mesh_data_statistics #网格数据的统计，除顶点和面外，其他数据为判断是否为空
        mesh_clean_data #清理网格数据，可自定义去除无效或不匹配的数据
    camera
        array1 to camposes #将数组转换为3dpack的摄像机姿势（需输入6xNx3的数组，具体参考3dpack的campos规范）
    edit
        unwrapUV_xatlas #最新(2023)的UV展开算法
        UV_options # unwrapUV_xatlas节点的设置，如果不连接，则使用默认设置
        Auto_Normal #自动计算模型法线
    optimization
        mesh_optimization #网格优化，可选择优化类型和参数
        mesh_cleanup #网格清理，可选择清理模型碎块
        mesh_subdivide #网格切割细分，不改变外形仅增加顶点
    show

路线：

基础功能
✅array序列(还需要优化)
✅转换数据(可能需要增加其它转换)
✅OBJ导入(使用了3dpack的代码，还需要加入模型是否归一化和其数据输出以批量处理模型时保留原大小与位置)
🟩简单的直接预览窗口(不用先保存)+可输出世界法线/深度/遮罩/指定视角的预览窗口(可用于合成)
🟩保存,选择保存哪些数据
模型优化
✅移除碎块
✅按百分比(顶点)减面
✅切割细分
🟩涡轮平滑
🟩转四边面
🟩...(其它)
模型编辑
✅分解UV(xatlas)
✅自动顶点法线
🟩UV映射
🟩将归一化的顶点还原
🟩...(其它)
🟩高模到低模的纹理/法线烘焙，AO烘焙(尝试将blender的代码转换到comfyui)
其它
🟩显示任意数据
