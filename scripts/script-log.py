from datetime import datetime

import base64
from urllib.parse import unquote
import re

log_pattern = re.compile(r'\[(.*?)\] .*?order=([a-zA-Z0-9%]+)\sHTTP')

file_path = "/home/guillaume/Downloads/ch13.txt"

timestamps = []
queries = []
binary_string = ""
bit_pos = []
def parse_time(time_str):
    # On ignore le fuseau horaire (+0200) pour simplifier le calcul relatif
    time_format = "%d/%b/%Y:%H:%M:%S"
    clean_time = time_str.split(' ')[0] 
    clean_time = clean_time.replace("[", "") 
    return datetime.strptime(clean_time, time_format)

with open(file_path, 'r') as f:
    for line in f:
        match = log_pattern.search(line)
        if match:
            timestamps.append(parse_time(match.group(1)))
            b64_payload = unquote(match.group(2)) # Remplace %3D par =
    
            # 2. Décoder le SQL
            sql_decode = base64.b64decode(b64_payload).decode('utf-8')
            
            # 3. Extraire les positions
            char_pos = re.search(r'password,(\d+),1', sql_decode).group(1)
            bit_pos.append(re.search(r'password,\d+,1\)\)\),(\d+),1', sql_decode).group(1))

current_byte = ""
password = ""
for i in range(len(timestamps) - 1):
#for i in range(8):
    delta = (timestamps[i+1] - timestamps[i]).total_seconds()
    # case where we compare the last bit (time sleep values different from normal comparison)
    print(delta, bit_pos[i])
    if bit_pos[i] == "7":
    # short function : 1 bit 
        if (delta == 2.0):
            bit = "0" 
        elif(delta == 4.0):
            bit = "1"
        else:
            bit = ""
        
        current_byte += bit
        byte = current_byte.zfill(8)
        print("current byte ", byte)
        password += chr(int(byte, 2))
        current_byte = ""
    else:
    # longer function : 2 bits
        par = ""
        if delta == 0.0: par += "00"
        elif delta == 2.0: par += "01"
        elif delta == 4.0: par += "10"
        elif delta == 6.0: par += "11"

        current_byte += par

print("Password : ", password)
