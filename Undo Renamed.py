import os

def remove_prefixes(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file in files:
        if ". " in file:
            new_name = file[file.index(". ")+2:]
            os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name))

# 获取当前脚本所在的文件夹路径
script_path = os.path.dirname(os.path.realpath(__file__))
# 使用当前脚本所在的文件夹作为文件夹路径
folder_path = script_path

remove_prefixes(folder_path)
