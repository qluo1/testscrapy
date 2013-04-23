from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer,TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans


from .mongoquery import query_news_by_oid, query_wantTimes



def test():
	item = query_news_by_oid("5175e99a346e9d86e9abfbfa")
	vocab = {"pizza": 0, "beer": 1}
	vec = CountVectorizer(stop_words='english',vocabulary=vocab)

	# print item['content']
	return  vec.transform(item['content'])


def test1():
	item = query_news_by_oid("5175e99a346e9d86e9abfbfa")
	vec = HashingVectorizer(stop_words='english')
	return vec.transform([item['content'],])


def test2():
	items = query_wantTimes()
	hasher = HashingVectorizer(stop_words = 'english')
	vec = Pipeline( [('hasher', hasher), ('tf_idf',TfidfTransformer())])

	data = [ query_news_by_oid(i['oid'])['content'] for i in items]
	x = vec.fit_transform(data)
	print x.shape
	mk = KMeans(n_clusters=x.shape[0]-1,init='k-means++', max_iter =50, n_init=1,verbose=1)

	mk.fit(x)

	print km.labels_

