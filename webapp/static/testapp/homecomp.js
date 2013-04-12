define (
	['components/flight/lib/component','components/jquery/jquery'],

	function(defineComponent,$) {
		//
		return defineComponent(homeComp);

		function homeComp() {

			this.defaultAttrs({
				menuSelector: 	'#top_menu',
				bizSelector: 	'#biz',
				marketSelector: '#market',
				dataSelector: 	'#data',
				selectedClass: 	'active',
				curr_actived: 	''
			});

			// this.onClick = function() {
			// 	alert("inside onClick");
			// 	var that = this
			// 	jQuery.ajax({
			// 		url: "/get/fears-holden-job-cuts-flow-053542148.html",
			// 		method: 'GET',
			// 		dataType: 'json',
			// 		success: function(data) {that.onDataRec.apply(that, data)}
			// 	});

			// 	this.trigger("custom_event",{key: "hello"})
			// }
			this.unselectmenu = function() {
				//this.$node.

			}

			this.bizSelected = function(e,data) {
				// alert("bizSelected");
				this.attr.curr_actived = this.attr.bizSelector;
				this.select('bizSelector').toggleClass(this.attr.selectedClass);
				// load biz data
			}

			this.marketSelected = function(e,data) {
				
				this.attr.curr_actived = this.attr.marketSelector;
				this.select('marketSelector').toggleClass(this.attr.selectedClass);
				// load market data
			}

			this.dataSelected = function(e,data) {
				//
				this.attr.curr_actived = this.attr.marketSelector;
				this.select('dataSelector').toggleClass(this.attr.selectedClass);
				//load data
			}


			this.after('initialize',function ()
			{	
				alert("initialize");
				//
				this.select('bizSelector').toggleClass(this.attr.selectedClass);
				//
				this.on("click", {
					bizSelector: this.bizSelected,
					marketSelector: this.marketSelected,
					dataSelector: this.dataSelected
				});
			});

		} /* homeComp */
	}
);