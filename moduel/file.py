import os

def move_file(path,to_path,cover=True):#移动文件，可选是否覆盖
    if not os.path.exists(path):print(f"error(move_file): not found {path}")
    else:
        try:
            os.rename(path,to_path)
        except FileExistsError:# 如果目标位置已有同名文件，先删除再移动
            if cover:
                os.remove(to_path)
                os.rename(path,to_path)
            else:print("Warning: The file overwrite is not set, but there is an existing file with the same name.")

def cache_number(path,num):#控制文件夹内文件数量，用于清除旧文件缓存
    if not os.path.exists(path):print(f"error(cache_number): not found {path}")
    else:
        files=os.listdir(path)
        if len(files)>num:
            for file in files[:-num]:
                 os.remove(os.path.join(path,file))

def split_path(input_path):#分割路径，返回[目录路径，文件名，文件扩展名，文件全名]
    if os.path.isfile(input_path):
        dir_path, file_full_name = os.path.split(input_path)
        file_name, file_extension = os.path.splitext(file_full_name)
        return [dir_path, file_name, file_extension, file_full_name]
    elif os.path.isdir(input_path):
        return [input_path, None, None, None]
    else:
        file_name, file_extension = os.path.splitext(input_path)
        if file_extension:
            return [None, os.path.splitext(input_path)[0], file_extension, input_path]
        else:
            return [None, None, None, None]