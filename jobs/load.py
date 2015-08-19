import requests

username = "podium"
password = "nvs2014!"
host = "ludwig.podiumdata.com"
port = "8080"
projectName = "podium"
sourceType = "source/internal"
url = "http://" + host + ":" + port + "/" + projectName + "/"
securityUrl = url + "j_spring_security_check"

s = requests.session()
login_data = dict(j_username=username, j_password=password)
loginResponse = s.post(securityUrl, data=login_data)
loginResponseText = loginResponse.text

if not "login" in loginResponseText:
    r = s.get(url + sourceType)
    print (r.text)
    
else:
    print ("Invalid username or password....!!")
    



