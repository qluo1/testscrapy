/*jslint node: true */
'use strict';

define (
    ['components/flight/lib/component','testapp/template/templates',
     'components/mustache/mustache'],

    function(defineComponent,templates,Mustache, underscore) {
        //
        return defineComponent(searchData);

        function searchData() {

            this.defaultAttrs({ });

            this.onIndexDataReady = function(data) {
                //
                var html = Mustache.to_html(templates.indexItem, {items:data});
                this.trigger(document,"onIndexDataReady",{markup: html});
            };

            this.onSearchDataReady = function(data,terms) {
                // alert(data);
                var html = Mustache.to_html(templates.indexItem, {items: data});
                this.trigger(document,"onSearch",{markup: html, term: terms});
            };

            this.onSearchData = function(e,data){
                //
                var that = this;
                // alert(data.terms);
                var terms = data.terms;
                jQuery.ajax({
                    url: "/search",
                    type: "POST",
                    dataType: "json",
                    data: {'terms': terms},
                    error: function(data) {alert("error");},
                    success: function(data) {
                        that.onSearchDataReady.apply(that,[data,terms]);
                    }
                });
            };
            
            this.after('initialize',function ()
            {   
                // default, load default content
                //
                this.on(document,"onSearchTerms",this.onSearchData);
            });

        } /* uiIndexContent */
    }
);