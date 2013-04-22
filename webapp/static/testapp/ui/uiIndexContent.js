/*jslint node: true */
'use strict';

define (
    ['components/flight/lib/component','components/mustache/mustache', 
     'testapp/template/templates','components/underscore-amd/underscore'],

    function(defineComponent,mustache,templates,underscore) {
        //
        return defineComponent(uiIndexContent);

        function uiIndexContent() {

            this.defaultAttrs({
                contentSelector : '#IndexContent',
                linkSelector : 'a',
                btnSelector : '.btn',
                searchTerms : 'input#q'
            });

            this.onDataRec = function(e,data) {
                // render UI ??
                // alert(data);
                this.$node.html("");
                this.$node.html(data.markup);
            };

            this.onClick = function(e,data) {
                if (e.target && e.target.href) {

                    var _ref = e.target.href.split("#");
                    this.trigger(document,"loadNewsData",{ref:_ref[_ref.length -1]}); 
                    jQuery(e.target).addClass("visited");
                } 
            };

        /* search */
        this.onSearch = function(e,data) {
            this.$node.html("");
            if (data && data.markup) {
                this.$node.html(templates.searchForm);
                this.$node.append(data.markup);
            }else {
                this.$node.html(templates.searchForm);
            }
        };

        this.onSubmit = function(e,data) {
            var terms = jQuery(this.attr.searchTerms).val();
            // alert("on submit: " + terms);
            this.trigger(document,"onSearchTerms", {terms: terms});
        };

        /* initializ */
        this.after('initialize',function ()
        {   
            // default, load default content
            //
            this.on(document,"onIndexDataReady",this.onDataRec);
            this.on(document,"onSearch",this.onSearch);
            
            this.on("click", {
                linkSelector:  this.onClick,
                btnSelector: this.onSubmit,
             } );

            // load default pages
            this.trigger(document,"loadIndexData",{type:'business'});
        });

        } /* uiIndexContent */
    }
);