#saves the nvidi-smi result to a text file
nvidia-smi > result.txt

#continues to send nvidi-smi result to the text file for the next 5 mins every min
for ((i = 0 ; i < 300 ; i++ )); do nvidia-smi >> result.txt; sleep 1s; done

#create an original html file of htop (like a screenshot of the current state)
echo q | htop | aha --black --line-fix > htop.html

#to save the htop as a html file
for ((i = 0 ; i < 300 ; i++ )); do echo q | htop | aha --black --line-fix >> htop.html; sleep 1s; done

# to save top it as a csv file
for ((i = 0 ; i < 10 ; i++ )); do (ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | awk 'BEGIN {OFS=","} NR==1 {print "PID,PPID,CMD,%MEM,%CPU"} NR>1 {print $1,$2,$3,$4,$5}' > processes.csv); sleep 1s; done

# to bring these file back locally:

scp root@srv1-lg1:/root/htop.html . # in console
scp rahulrajkumar@console.sb2.cosmos-lab.org:htop.html .

# for stressing the compute with artifical load using stres-ng

stress-ng -c 0 -l 40


