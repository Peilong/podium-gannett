import requests
import json
import time
from datetime import datetime

username = "podium"
password = "nvs2014!"
host = "172.21.6.66"
port = "4675"
projectName = "podium"
sourceType = "entity/loadDataForEntities/true"
url = "http://" + host + ":" + port + "/" + projectName + "/"
securityUrl = url + "j_spring_security_check"

s = requests.session()
login_data = dict(j_username=username, j_password=password)
headers = {'content-type': 'application/json'}
print headers

now = datetime.now()
payload = []
payload1 = dict(loadTime=now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), entityId="3539")
payload2 = dict(loadTime=now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), entityId="3535")

# payload3 = dict(loadTime=now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), entityId="3539")
payload.append(payload1)
payload.append(payload2)
# payload.append(payload3)

loginResponse = s.post(securityUrl, data=login_data)
loginResponseText = loginResponse.text

if not "login" in loginResponseText:
    r = s.put(url + sourceType, data=json.dumps(payload), headers=headers)
    print (r.text)
    
else:
    print ("Invalid username or password....!!")
    



