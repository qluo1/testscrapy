import pymongo
from pymongo import MongoClient
import codecs

client = MongoClient()
from collections import namedtuple

News = namedtuple("News","title,url,source")

def extract_row_data_mongo():
	news_data = []

	for i in client['scrapy'].items.find({'source': {"$ne": 'ABC'}}):
		news_data.append(News(i['title'],i['url'],i['source']))

	return {'train': news_data[0:100], 'test': news_data[101:] }

query_content = lambda url: client['scrapy'].items.find_one({'url': url})['content']

def dump_data_csv(fname, data):
	"""
	"""
	with codecs.open(fname, "w",encoding="utf-8") as f:
		for i in data:
			# print "%s,%s,%s," % (i.title,i.url,i.source)
			f.write("%s|%s|%s|\n" % (i.title,i.url,i.source))


def gen_data_mongo():
	data = extract_row_data_mongo()

	dump_data_csv("train.csv",data['train'])
	dump_data_csv("test.csv",data['test'])


import re
import string
import nltk

regex_punc = re.compile("[%s]" % re.escape(string.punctuation))
regex_num = re.compile("[0-9]")

def normalize_text(text):
	"""
		- remove html tags
		- remove EOL
		- remove punctuation
		- remove numerical
		- remove stopwords
	"""
	_text = nltk.clean_html(text).replace("\n",'')
	_text = regex_punc.sub('',_text)
	text_clean = regex_num.sub('',_text)
	words = text_clean.split()
	words_clean = [i.lower() for i in words if i.lower() not in nltk.corpus.stopwords.words('english')]
	return words_clean

def process_training_data(fn):
	words = []
	with codecs.open(fn,"r",encoding="utf-8") as f:
		for line in f.readlines():
			title,url,source,predict = line.strip().split("|")
			if int(predict) == 1:
				content = query_content(url)
				[ words.append(i) for i in normalize_text(content)]
	top_words = nltk.FreqDist(words)
	print len(top_words)
	return top_words.keys()[:30]

def features_set( fn):
	top_words = process_training_data(fn)
	f_set = []
	with codecs.open(fn,"r",encoding="utf-8") as f:
		for line in f.readlines():
			title,url,source,predict = line.strip().split("|")
			content = query_content(url)
			target = set(normalize_text(content))
			features = {}
			for w in top_words:
				features["w_%s" % w] = (w in target)
			f_set.append((features,int(predict)))

	return top_words,f_set

top_words,train_set = features_set("train_manual.data")
classifier = nltk.NaiveBayesClassifier.train(train_set)

def predict(fn,top_words,classifier):
	with codecs.open(fn,"r",encoding='utf-8') as f:
		for line in f.readlines():
			title,url,source,predict = line.strip().split("|")
			try:
				content = query_content(url)
			except TypeError:
				continue
			target = set(normalize_text(content))
			features = {}
			for w in top_words:
				features["w_%s" % w] = (w in target)
			res = classifier.classify(features)
			if res == 0:
				print res, title

predict("test.csv",top_words,classifier)

