import os
import glob

def merge_txt_files(directory, output_file):
    with open(output_file, 'w') as outfile:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())

# 指定目录和输出文件名
directory = 'txt1'
output_file = 'output.txt'

# 调用函数进行整合
merge_txt_files(directory, output_file)
