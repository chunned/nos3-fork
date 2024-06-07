import json
import time, hmac, hashlib
import requests
import re, uuid
import math
import os
from dotenv import load_dotenv


def collect(file):
    # Reads the last line of a CSV file and returns the values
    with open(file, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = f.readline().decode()
    return last_line


# Load environment variables
load_dotenv()
DATA_FILE = os.getenv("DATA_FILE")
HMAC_KEY = os.getenv("HMAC_KEY")
API_KEY = os.getenv("API_KEY")

# Create empty HMAC signature
emptySignature = ''.join(['0'] * 64)

# use MAC address of network interface as deviceId
device_name = ":".join(re.findall('..', '%012x' % uuid.getnode()))

# Collection frequency interval
INTERVAL_MS = 25   
freq = INTERVAL_MS/1000

# How many iterations (rounds) should the collector perform?
ROUNDS = 100


values = []
for i in range(ROUNDS):
    x = collect(COLLECTION_FILE)
    values.append(x)
    time.sleep(freq)

# ---------- BELOW FROM https://github.com/edgeimpulse/linux-sdk-python/blob/master/examples/custom/collect.py

data = {
    "protected": {
        "ver": "v1",
        "alg": "HS256",
        "iat": time.time() # epoch time, seconds since 1970
    },
    "signature": emptySignature,
    "payload": {
        "device_name":  device_name,
        "device_type": "LINUX_TEST",
        "interval_ms": INTERVAL_MS,
        "sensors": [
            { "name": "accX", "units": "m/s2" },
            { "name": "accY", "units": "m/s2" },
            { "name": "accZ", "units": "m/s2" }
        ],
        "values": values
    }
}



# encode in JSON
encoded = json.dumps(data)

# sign message
signature = hmac.new(bytes(HMAC_KEY, 'utf-8'), msg = encoded.encode('utf-8'), digestmod = hashlib.sha256).hexdigest()

# set the signature again in the message, and encode again
data['signature'] = signature
encoded = json.dumps(data)

# and upload the file
res = requests.post(url='https://ingestion.edgeimpulse.com/api/training/data',
                    data=encoded,
                    headers={
                        'Content-Type': 'application/json',
                        'x-file-name': 'idle01',
                        'x-api-key': API_KEY
                    })
if (res.status_code == 200):
    print('Uploaded file to Edge Impulse', res.status_code, res.content)
else:
    print('Failed to upload file to Edge Impulse', res.status_code, res.content)