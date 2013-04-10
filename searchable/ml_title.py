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
def normalize_title(title):
	title = title.replace("\n",'')
	title = regex_punc.sub('',title)
	title_clean = regex_num.sub('',title)
	words = title_clean.split()
	words_clean = [i.lower() for i in words if i.lower() not in nltk.corpus.stopwords.words('english')]
	return words_clean

def process_traning_data(fn):
	titles = []
	with codecs.open(fn,"r",encoding="utf-8") as f:
		for line in f.readlines():
			# print line
			# print line.strip().split("|")
			title,url,source,predict = line.strip().split("|")

			titles.append({'title': title, 'predict': int(predict),'source': source})
	return titles

#gen_data_mongo()
for i in process_traning_data("train_manual.data"):
	print normalize_title(i['title']),i['predict']


