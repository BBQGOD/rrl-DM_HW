#!/bin/bash

cd rrl-DM_HW/scripts

python check_best_param.py ../log_folder/bank-marketing > log.bank-marketing.txt True
python check_best_param.py ../log_folder/breast-cancer > log.bank-marketing.txt False
# python check_best_param.py ../log_folder/bank-marketing > log.bank-marketing.txt True
