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
				alert(data);
			}

			this.onClick = function() {
				alert("inside onClick");
				jQuery.ajax({
					url: "/get/fears-holden-job-cuts-flow-053542148.html",
					method: 'GET',
					dataType: 'json',
					success: this.onDataRec
				});
			}

			this.after('initialize',function ()

			{
				alert("initialized");
				this.on(document,"click", this.onClick);
			});

		} /* testComp */

	}
);