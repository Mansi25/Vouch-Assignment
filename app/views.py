from django.shortcuts import render,redirect
import tweepy
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as lg
from .models import Tweets
from django.db.models import Count
from datetime import date, timedelta

import environ

env = environ.Env(
    DEBUG=(bool, False)
)

Consumer_Key=env('Consumer_Key')
Consumer_Secret=env('Consumer_Secret')
# Create your views here.

def api_obj(request):
	oauth = tweepy.OAuthHandler(Consumer_Key, Consumer_Secret)
	access_key = request.session['access_key_token']
	access_secret = request.session['access_secret_token']
	oauth.set_access_token(access_key, access_secret)
	api = tweepy.API(oauth, wait_on_rate_limit=True)
	return api
def base(request):
    if request.session.get('access_key_token',None) is not None :
        return redirect('Home')
    return render(request,'login.html')

def login(request):
    if request.session.get('access_key_token',None) is not None :
        return redirect('Home')
    oauth=tweepy.OAuthHandler(Consumer_Key,Consumer_Secret)
    try:
        redirect_url = oauth.get_authorization_url(True)
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
    request.session['request_token']= oauth.request_token    
    return HttpResponseRedirect(redirect_url)

def callback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(Consumer_Key, Consumer_Secret)
    token = request.session.get('request_token')
    request.session.delete('request_token')
    oauth.request_token = token
    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')
    request.session['access_key_token']=oauth.access_token
    request.session['access_secret_token']= oauth.access_token_secret
    return redirect('Home')

def loggedout(request):
    if request.session.get('access_key_token',None) is not None :
        return redirect('Home')
    return redirect('Base')

def logout(request):
    if request.session.get('access_key_token',None) is not None :
        request.session.clear()
        lg(request)        
    return redirect('Loggedout')

def home(request):
    if request.session.get('access_key_token',None) is not None :
        api=api_obj(request)
        user=api.me()
        context={
            'username':user.name
        }
        return render(request, 'index.html')
    return redirect('Login')

def all_twt(request):
    if request.session.get('access_key_token',None) is not None :
        api=api_obj(request)
        user=api.me()
        tweets=Tweets.objects.all()
        context={
            'my_list':tweets
        }
        return render(request,'tweettimeline.html',context)
    return redirect('Login')

def top_user(request):
    if request.session.get('access_key_token',None) is not None:
        tweets=Tweets.objects.values('User').order_by().annotate(user_count=Count('User'))
        print(tweets)
        Uid=max(tweets,key=lambda x:x['user_count'])
        api=api_obj(request)
        user=api.me()
        max_user=api.get_user(Uid['User'])
        context={
            'user':max_user
        }
        return render(request,'topuser.html',context)
    return redirect('Login')

def top_domain(request):
    if request.session.get('access_key_token',None) is not None:
        tweets=Tweets.objects.values('Domain').order_by().annotate(domain_count=Count('Domain'))
        tweets=sorted(tweets,key=lambda x:x['domain_count'],reverse=True)
        api=api_obj(request)
        user=api.me()
        domains=[]
        for i in range(0,min(3,len(tweets))):
            domains.append([tweets[i]['Domain'],tweets[i]['domain_count']])
        context={
            'my_list':domains
           
        }
        return render(request,'topdomain.html',context)
    return redirect('Login')

import json
class save_data():
    def get_domain(self,str):
        for x in range(0, len(str)):
            if (str[x] == '/'):
                return str[0:x]

    def insert_db(self,ttweet, url):
        tweet = Tweets()
        tweet.id = str(ttweet.id) + str(ttweet.user.id)
        tweet.Name = ttweet.user.name
        tweet.User = ttweet.user.id
        tweet.Tweet_id = ttweet.id
        tweet.Text = ttweet.text
        tweet.Domain = self.get_domain(url[0]['display_url'])
        tweet.Display_picture = ttweet.user.profile_image_url
        tweet.save()

def link_twt(request):
    if request.session.get('access_key_token',None) is not None:
        api = api_obj(request)
        user = api.me()
        delta = date.today() - timedelta(days=7)
        my_list = []
        for tweet in tweepy.Cursor(api.home_timeline, since_id=delta).items(100):
            url = tweet.entities['urls']
            if len(url) != 0:
                if url[0]['display_url'][0:7] != 'twitter':
                    my_list.append(tweet)
                    try:
                        save_data().insert_db(tweet, url)
                    except:
                        continue
                    
        context={
            'my_list': my_list
            
        }
        return render(request, 'fetchtweet.html',context)
    return redirect('Login')  