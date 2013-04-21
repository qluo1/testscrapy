from views.view import home,get_index,get,search,get_news,demo


def build_url(app):
    urls = (
        app.add_url_rule('/','home',home),
        app.add_url_rule('/demo','demo',demo),
        app.add_url_rule('/index/<index>','index',get_index),
        app.add_url_rule('/get/<ref>', 'get',get),
        app.add_url_rule('/query/<oid>','query',get_news),
        app.add_url_rule('/search','search',search, methods=['POST']),
    )
    # return urls

