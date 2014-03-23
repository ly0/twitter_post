import requests
import time
from datetime import datetime
from BeautifulSoup import BeautifulSoup
import simplejson as json
import requests
from random import randint
import urllib, cStringIO,StringIO

def test():
    username = "abc"
    password = "abc"
    kit = TwitterDevKit(username,password)
    kit.post_image('nice picture',"http://fallfor.com/static/img/promot1.jpg")


class TwitterDevKit(object):
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login_dev()


    def login_dev(self):
        login_page = "https://twitter.com/login"
        authenticity_token,cookies = self._get_dev_login_data(login_page)
        data = {'session[username_or_email]':self.username,'session[password]':self.password,'remember_me': 1,\
                'redirect_after_login': '/','authenticity_token':authenticity_token,
                'authenticity_token':authenticity_token,'scribe_log':''}
        
        headers = self._get_dev_header()
        headers['Referer'] = 'https://twitter.com/login'
        r =  self.session.post('https://twitter.com/sessions', data=data,headers=headers)
        if r.status_code == requests.codes.ok:
            print "logged in!"
            return True
        else:
            print "Can't login!"
            return None


    def _get_dev_login_data(self,login_page):
        r = self.session.get(login_page,headers=self._get_dev_header())
        bf = BeautifulSoup(r.content)
        authenticity_token = bf.find('input',{'name':'authenticity_token'})['value']
        return authenticity_token,r.cookies


    
    def _get_authenticity_token(self):
        url = 'https://twitter.com/'
        r = self.session.get(url)
        bf = BeautifulSoup(r.content)
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

    def post_image(self,text,image):
        headers = {'Host':' upload.twitter.com','Referer':'https://twitter.com/',
                   'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Connection': 'keep-alive'
                   }
               

        url = 'https://upload.twitter.com/i/tweet/create_with_media.iframe'
        image = "https://d3ltqlcsk1pxob.cloudfront.net/img/fallfor_icon.png"
        #r = StringIO.StringIO(urllib.urlopen(image).read())
        r = cStringIO.StringIO(urllib.urlopen(image).read())
        
        headers['Content-Length'] = 320583
        headers['Content-Type']= 'boundary=---------------------------17081664101591459774755598233'  

        authenticity_token = self._get_authenticity_token()
        if not authenticity_token:
            return False
        data = {'post_authenticity_token':authenticity_token,'place_id':None,'status':text,'in_reply_to_status_id':None,\
                'impression_id':None,'page_context':None,'media_empty':None,'place_id':None,'earned':None}
        data['media_data[]'] = urllib.urlopen(image).read()
        data['iframe_callback'] = 'window.top.swift_tweetbox_1395441791174'

        r = self.session.post(url,data=data,headers=headers)
