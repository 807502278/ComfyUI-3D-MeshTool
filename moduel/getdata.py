import os
import json

"""
Load files and read data through keys or items
加载文件,通过key或item读取数据
"""

def read_file(file_path,key=None):
    with open(file_path, 'r') as f:
        data = json.loads(f.read())
    if key is None:
        return data
    elif isinstance(key, (str,int)):
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

print(read_file(r"D:\Project\Work_2024\AIGC-24-0918CameraTracking\py\Task-of-2024-09-20T015106902Z-shots.geojson",
                {'features':0}))