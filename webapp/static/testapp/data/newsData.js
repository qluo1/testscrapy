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
                jQuery.ajax({
                    url: "/get/business",
                    method: "GET",
                    dataType: "json",
                    success: function(data) {that.onIndexDataReady.apply(that,[data]);}
                    //error: function
                });
            };

            this.onNewsData = function(e,data) {

                var that = this;
                alert(data.ref);
                jQuery.ajax({
                    url: '/query/' + data.ref,
                    method: 'GET',
                    dataType :'json',
                    success : function(data) {that.onNewsDataReady.apply(that,[data]);}
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