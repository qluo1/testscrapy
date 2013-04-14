define (
    ['components/flight/lib/component','components/mustache/mustache', 
     'testapp/templates','components/underscore-amd/underscore'],

    function(defineComponent,mustache,templates,underscore) {
        //
        return defineComponent(uiIndexContent);

        function uiIndexContent() {

            this.defaultAttrs({
                contentSelector : '#IndexContent'
            });

            // this.onClick = function() {
            //  alert("inside onClick");
            //  var that = this
            //  jQuery.ajax({
            //      url: "/get/fears-holden-job-cuts-flow-053542148.html",
            //      method: 'GET',
            //      dataType: 'json',
            //      success: function(data) {that.onDataRec.apply(that, data)}
            //  });

            //  this.trigger("custom_event",{key: "hello"})
            // }

            this.onDataRec = function(e,data) {

                // render UI ??
                alert(e.target);
                var markup = mustache.render(templates.indexItem,data);
                var temp = _.template(templates.indexItem);
                var html = temp({items:data.data});
                jQuery(this.attr.contentSelector).html(html);
            }



            this.after('initialize',function ()
            {   
                // default, load default content
                //
                this.on(document,"loadIndexData",this.onDataRec);

            });

        } /* uiIndexContent */
    }
);