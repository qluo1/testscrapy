import os
import sys
import re
import string
import codecs
import pymongo
from pymongo import MongoClient
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

ROOT = os.path.dirname(os.path.abspath(__file__))

# project setting
from scrapy.conf import settings

class YahooClassifier(object):
	"""
	"""
	def __init__(self):
		"""
			build classifier
		"""
		self._client = MongoClient()
		self._train_fn = os.path.join(ROOT,"train_manual.data")
		# top_words
		words = []
		with codecs.open(self._train_fn,"r",encoding="utf-8") as f:
			for line in f.readlines():
				title,url,source,predict = line.strip().split("|")
				if int(predict) == 1:
					content = self._query_content(url)
					[ words.append(i) for i in normalize_text(content)]
		top_words = nltk.FreqDist(words)
		self._top_words = top_words.keys()[:settings['NUM_TOP_WORDS']]

		# feature
		f_set = []
		with codecs.open(self._train_fn,"r",encoding="utf-8") as f:
			for line in f.readlines():
				title,url,source,predict = line.strip().split("|")
				content = self._query_content(url)
				f_set.append((self._ext_features(content),int(predict)))
		# build classifier
		self._classifier = nltk.NaiveBayesClassifier.train(f_set)

	def _query_content(self,url):
		""" helper	"""
		item = self._client['scrapy'].items.find_one({'url': url})
		if item:
			return  item['content']
		return None

	def _ext_features(self,content):
		""" """
		assert(self._top_words)
		target = set(normalize_text(content))
		features = {}
		for w in self._top_words:
			features["w_%s" % w] = (w in target)
		return features

	def classify(self,text):
		""" """
		assert(self._classifier)
		features = self._ext_features(text)
		# print features
		return self._classifier.classify(features)


if __name__ == "__main__":
	import numpy
	classifier = YahooClassifier()
	stat = []
	with codecs.open("test.csv","r",encoding='utf-8') as f:
		for line in f.readlines():
			title,url,source,predict = line.strip().split("|")
			content = classifier._query_content(url)
			if content is None:
				continue
			# print title,predict
			stat.append([classifier.classify(content),int(predict)])

	out = numpy.array(stat,int)
	print out,sum(out[:,0]), sum(out[:,1])
	print out.shape
	print "accuarcy: ", 1 - sum(out[:,0] != out[:,1]) * 1.0 / out.shape[0]




