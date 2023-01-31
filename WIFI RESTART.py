import os
import time

wifi_name = 'SOLUPPI'
enable_wifi = 'netsh interface set interface "'+wifi_name+'" enabled'
disable_wifi = 'netsh interface set interface "'+wifi_name+'" disabled'


#disable wifi, if network is OFFLINE
os.popen(disable_wifi)

time.sleep(10)
#enable wifi
os.popen(enable_wifi)