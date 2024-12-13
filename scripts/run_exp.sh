#!/bin/bash

cd rrl-DM_HW
# trained on the bank-marketing data set with available GPUs.

available_gpus=(0 1 2)

dataset=bank-marketing

# 网格搜索结构参数列表
learning_rates=(0.001)
temperatures=(1.0)
structures=("4@64" "16@64" "64@64" "128@64" "128@1" "128@16" "128@1024")
weight_decays=(0)

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
                        -t classification \
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


dataset="breast-cancer-{}"

# 网格搜索结构参数列表
learning_rates=(0.001)
temperatures=(1.0)
structures=("4@32" "16@32" "32@16" "32@8" "32@4" "32@1")
weight_decays=(0)

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
                # 获取当前可用的 GPU
                gpu_id=${available_gpus[$current_job%gpu_count]}
                
                # 启动实验
                CUDA_VISIBLE_DEVICES=$gpu_id \
                python experiment.py \
                    -d $dataset \
                    -t classification-test \
                    -bs 32 \
                    -s $structure \
                    -e401 \
                    -lrde 100 \
                    -lr $lr \
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

# 等待所有剩余的后台工作完成
wait

echo "$dataset done"


dataset="boston-housing"

# 网格搜索结构参数列表
learning_rates=(0.001)
temperatures=(1.0)
structures=("4@64" "16@64" "64@64" "128@64" "128@1" "128@16" "128@1024")
weight_decays=(0)

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
                for i in 0 #1 2 3 4
                do
                    # 获取当前可用的 GPU
                    gpu_id=${available_gpus[$current_job%gpu_count]}
                    
                    # 启动实验
                    CUDA_VISIBLE_DEVICES=$gpu_id \
                    python experiment.py \
                        -d $dataset \
                        -t regression \
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
