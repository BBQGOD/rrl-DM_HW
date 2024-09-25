#!/bin/bash

cd rrl-DM_HW
# trained on the bank-marketing data set with available GPUs.

available_gpus=(2 2 2 6 6 6 7 7 7)

dataset=bank-marketing

# 参数列表
learning_rates=(0.0002 0.001 0.005)          # 学习率
temperatures=(1.0 0.1 0.01)                 # 温度参数
structures=("1@16" "4@16" "16@16" "1@64" "1@1024" "1@64@32" "1@64@32@16")      # 结构
weight_decays=(0.0001 0.01 0.00001 0)          # 权重衰减

gpu_count=${#available_gpus[@]}  # 可用GPU数量
current_job=0  # 当前实验计数器

# 迭代网格搜索
for lr in "${learning_rates[@]}"
do
    for temp in "${temperatures[@]}"
    do
        for structure in "${structures[@]}"
        do
            for wd in "${weight_decays[@]}"
            do
                for i in 0 1 2 3 4
                do
                    # 获取当前可用的 GPU
                    gpu_id=${available_gpus[$current_job%gpu_count]}
                    
                    # 启动实验
                    CUDA_VISIBLE_DEVICES=$gpu_id \
                    python experiment.py \
                        -d $dataset \
                        -bs 32 \
                        -s $structure \
                        -e401 \
                        -lrde 100 \
                        -lr $lr \
                        -ki $i \
                        -i 0 \
                        -wd $wd \
                        --temp $temp \
                        --save_best \
                        --print_rule &

                    # 增加实验计数器
                    current_job=$((current_job + 1))

                    # 如果达到 GPU 数量的上限，暂停并等待所有后台作业完成
                    if (( current_job % gpu_count == 0 )); then
                        wait  # 等待GPU资源释放
                    fi
                done
            done
        done
    done
done

# 等待所有剩余的后台工作完成
wait

echo "$dataset done"
