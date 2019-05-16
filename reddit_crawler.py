#created by JT on May 30,2018
import requests
import requests.auth
import json
import time
from time import strftime,gmtime
from config import REDDIT_CRED
from datetime import datetime,date

client_auth = requests.auth.HTTPBasicAuth(REDDIT_CRED['ID'], REDDIT_CRED['SECRET'])
post_data = {"grant_type": "client_credentials", "username": REDDIT_CRED['USER'], "password": REDDIT_CRED["PASSWORD"]}
headers = {"User-Agent": "Apollo/0.1 by michaeljavy"}

def calculateDays(created_utc,factor):
	d1 = datetime.fromtimestamp(1523318400)
	d2 = datetime.fromtimestamp(created_utc)
	d3 = datetime.utcnow()
	if factor=="1":
		return (d1-d2).days
	else:
		return (d3-d2).days

def factorize(p):
	if p==True:
		return '1'
	else:
		return '0'
def profileDownload(author,new_headers,factor):#factor: 0=good 1=bad
		s=''
		try:
			user_response = requests.get("https://oauth.reddit.com/user/"+author+"/about", headers=new_headers)
			if user_response.status_code ==200:
				data = user_response.json()['data']
				s += author
				s += '\t'+factor
				s += '\t'+str(calculateDays(data['created_utc'],factor))
				s += '\t'+str(data['link_karma'])
				s += '\t'+str(data['comment_karma'])
				s += '\t'+factorize(data['has_verified_email'])
				s += '\t'+factorize(data['is_gold'])
				s += '\n'
			else:
				# print(user_response.content+"\n The author is "+author)
				return ''
		except Exception, e:
			# print(e)
			# print("whats wrong with: "+author)
			return ''
		return s


def get_good_users(new_headers):
	utc = "1420000000"
	s=''
	count = 0
	while count<1000:
		response = requests.get('https://api.pushshift.io/reddit/comment/search?after='+utc+'&before=1534688400&size=500')
		if response.status_code==200:
			response = response.json()
			for c in response['data']:
				if c['author']=="[deleted]":
					continue
				t = profileDownload(c['author'],new_headers,'0')
				if t=='':
					continue
				s+=t
				count+=1
				utc = str(c['created_utc'] + 1)
				if count>1000:
					break
	with open('train_good.txt','w') as f:
		print >> f,s
			
def get_bad_users(new_headers):
	s=''
	with open('bots.txt','r') as f:
			lines = f.readlines()
			for i in range(len(lines)):
				j = lines[i].index('\t')
				author = lines[i][2:j]
				s+=profileDownload(author,new_headers,'1')
	with open('train_bad.txt','w') as f:
		print >> f,s
	
def get_a_user_profile(author):
	new_headers = prep()
	return profileDownload(author,new_headers,"0")


def prep():
	response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
	response = response.json()
	access_token = response['access_token']
	token_type = response['token_type']
	new_headers = {"Authorization": str(token_type+" "+access_token), "User-Agent": "Apollo/0.1 by michaeljavy"}
	return new_headers

if __name__=="__main__":
	new_headers = prep()
	get_bad_users(new_headers)
	get_good_users(new_headers)



