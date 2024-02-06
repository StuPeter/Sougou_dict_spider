import os
import shutil

def merge_txt_files(directory, output_file):
    # 获取目录下的所有txt文件
    txt_files = [file for file in os.listdir(directory) if file.endswith('.txt')]

    # 打开输出文件
    with open(output_file, 'w') as output:
        # 遍历所有txt文件
        for file in txt_files:
            file_path = os.path.join(directory, file)
            # 打开当前txt文件并将内容写入输出文件
            with open(file_path, 'r') as input_file:
                shutil.copyfileobj(input_file, output)
            output.write('\n')  # 在每个文件的末尾添加换行符

    print("合并完成！")

# 指定目录和输出文件的路径
directory = 'txt1/'  # 替换为你的目录路径
output_file = 'output.txt'  # 替换为你的输出文件路径

# 调用函数进行合并
merge_txt_files(directory, output_file)
