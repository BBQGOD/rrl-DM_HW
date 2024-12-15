#!/bin/bash

cd rrl-DM_HW/scripts

python check_best_param_classification.py ../log_folder/bank-marketing True > log.bank-marketing.txt
python check_best_param_regression.py ../log_folder/boston-housing True > log.boston-housing.txt
