import json
import time
import os
import psutil
import requests

last_connection_time = time.time() # Track the last connection time
last_update_time = time.time()     # Track the last update time
posting_interval = 120             # Post data once every 2 minutes
update_interval = 15               # Update once every 15 seconds

write_api_key = "YOUR-CHANNEL-WRITEAPIKEY" # Replace YOUR-CHANNEL-write_api_key with your channel write API key
channel_ID = "YOUR-CHANNELID"              # Replace YOUR-channel_ID with your channel ID
url = "https://api.thingspeak.com/channels/" + channel_ID + "/bulk_update.json" # ThingSpeak server settings
message_buffer = []

def httpRequest():
    # Function to send the POST request to ThingSpeak channel for bulk update.
        global message_buffer
        bulk_data = json.dumps({'write_api_key':write_api_key,'updates':message_buffer}) # Format the json data buffer
        request_headers = {"User-Agent":"mw.doc.bulk-update (Raspberry Pi)","Content-Type":"application/json","Content-Length":str(len(bulk_data))}
    # Make the request to ThingSpeak
        try:
            # print(request_headers)
            response = requests.post(url,headers=request_headers,data=bulk_data)
            print (response) # A 202 indicates that the server has accepted the request
        except e:
            print(e.code) # Print the error code
        message_buffer = [] # Reinitialize the message buffer
        global last_connection_time
        last_connection_time = time.time() # Update the connection time

def getData():
    # Function that returns the CPU temperature and percentage of CPU utilization
        cmd = '/opt/vc/bin/vcgencmd measure_temp'
        process = os.popen(cmd).readline().strip()
        cpu_temp = process.split('=')[1].split("'")[0]
        cpu_usage = psutil.cpu_percent(interval=2)
        return cpu_temp,cpu_usage

def updatesJson():
    # Function to update the message buffer every 15 seconds with data. 
    # And then call the httpRequest function every 2 minutes. 
    # This examples uses the relative timestamp as it uses the "delta_t" parameter.
    # If your device has a real-time clock, you can also provide the absolute timestamp 
    # using the "created_at" parameter.

        global last_update_time
        message = {}
        message['delta_t'] = int(round(time.time() - last_update_time))
        Temp,Usage = getData()
        message['field1'] = Temp
        message['field2'] = Usage
        global message_buffer
        message_buffer.append(message)
    # If posting interval time has crossed 2 minutes update the ThingSpeak channel with your data
        if time.time() - last_connection_time >= posting_interval:
                httpRequest()
                last_update_time = time.time()

if __name__ == "__main__":  # To ensure that this is run directly and does not run when imported
        while True:
                # If update interval time has crossed 15 seconds update the message buffer with data
            if time.time() - last_update_time >= update_interval:
                updatesJson()