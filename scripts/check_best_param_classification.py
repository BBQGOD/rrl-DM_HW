import os
import re
import sys

ROOT_DIR = sys.argv[1]
FIVE_FOLDED = sys.argv[2] == 'True'


def find_max_values(directory):
    max_third_value = -float('inf')  # 第三个数的最大值
    max_accuracy = -float('inf')    # 准确率的最大值
    max_dir = None                  # 最大值对应的子目录

    # 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        if 'test_res.txt' in files:  # 检查是否存在 test_res.txt 文件
            log_path = os.path.join(root, 'test_res.txt')

            if 'ki0' in root:  # 如果路径中包含 'ki'，我们处理五折验证
                avg_third_value = 0
                avg_accuracy = 0
                fold_count = 0
                
                # 遍历 ki0 到 ki4
                for i in range(5):
                    modified_root = root.replace('ki0', f'ki{i}')
                    modified_log_path = os.path.join(modified_root, 'test_res.txt')
                    
                    if os.path.exists(modified_log_path):
                        try:
                            third_value = None
                            accuracy = None

                            with open(modified_log_path, 'r') as f:
                                for line in f:
                                    # 提取第三个数
                                    match_third = re.search(r"macro avg\s+\S+\s+\S+\s+(\S+)", line)
                                    if match_third:
                                        third_value = float(match_third.group(1))

                                    # 提取准确率
                                    match_accuracy = re.search(r"Accuracy of RRL\s+Model:\s+(\S+)", line)
                                    if match_accuracy:
                                        accuracy = float(match_accuracy.group(1))

                            # 如果找到有效的值，累加
                            if third_value is not None and accuracy is not None:
                                avg_third_value += third_value
                                avg_accuracy += accuracy
                                fold_count += 1

                        except Exception as e:
                            print(f"无法读取文件 {modified_log_path}: {e}")

                # 如果所有五个文件都读取成功
                if fold_count == 5:
                    avg_third_value /= fold_count
                    avg_accuracy /= fold_count
                    print(f"目录 {root} 的平均 macro f1 为 {avg_third_value}，平均准确率为 {avg_accuracy}")

                    # 更新最大值
                    if (avg_third_value > max_third_value or 
                        (avg_third_value == max_third_value and avg_accuracy > max_accuracy)):
                        max_third_value = avg_third_value
                        max_accuracy = avg_accuracy
                        max_dir = root

    return max_dir, max_third_value, max_accuracy

result_dir, max_third, max_accuracy = find_max_values(ROOT_DIR)

if result_dir:
    print(f"最大macro f1为 {max_third}，最大准确率为 {max_accuracy}，对应的子目录是：{result_dir}")
else:
    print("未找到符合条件的文件或行。")
