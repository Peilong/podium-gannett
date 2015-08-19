import requests

username = "podium"
password = "nvs2014!"
host = "172.21.6.66"
port = "4675"
projectName = "podium"
sourceType = "entity/loadDataForEntities/3091,3093,3094,3095,3096,3097,3098,3099,3100,3101,3102,3103,3104,3105,3106,3107,3109,3110,3111,3112,3113,3115,3108,3092,3114/1"
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
    



