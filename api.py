import requests
import time
from datetime import datetime
from BeautifulSoup import BeautifulSoup
import simplejson as json
import requests
from random import randint
import urllib, cStringIO,StringIO
from requests_toolbelt import MultipartEncoder
from base64 import b64encode

def test():
    username = "user"
    password = "pass"
    kit = TwitterDevKit(username,password)
    kit.post_image('nice picture',"http://fallfor.com/static/img/promot1.jpg")


class TwitterDevKit(object):
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login_dev()


    def login_dev(self):
        print 'Login start'
        login_page = "https://twitter.com/login"
        authenticity_token,cookies = self._get_dev_login_data(login_page)
        data = {'session[username_or_email]':self.username,'session[password]':self.password,'remember_me': 1,\
                'redirect_after_login': '/','authenticity_token':authenticity_token,
                'authenticity_token':authenticity_token,'scribe_log':''}
        
        headers = self._get_dev_header()
        headers['Referer'] = 'https://twitter.com/login'
        print 'Login2'
        r =  self.session.post('https://twitter.com/sessions', data=data,headers=headers)
        if r.status_code == requests.codes.ok:
            print "logged in!"
            return True
        else:
            print "Can't login!"
            return None

    def _get_dev_header(self):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding':'gzip, deflate',
                   'Accept-Language':'en-US,en;q=0.5',
                   'Connection':'keep-alive',
                   'Host':'twitter.com',
                   'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0'
                   }
        return headers
    def _get_dev_login_data(self,login_page):
        r = self.session.get(login_page,headers=self._get_dev_header())
        print 'GET'
        bf = BeautifulSoup(r.content)
        authenticity_token = bf.find('input',{'name':'authenticity_token'})['value']
        return authenticity_token,r.cookies


    
    def _get_authenticity_token(self):
        url = 'https://twitter.com/'
        r = self.session.get(url)
        bf = BeautifulSoup(r.content)
        self.write_result(r)
        form = bf.find('form',{'id':'signout-form'})
        if not form:
            return False
        authenticity_token = form.find('input',{'name':'authenticity_token'})['value']
        return authenticity_token
    
    def post_text(self,text):
        headers = {'X-Requested-With':'XMLHttpRequest','Referer':'https://twitter.com/','Pragma':'no-cache'}
        url = 'https://twitter.com/i/tweet/create'
        authenticity_token = self._get_authenticity_token()
        if not authenticity_token:
            return False
        data = {'authenticity_token':authenticity_token,'place_id':None,'status':text}
        r = self.session.post(url,data=data,headers=headers)
    def write_result(self,r):
        print r.content
    def post_image(self,text,image):
        print 'CALLED'
        headers = {'Referer':'https://twitter.com/',
                    'origin':'https://twitter.com',
                    'user-agent':'Mozilla/5.0'
                   }
               
        url = 'https://upload.twitter.com/i/tweet/create_with_media.iframe'
        image = "https://www.google.com/logos/doodles/2014/agnes-martin-102nd-birthday-6193044541931520-hp.jpg"

        f = open('/home/latyas/Pictures/xxx.png','rb')

        authenticity_token = self._get_authenticity_token()
        if not authenticity_token:
            return False
        data = {'post_authenticity_token':authenticity_token,'place_id':None,'status':'HAHAHAHA','in_reply_to_status_id':None,\
                'impression_id':None,'page_context':None,'media_empty':(""),'place_id':None,'earned':None}
        
        data['media_data[]'] = b64encode(f.read()) 
        data['iframe_callback'] = 'window.top.swift_tweetbox_1395541013159'
        
        body = MultipartEncoder(data)
        headers['content-type'] = body.content_type
        
        r = self.session.post(url,data=body,headers=headers)
        #print r.content
        self.write_result(r)

test()
