import os

# 指定文件夹路径和输出文件路径
folder_path = 'path/to/file.txt'  # 替换为你的文件夹路径
output_file = 'path/to/output.txt'  # 替换为你的输出文件路径

def concatenate_txt_files(folder_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as output:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                        output.write(file_content)
                        output.write('\n')  # 在文件之间添加换行符

    print("Concatenation completed.")

# 调用函数进行拼接
concatenate_txt_files(folder_path, output_file)
