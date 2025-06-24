nvidia > result.txt

for i $(seq 1 10);
do 
    nvidia-smi >> result.txt sleep 1s;
done