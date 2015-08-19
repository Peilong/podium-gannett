import requests

username = "podium"
password = "nvs2014!"
host = "172.21.6.66"
port = "8675"
projectName = "podium"
sourceType = "entity/loadDataForEntities/3039,3040,3041,3042,3043,3044,3045,3046,3047,3048,3049,3050,3051,3053,3054,3055,3056,3057,3059,3060,3061,3062,3063,3052,3058/1"
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
    



