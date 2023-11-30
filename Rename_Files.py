import os
import re

def rename_dwg_files(folder_path, keywords):
    # 获取文件夹下的所有dwg文件，也可以其他的
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(".dwg")]

    for count, keyword in enumerate(keywords, start=1):
        for file in files:
            # 使用正则表达式匹配关键字
            match = re.search(keyword, file)
            if match:
                # 找到第一个中文字符的索引
                chinese_char_index = re.search('[\u4e00-\u9fa5]', file)
                if chinese_char_index:
                    # 删除序号和空格之前的内容
                    new_name = "{:03d}. {}".format(count, file[chinese_char_index.start():])
                else:
                    # 如果文件名中没有中文字符，则不进行删除
                    new_name = "{:03d}. {}".format(count, file)

                # 处理文件名冲突
                base_name, extension = os.path.splitext(new_name)
                new_name_with_suffix = new_name
                suffix = 1

                while os.path.exists(os.path.join(folder_path, new_name_with_suffix)):
                    new_name_with_suffix = "{}_{:02d}{}".format(base_name, suffix, extension)
                    suffix += 1

                try:
                    # 重命名文件
                    os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name_with_suffix))
                except Exception as e:
                    print(f"Error renaming file {file}: {e}")

# 获取当前脚本所在的文件夹路径
script_path = os.path.dirname(os.path.realpath(__file__))
# 使用当前脚本所在的文件夹作为文件夹路径
folder_path = script_path
# 请将下面的关键字替换成你需要的关键字列表，并按照希望的顺序排列，可以无数个
keywords = ["KEYWORD1", "KEYWORD2", "KEYWORD3", "KEYWORD4"]

rename_dwg_files(folder_path, keywords)
