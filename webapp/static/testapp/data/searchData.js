/*jslint node: true */
'use strict';

define (
    ['components/flight/lib/component','testapp/template/templates',
     'components/mustache/mustache','components/underscore-amd/underscore'],

    function(defineComponent,templates,Mustache, underscore) {
        //
        return defineComponent(searchData);

        function searchData() {

            this.defaultAttrs({ });

            this.onIndexDataReady = function(data) {
                //
                // alert(data);
                var html = Mustache.to_html(templates.indexItem, {items:data});
                this.trigger(document,"onIndexDataReady",{markup: html});
            };

            this.onSearchDataReady = function(data) {

                // alert(data);
                var html = Mustache.to_html(templates.newsItem,data);
                this.trigger(document,"onSearchDataReady",{markup: html});
            };

            this.onSearchData = function(e,data) {
                //
                
                var that = this;
                jQuery.getJSON(url, function(data) {
                        that.onSearchDataReady.apply(that,[data]);
                 });

            };



            this.after('initialize',function ()
            {   
                // default, load default content
                //
                this.on(document,"onSearchData",this.onSearchData);
            });

        } /* uiIndexContent */
    }
);