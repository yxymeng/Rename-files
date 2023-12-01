import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
def is_already_renamed(filename):
    # 检查文件名是否包含序号
    return re.match(r'\d{3}\.', filename)
def rename_dwg_files(folder_path, keywords_groups):
    # 获取文件夹下的所有dwg文件，也可以其他的
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(".dwg")]
    for count, keywords_group in enumerate(keywords_groups, start=1):
        for file in files:
            # 检查文件是否已经重命名
            if is_already_renamed(file):
                continue
            # 检查文件名是否包含关键词组中的所有关键词
            if all(re.search(keyword, file) for keyword in keywords_group):
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
def browse_folder():
    folder_path.set(filedialog.askdirectory())
def submit():
    # 获取用户输入的文件夹路径和关键词组
    path = folder_path.get()
    keywords_groups = [group.split() for group in keywords_entry.get().split(';')]
    # 在这里调用你的函数
    rename_dwg_files(path, keywords_groups)
    messagebox.showinfo("成功", "文件已成功重命名！")
root = tk.Tk()
folder_path = tk.StringVar()
keywords_entry = tk.Entry(root)
browse_button = tk.Button(root, text="浏览", command=browse_folder)
submit_button = tk.Button(root, text="提交", command=submit)
folder_entry = tk.Entry(root, textvariable=folder_path)
folder_entry.pack()
browse_button.pack()
keywords_entry.pack()
submit_button.pack()
root.mainloop()
# 获取当前脚本所在的文件夹路径
#script_path = os.path.dirname(os.path.realpath(__file__))
# 使用当前脚本所在的文件夹作为文件夹路径
#folder_path = script_path
# 请将下面的关键字替换成你需要的关键字列表，并按照希望的顺序排列
#keywords = ["侧围", "底盘", "燃油", "顶盖", "踏步", "外饰"]
#rename_dwg_files(folder_path, keywords)
