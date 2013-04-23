/*jslint node: true */
'use strict';

define (
    ['components/flight/lib/component','testapp/template/templates',
     'components/mustache/mustache','components/underscore-amd/underscore'],

    function(defineComponent,templates,Mustache, underscore) {
        //
        return defineComponent(newsData);

        function newsData() {

            this.defaultAttrs({ });

            this.onIndexDataReady = function(data) {
                //
                // alert(data);
                var html = Mustache.to_html(templates.indexItem, {items:data});
                this.trigger(document,"onIndexDataReady",{markup: html});
            };

            this.onNewsDataReady = function(data) {

                // alert(data);
                var html = Mustache.to_html(templates.newsItem,data);
                this.trigger(document,"onNewsDataReady",{markup: html});

            };

            this.onIndexData = function(e,data) {

                // filter  & cache
                var that = this;
                // default
                var url = '/yahoo/business';
                if (data && data.src) {
                    url = "/" + data.src;
                    if (data.type) {
                        url += "/" + data.type;
                    }
                }

                jQuery.getJSON(url, function(data) {
                        that.onIndexDataReady.apply(that,[data]);
                 });
            };

            this.onNewsData = function(e,data) {
                var that = this;
                jQuery.getJSON('/query/' + data.ref, function(data){
                    that.onNewsDataReady.apply(that,[data]);
                });
            };


            this.after('initialize',function ()
            {   
                // default, load default content
                //
                this.on(document,"loadIndexData",this.onIndexData);
                this.on(document,"loadNewsData",this.onNewsData);
            });

        } /* uiIndexContent */
    }
);