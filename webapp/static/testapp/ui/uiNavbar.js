define (
	['components/flight/lib/component','components/jquery/jquery'],

	function(defineComponent,$) {
		//
		return defineComponent(uiNavbar);

		function uiNavbar() {

			this.defaultAttrs({
				menuSelector: 	'#top_menu',
				bizSelector: 	'#biz',
				marketSelector: '#market',
				dataSelector: 	'#data',
				selectedClass: 	'active',
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

			this.onDataRec = function(data) {

				alert(data);
				// render UI ??
				this.trigger(document,"loadIndexData",{data:data})
			}

			this.bizSelected = function(e,data) {
				this.select('marketSelector').removeClass(this.attr.selectedClass);	
				this.select('dataSelector').removeClass(this.attr.selectedClass);	
				// highlight
				this.select('bizSelector').addClass(this.attr.selectedClass);	
				// load biz data
				var that = this;
				jQuery.ajax({
					url:"/get/business",
					method:"GET",
					data: "json",
					success : function(data) {
						that.onDataRec.apply(that,[data]);
					}

				});

			}

			this.marketSelected = function(e,data) {
				this.select('bizSelector').removeClass(this.attr.selectedClass);	
				this.select('dataSelector').removeClass(this.attr.selectedClass);	
				this.select('marketSelector').addClass(this.attr.selectedClass);	
				// load market data
			}

			this.dataSelected = function(e,data) {
				//
				this.select('marketSelector').removeClass(this.attr.selectedClass);	
				this.select('bizSelector').removeClass(this.attr.selectedClass);	
				this.select('dataSelector').addClass(this.attr.selectedClass);	
				//load data
			}


			this.after('initialize',function ()
			{	
				// default
				this.select('bizSelector').addClass(this.attr.selectedClass);
				//
				this.on("click", {
					bizSelector: this.bizSelected,
					marketSelector: this.marketSelected,
					dataSelector: this.dataSelected
				});

			});

		} /* uiNavbar */
	}
);
