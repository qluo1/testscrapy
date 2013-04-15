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
                jQuery(this.attr.contentSelector).html(data.markup);
            }

            this.after('initialize',function ()
            {   
                // default, load default content
                //
                this.on(document,"onIndexDataReady",this.onDataRec);

                this.trigger(document,"loadIndexData",{});
            });

        } /* uiIndexContent */
    }
);