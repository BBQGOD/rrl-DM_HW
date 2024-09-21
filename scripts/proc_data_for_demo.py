import csv
import sys

SRC_PATH = sys.argv[1]
LABEL_PATH = sys.argv[2]
TGT_NAME = sys.argv[3]

def is_continuous_column(column):
    """
    判断一列是否为连续字段（数值类型），若所有值均为数值，则认为是连续字段。
    """
    try:
        # 尝试将所有元素转换为浮点数，若成功则认为该列为连续字段
        [float(value) for value in column]
        return True
    except ValueError:
        return False

def convert_csv_to_data_info(feature_file, label_file, output_name):
    # 打开特征CSV文件
    with open(feature_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # 读取特征表头
        feature_rows = list(reader)  # 读取特征数据行

    # 打开标签CSV文件
    with open(label_file, 'r') as f:
        reader = csv.reader(f)
        y_header = next(reader)[0]  # 读取标签表头
        labels = [row[0] for row in reader]  # 假设标签文件只有一列

    # 检查特征数据和标签数量是否匹配
    if len(feature_rows) != len(labels):
        raise ValueError("特征文件与标签文件的行数不匹配")

    # 将标签合并到特征数据的最后一列
    for i, row in enumerate(feature_rows):
        row.append(labels[i])

    # 创建 .data 文件，保留原始值
    data_file = output_name + '.data'
    with open(data_file, 'w') as data_f:
        for row in feature_rows:
            data_line = ','.join(row)
            data_f.write(data_line + '\n')

    # 将数据按列转置，方便按字段检测
    columns = list(zip(*feature_rows))

    # 创建 .info 文件，写入字段信息
    info_file = output_name + '.info'
    with open(info_file, 'w') as info_f:
        for idx, header in enumerate(headers):  # 处理特征列
            column = columns[idx]
            if is_continuous_column(column):
                info_f.write(f"{header} continuous\n")
            else:
                info_f.write(f"{header} discrete\n")
        # 最后一列为标签列
        info_f.write(f"{y_header} discrete\n")
        # LABEL_POS 行
        info_f.write("LABEL_POS -1\n")

    print(f"{data_file} 和 {info_file} 文件已生成.")

convert_csv_to_data_info(SRC_PATH, LABEL_PATH, 'rrl-DM_HW/dataset/' + TGT_NAME)
