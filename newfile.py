#GUI界面，暂未美化，自定义文件夹位置，自定义关键词，关键词组之间用英文";"分隔，排序按照关键词组顺序从001开始。
#关键词之间用空格间隔，每个关键词组里可以有一个或者无数个关键词，"并"语法，只有关键词组里所有的关键词都匹配到才会对其重命名。
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def is_already_renamed(filename):
    # 检查文件名是否包含序号
    return re.match(r'\d{3}\.', filename)

def rename_dwg_files(folder_path, keywords_groups, use_custom_rename):
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

def toggle_custom_rename():
    # 切换使用自定义重命名时的关键词输入框的显示状态
    if custom_rename_var.get():
        keywords_entry.pack()
    else:
        keywords_entry.pack_forget()
        keywords_entry.delete(0, tk.END)  # 清空输入框

def start_rename():
    # 获取用户输入的文件夹路径和关键词组
    path = folder_path.get()
    keywords_input = keywords_entry.get()
    use_custom_rename = custom_rename_var.get()

    # 如果使用自定义重命名，但未填写关键词，则给予提示
    if use_custom_rename and not keywords_input:
        messagebox.showwarning("警告", "使用自定义重命名时，请填写关键词。")
        return

    # 如果未使用自定义重命名，使用默认关键词组
    if not use_custom_rename:
        keywords_input = "侧围 骨架;底盘;电器;燃油"

    keywords_groups = [group.split() for group in keywords_input.split(';')]

    # 在这里调用你的函数
    rename_dwg_files(path, keywords_groups, use_custom_rename)
    messagebox.showinfo("成功", "文件已成功重命名！")

def browse_folder():
    folder_path.set(filedialog.askdirectory())

# GUI部分
root = tk.Tk()
root.title("DWG文件批量重命名工具")

font_style = ("Helvetica", 12)

# 文件夹路径部分
folder_label = tk.Label(root, text="文件夹路径:", font=font_style)
folder_path = tk.StringVar()
folder_entry = tk.Entry(root, textvariable=folder_path, font=font_style)
browse_button = tk.Button(root, text="浏览", command=browse_folder, font=font_style)

# 使用自定义重命名复选框
custom_rename_var = tk.BooleanVar()
custom_rename_var.set(False)  # 默认不勾选
custom_rename_checkbox = tk.Checkbutton(root, text="使用自定义重命名", variable=custom_rename_var, command=toggle_custom_rename, font=font_style)

# 清空关键词按钮
clear_keywords_button = tk.Button(root, text="清空关键词", command=lambda: keywords_entry.delete(0, tk.END), font=font_style)

# 关键词输入框部分
keywords_label = tk.Label(root, text="关键词组:", font=font_style)
keywords_entry = tk.Entry(root, font=font_style)

# 开始重命名按钮
rename_button = tk.Button(root, text="开始重命名", command=start_rename, font=font_style)

# 布局
folder_label.pack(pady=5)
folder_entry.pack(pady=5)
browse_button.pack(pady=10)
custom_rename_checkbox.pack(pady=5)
keywords_label.pack(pady=5)
keywords_entry.pack(pady=5, side=tk.LEFT)
clear_keywords_button.pack(pady=5, side=tk.RIGHT)
rename_button.pack(pady=10)

# 初始化时隐藏关键词输入框
toggle_custom_rename()

# 主循环
root.mainloop()
