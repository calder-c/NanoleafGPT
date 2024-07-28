import requests
import time
print('--- Nanoleaf Authentication Helper ---')
time.sleep(0.5)
print('To begin, please hold the on-off button down for 5-7 seconds until your leds start flashing in a pattern.')
time.sleep(0.5)
input('Any input to proceed >> ')
time.sleep(0.15)
ip = input('Please input the IP of your Nanoleaf device >> ')
time.sleep(0.15)
print('The helper will now retrieve your auth token. Keep it safe!')
http = 'http://'+ip+':16021/api/v1/new'
print('POSTing to ' + http + '...')
data = requests.post(http)
print('Done, Response ' + str(data.status_code))
if data.status_code == 200:
    print(data.text)
    print('This is your token!')
else:
    print('Something went wrong. Ensure the IP is correct and you have used this helper less than 30 seconds after you have initiated the pairing.')
