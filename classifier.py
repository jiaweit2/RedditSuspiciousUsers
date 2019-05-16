from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
import numpy as np
import sys
from reddit_crawler import get_a_user_profile

def load():
	y=[]
	x=[]
	with open('train_good.txt') as f:
		for num, line in enumerate(f):
			each_row = line.strip().split('\t')
			if len(each_row)<=1:
				continue
			days = each_row[2]
			link_karma = each_row[3]
			comment_karma = each_row[4]
			verified = each_row[5]
			gold = each_row[6]
			avg_days_link_karma = float(link_karma)/float(days)
			avg_days_cmt_karma = float(comment_karma)/float(days)
			x+=[[avg_days_link_karma,avg_days_cmt_karma,verified,gold]]
			y+=[0]
	with open('train_bad.txt') as f:
		for num, line in enumerate(f):
			each_row = line.strip().split('\t')
			if len(each_row)<=1:
				continue
			days = each_row[2]
			link_karma = each_row[3]
			comment_karma = each_row[4]
			verified = each_row[5]
			gold = each_row[6]
			avg_days_link_karma = float(link_karma)/float(days)
			avg_days_cmt_karma = float(comment_karma)/float(days)
			x+=[[avg_days_link_karma,avg_days_cmt_karma,verified,gold]]
			y+=[1]
	return x,y


def classify(x,y,author=None):
	clf = RandomForestClassifier(n_estimators = 50, random_state = 0)
	clf.fit(x,y)
	#FORMAT - test_x: [[avg_days_link_karma,avg_days_cmt_karma,verified,gold]]
	#clf.predict(test_x)
	#here put in the test data to get the prediction
	#1: suspicious account 
	#0: normal account
	if author!=None:
		s = get_a_user_profile(author)
		each_row = s.strip().split('\t')
		days = each_row[2]
		link_karma = each_row[3]
		comment_karma = each_row[4]
		verified = each_row[5]
		gold = each_row[6]
		avg_days_link_karma = float(link_karma)/float(days)
		avg_days_cmt_karma = float(comment_karma)/float(days)
		score = clf.predict([[avg_days_link_karma,avg_days_cmt_karma,verified,gold]])
		if score==[1]:
			print "This account is suspicious!"
		else:
			print "Just some normal user..."
if __name__ == '__main__':
	x,y = load()
	if len(sys.argv)>1:
		classify(x,y,sys.argv[1])
	else:
		classify(x,y)


