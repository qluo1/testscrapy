define (
	['components/flight/lib/component','components/jquery/jquery'],

	function(defineComponent, $) {

		//
		return defineComponent(testComp);

		function testComp() {

			this.load = function() {
				alert("load");
			}

			this.onClick = function() {
				alert("inside onClick");
			}

			this.after('initialize',function ()

			{
				alert("initialized");
				this.on(document,"click", this.onClick);
			});

		} /* testComp */

	}
);