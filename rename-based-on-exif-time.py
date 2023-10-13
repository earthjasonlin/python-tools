#############################################################
#               rename-based-on-exif-time.py                #
# Description: Batch modify file names in a folder based on #
#              the photo's capture time in EXIF metadata    #
# Author: earthjasonlin                                     #
# Created At: 2023-10-13                                    #
#############################################################
#                   INSATLL REQUIREMENTS                    #
#############################################################
# pip install pillow                                        #
#############################################################
#                          CONFIGS                          #
#############################################################
# folder_path: Files in this folder will be renamed         #
#              eg. D:/test                                  #
#############################################################

folder_path = ""

#############################################################

import os
import shutil
import time
from PIL import Image

# 获取当前文件夹下所有文件的文件名及扩展名
file_names = os.listdir(folder_path)

# 创建一个字典来存储每个拍摄时间对应的文件数
count_by_time = {}

# 循环遍历文件
for file_name in file_names:
    # 获取文件完整路径
    file_path = os.path.join(folder_path, file_name)
    # 判断是否是文件，如果是文件则进行操作
    if os.path.isfile(file_path):
        try:
            # 打开图片文件
            img = Image.open(file_path)
            # 获取EXIF信息
            exif_data = img._getexif()
            # 获取拍摄时间
            capture_time = exif_data[36867]
            # 将时间格式转换为带有年月日时分的格式
            time_str = time.strftime("%Y-%m-%d_%H-%M", time.strptime(capture_time, "%Y:%m:%d %H:%M:%S"))
            # 获取文件扩展名
            file_extension = os.path.splitext(file_name)[1]
            # 检查是否已经存在相同时间的文件
            if time_str in count_by_time:
                count_by_time[time_str] += 1
            else:
                count_by_time[time_str] = 1
            # 构建新的文件名，包括序号
            new_file_name = f"{time_str}_{count_by_time[time_str]}"
            # 构建新的文件路径
            new_file_path = os.path.join(folder_path, new_file_name + file_extension)
            # 关闭图片文件
            img.close()
            # 重命名文件
            os.rename(file_path, new_file_path)
            # 输出日志
            print(file_path + " -> " + new_file_path)
        except (AttributeError, KeyError, IndexError):
            # 如果无法获取拍摄时间，则跳过该文件
            print("Failed to get capture time for file:", file_path)
            continue
