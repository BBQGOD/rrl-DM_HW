import os
import re
import sys

ROOT_DIR = sys.argv[1]
FIVE_FOLDED = sys.argv[2] == 'True'


def find_max_values(directory):
    max_third_value = -float('inf')  # 第三个数的最大值
    min_rmse = float('inf')   # 准确率的最大值
    max_dir = None                  # 最大值对应的子目录

    # 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        if 'test_res.txt' in files:  # 检查是否存在 test_res.txt 文件
            log_path = os.path.join(root, 'test_res.txt')

            if 'ki0' in root:  # 如果路径中包含 'ki'，我们处理五折验证
                avg_third_value = 0
                avg_rmse = 0
                fold_count = 0
                
                # 遍历 ki0 到 ki4
                for i in range(5):
                    modified_root = root.replace('ki0', f'ki{i}')
                    modified_log_path = os.path.join(modified_root, 'test_res.txt')
                    
                    if os.path.exists(modified_log_path):
                        try:
                            third_value = None
                            rmse = None

                            with open(modified_log_path, 'r') as f:
                                file = []
                                for line in f:
                                    # 提取rmse
                                    match_rmse = re.search(r"RMSE of RRL\s+Model:\s+(\S+)", line)
                                    if match_rmse:
                                        rmse = float(match_rmse.group(1))
                                        
                                    file.append(line)
                                file = "".join(file)
                                # 提取第三个数
                                match_third = re.search(r"^Performance of  RRL Model:\s*(\S+)$", file, re.MULTILINE)
                                if match_third:
                                    third_value = float(match_third.group(1))

                            # 如果找到有效的值，累加
                            if third_value is not None and rmse is not None:
                                avg_third_value += third_value
                                avg_rmse += rmse
                                fold_count += 1

                        except Exception as e:
                            print(f"无法读取文件 {modified_log_path}: {e}")

                # 如果所有五个文件都读取成功
                if fold_count == 5:
                    avg_third_value /= fold_count
                    avg_rmse /= fold_count
                    print(f"目录 {root} 的平均 r^2 为 {avg_third_value}，平均rmse为 {avg_rmse}")

                    # 更新最大值
                    if (avg_third_value > max_third_value or 
                        (avg_third_value == max_third_value and avg_rmse < min_rmse)):
                        max_third_value = avg_third_value
                        min_rmse = avg_rmse
                        max_dir = root

    return max_dir, max_third_value, min_rmse

result_dir, max_third, min_rmse = find_max_values(ROOT_DIR)

if result_dir:
    print(f"最大r^2为 {max_third}，最小rmse为 {min_rmse}，对应的子目录是：{result_dir}")
else:
    print("未找到符合条件的文件或行。")
