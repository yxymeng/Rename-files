#GUI界面，暂未美化，自定义文件夹位置，自定义关键词，关键词组之间用英文";"分隔，排序按照关键词组顺序从001开始。
#关键词之间用空格间隔，每个关键词组里可以有一个或者无数个关键词，"并"语法，只有关键词组里所有的关键词都匹配到才会对其重命名。
import os
import re
import tkinter as tk
from tkinter import filedialog, simpledialog, ttk

DWG_EXTENSION = ".dwg"

def is_file_already_renamed(filename):
    return re.match(r'\d{3}\.', filename)

def get_dwg_files(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(DWG_EXTENSION)]

def update_progress(progress_var, current_progress, total_files):
    progress_var.set((current_progress / total_files) * 100)
    root.update_idletasks()

def show_warning(message):
    simpledialog.messagebox.showwarning("警告", message)

def rename_dwg_files(folder_path, keywords_groups, use_custom_rename, progress_var):
    files = get_dwg_files(folder_path)
    total_files = len(files) * len(keywords_groups)
    current_progress = 0

    for count, keywords_group in enumerate(keywords_groups, start=1):
        for file in files:
            if is_file_already_renamed(file):
                continue

            if all(re.search(keyword, file) for keyword in keywords_group):
                chinese_char_index = re.search('[\u4e00-\u9fa5]', file)
                if chinese_char_index:
                    new_name = "{:03d}. {}".format(count, file[chinese_char_index.start():])
                else:
                    new_name = "{:03d}. {}".format(count, file)

                base_name, extension = os.path.splitext(new_name)
                new_name_with_suffix = new_name
                suffix = 1
                while os.path.exists(os.path.join(folder_path, new_name_with_suffix)):
                    new_name_with_suffix = "{}_{:02d}{}".format(base_name, suffix, extension)
                    suffix += 1

                try:
                    os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name_with_suffix))
                except (FileNotFoundError, PermissionError, OSError) as e:
                    print(f"Error renaming file {file}: {str(e)}")

            current_progress += 1
            update_progress(progress_var, current_progress, total_files)

    progress_var.set(100)
    root.update_idletasks()
    simpledialog.messagebox.showinfo("成功", "文件已成功重命名！")

def toggle_custom_rename():
    if custom_rename_var.get():
        keywords_frame.pack()
    else:
        keywords_frame.pack_forget()
        keywords_entry.delete(0, tk.END)

def start_rename():
    path = folder_path.get()
    keywords_input = keywords_entry.get()
    use_custom_rename = custom_rename_var.get()

    if not path:
        show_warning("请选择一个文件夹。")
        return

    if use_custom_rename and not keywords_input:
        show_warning("使用自定义重命名时，请填写关键词。")
        return
    #设置默认关键词组，用英文的";"分隔关键词组，关键词直接用空格隔开，只有包含全部关键词的关键词组才会重命名。
    if not use_custom_rename:
        keywords_input = "侧围 骨架;底盘;电器;燃油"

    keywords_groups = [group.split() for group in keywords_input.split(';')]

    rename_dwg_files(path, keywords_groups, use_custom_rename, progress_var)

def browse_folder():
    folder_path.set(filedialog.askdirectory())

root = tk.Tk()
root.title("DWG文件批量重命名工具")

root.geometry("600x400")
font_style = ("Segoe UI", 12)

# 文件夹路径部分
folder_frame = tk.LabelFrame(root, text="文件夹路径", font=font_style)
folder_frame.pack(pady=10)

folder_label = tk.Label(folder_frame, text="文件夹路径:", font=font_style)
folder_path = tk.StringVar()
folder_entry = tk.Entry(folder_frame, textvariable=folder_path, font=font_style)
browse_button = tk.Button(folder_frame, text="浏览", command=browse_folder, font=font_style)

# 使用自定义重命名复选框
custom_rename_var = tk.BooleanVar()
custom_rename_var.set(False)  # 默认不勾选
custom_rename_checkbox = tk.Checkbutton(root, text="使用自定义重命名", variable=custom_rename_var, command=toggle_custom_rename, font=font_style)

# 关键词输入框部分
keywords_frame = tk.LabelFrame(root, text="关键词设置", font=font_style)

keywords_label = tk.Label(keywords_frame, text="关键词组:", font=font_style)
keywords_entry = tk.Entry(keywords_frame, font=font_style)
keywords_entry.insert(0, "用空格分隔关键词，用分号分隔关键词组")
keywords_entry.config(fg = "gray", width=35)

def on_entry_click(event):
    if keywords_entry.get() == "用空格分隔关键词，用分号分隔关键词组":
        keywords_entry.delete(0, "end") # delete all the text in the entry
        keywords_entry.insert(0, '') #Insert blank for user input
        keywords_entry.config(fg = "black")

def on_focusout(event):
    if keywords_entry.get() == '':
        keywords_entry.insert(0, '用空格分隔关键词，用分号分隔关键词组')
        keywords_entry.config(fg = "gray")

keywords_entry.bind('<Key>', on_entry_click)  # change '<FocusIn>' to '<Key>'
keywords_entry.bind('<FocusOut>', on_focusout)

# 清除关键词按钮
clear_button = tk.Button(keywords_frame, text="清除关键词", command=lambda: keywords_entry.delete(0, tk.END), font=font_style)

# 开始重命名按钮
rename_button = tk.Button(root, text="开始重命名", command=start_rename, font=font_style)

# 进度条
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, length=300, variable=progress_var)

# 布局
folder_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
browse_button.grid(row=0, column=2, padx=5, pady=5)
custom_rename_checkbox.pack(pady=10)
keywords_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
keywords_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
clear_button.grid(row=0, column=2, padx=5, pady=5)
rename_button.pack(pady=10)
progress_bar.pack(pady=10)

root.mainloop()
