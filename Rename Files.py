import os

def rename_files(folder_path, keywords):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    count = 1
    for file in files:
        if any(keyword in file for keyword in keywords):
            new_name = f"{count:03d}_{file}"
            try:
                os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name))
                count += 1
            except Exception as e:
                print(f"Error renaming file {file}: {e}")

# 获取当前脚本所在的文件夹路径
script_path = os.path.dirname(os.path.realpath(__file__))
# 使用当前脚本所在的文件夹作为文件夹路径
folder_path = script_path
# 请将下面的关键字替换成你需要的关键字列表
keywords = ["KEYWORD1", "KEYWORD2"]

rename_files(folder_path, keywords)
