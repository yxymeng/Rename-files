@echo off

echo 请输入你需要进行操作的序号
echo 1.重命名所有文件
echo 2.撤销重命名
set /p answer="请输入1或2 ："
if /i "%answer%"=="1" (
    Rename_Files.py
) else if /i "%answer%"=="2" (
    Undo_Renamed.py
)

pause
