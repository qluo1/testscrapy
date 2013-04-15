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


			this.bizSelected = function(e,data) {
				this.select('marketSelector').removeClass(this.attr.selectedClass);	
				this.select('dataSelector').removeClass(this.attr.selectedClass);	
				// highlight
				this.select('bizSelector').addClass(this.attr.selectedClass);
				this.trigger(document,"loadIndexData",{});

			}

			this.marketSelected = function(e,data) {
				this.select('bizSelector').removeClass(this.attr.selectedClass);	
				this.select('dataSelector').removeClass(this.attr.selectedClass);	
				this.select('marketSelector').addClass(this.attr.selectedClass);	
				// load market data
				this.trigger(document,"loadIndexData",{});				
			}

			this.dataSelected = function(e,data) {
				//
				this.select('marketSelector').removeClass(this.attr.selectedClass);	
				this.select('bizSelector').removeClass(this.attr.selectedClass);	
				this.select('dataSelector').addClass(this.attr.selectedClass);	
				//load data
				this.trigger(document,"loadIndexData",{});
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
