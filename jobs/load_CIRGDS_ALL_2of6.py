import requests

username = "podium"
password = "nvs2014!"
host = "172.21.6.66"
port = "8675"
projectName = "podium"
sourceType = "entity/loadDataForEntities/3430,3432,3433,3434,3435,3436,3437/1"
url = "http://" + host + ":" + port + "/" + projectName + "/"
securityUrl = url + "j_spring_security_check"

s = requests.session()
login_data = dict(j_username=username, j_password=password)
loginResponse = s.post(securityUrl, data=login_data)
loginResponseText = loginResponse.text

if not "login" in loginResponseText:
    r = s.put(url + sourceType)
    print (r.text)
    
else:
    print ("Invalid username or password....!!")
    



