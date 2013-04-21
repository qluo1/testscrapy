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
                var html = Mustache.to_html(templates.searchItem,{items: data});
                this.trigger(document,"onSearch",{markup: html});
            };

            this.onSearchData = function(e,data){
                //
                var that = this;
                // alert(data.terms);
                jQuery.ajax({
                    url: "/search",
                    type: "POST",
                    dataType: "json",
                    data: {'terms': data.terms},
                    error: function(data) {alert("error");},
                    success: function(data) {
                        that.onSearchDataReady.apply(that,[data]);
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