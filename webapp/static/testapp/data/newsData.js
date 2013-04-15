define (
    ['components/flight/lib/component','testapp/template/templates','components/underscore-amd/underscore'],

    function(defineComponent,templates,underscore) {
        //
        return defineComponent(newsData);

        function newsData() {

            this.defaultAttrs({ });

            this.onIndexDataReady = function(data) {
                //
                alert(data);
                var temp = _.template(templates.indexItem);
                var html = temp({items:data});
                this.trigger("onIndexDataReady",{markup: html})
            }

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
            }

            this.after('initialize',function ()
            {   
                // default, load default content
                //
                this.on("loadIndexData",this.onIndexData);
            });

        } /* uiIndexContent */
    }
);