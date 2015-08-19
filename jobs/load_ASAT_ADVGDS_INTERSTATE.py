import requests

username = "podium"
password = "nvs2014!"
host = "172.21.6.66"
port = "8675"
projectName = "podium"
sourceType = "entity/loadDataForEntities/3348,3349,3350,3351,3352,3354,3355,3356,3357,3359,3360,3361,3362,3363,3364,3365,3366,3367,3368,3369,3370,3371,3372,3353,3358/1"
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
    



