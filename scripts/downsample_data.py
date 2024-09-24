import shutil
import random


def downsample_data(input_file, output_file, sample_ratio):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    # 计算保留的样本数量
    sample_size = int(len(lines) * sample_ratio)
    # 随机选择样本
    sampled_lines = random.sample(lines, sample_size)
    # 写入输出文件
    with open(output_file, 'w') as f:
        f.writelines(sampled_lines)

if __name__ == '__main__':
    # 输入文件、输出文件以及保留比例
    input_file = 'rrl-DM_HW/dataset/bank-marketing-wo-scaled.data'
    output_file = 'rrl-DM_HW/dataset/bank-marketing-wo-scaled.downsample.data'
    sample_ratio = 0.01

    shutil.copy('rrl-DM_HW/dataset/bank-marketing-wo-scaled.info', 'rrl-DM_HW/dataset/bank-marketing-wo-scaled.downsample.info')

    downsample_data(input_file, output_file, sample_ratio)

    input_file = 'rrl-DM_HW/dataset/bank-marketing-wo-scaled.data'
    output_file = 'rrl-DM_HW/dataset/bank-marketing-wo-scaled.manual.data'
    sample_ratio = 0.0002
    
    downsample_data(input_file, output_file, sample_ratio)
