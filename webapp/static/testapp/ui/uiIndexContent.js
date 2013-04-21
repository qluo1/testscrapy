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
                contentSelector : '#IndexContent'
            });

            this.onDataRec = function(e,data) {
                // render UI ??
                // alert(data);
                this.$node.html("");
                this.$node.html(data.markup);
            }
            this.onClick = function(e,data) {
                if (e.target && e.target.href) {

                    var _ref = e.target.href.split("#");
                    this.trigger(document,"loadNewsData",{ref:_ref[_ref.length -1]}); 
                    jQuery(e.target).addClass("visited");
                } 
               
            }

            this.onHideIndex = function(e,data) {
                alert("onhideindex");

                if (this.$node.html() !== '') {
                    this.$node.html("");    
                }
            }

            this.after('initialize',function ()
            {   
                // default, load default content
                //
                this.on(document,"onIndexDataReady",this.onDataRec);

                this.trigger(document,"loadIndexData",{type:'business'});

                this.trigger(document,"hideIndex",this.onHideIndex);

                this.on("click",this.onClick);
            });

        } /* uiIndexContent */
    }
);