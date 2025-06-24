nvidia > result.txt

for ((i = 0 ; i < 10 ; i++ )); do nvidia-smi >> result.txt; sleep 1s; done