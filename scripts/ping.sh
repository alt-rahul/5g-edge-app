nvidia-smi > result.txt

for ((i = 0 ; i < 300 ; i++ )); do nvidia-smi >> result.txt; sleep 1s; done

echo q | htop | aha --black --line-fix > htop.html

for ((i = 0 ; i < 300 ; i++ )); do echo q | htop | aha --black --line-fix >> htop.html; sleep 1s; done


# to bring these file back locally:

scp root@srv1-lg1:/root/htop.html . # in console
scp rahulrajkumar@console.sb2.cosmos-lab.org:htop.html .



