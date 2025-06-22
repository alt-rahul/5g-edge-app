import time
from datetime import datetime

intial = datetime.now()

time_curr = intial.strftime("%H:%M:%S")

print(f"initial time: {time_curr}")

while(True):
    time.sleep(5)
    now = datetime.now()
    change =  now - intial
    print(f"change in time {change.seconds}")
