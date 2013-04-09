define (
	['components/flight/lib/component','components/jquery/jquery'],

	function(defineComponent,jquery) {

		//
		return defineComponent(testComp);

		function testComp() {

			this.load = function() {
				alert("load");
			}

			this.onDataRec = function(data) {
				
				this.trigger("custom_event",{key: "world"})
				alert("on Data Rec");
			}

			this.on_cust_event = function(event, data) {

				alert("on cust event" + data.key)
			}

			this.onClick = function() {
				alert("inside onClick");
				var that = this
				jQuery.ajax({
					url: "/get/fears-holden-job-cuts-flow-053542148.html",
					method: 'GET',
					dataType: 'json',
					success: function(data) {that.onDataRec.apply(that, data)}
				});

				this.trigger("custom_event",{key: "hello"})
			}

			this.after('initialize',function ()

			{
				alert("initialized");
				this.on(document,"click", this.onClick);
				this.on(document,"custom_event",this.on_cust_event);
			});

		} /* testComp */

	}
);