/*jslint node: true */
'use strict';

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
				searchSelector: '#search',
				selectedClass: 	'active',
			});


			this.bizSelected = function(e,data) {
				this.select('marketSelector').removeClass(this.attr.selectedClass);	
				this.select('dataSelector').removeClass(this.attr.selectedClass);
				this.select('searchSelector').removeClass(this.attr.selectedClass);
				// highlight
				this.select('bizSelector').addClass(this.attr.selectedClass);
				//
				this.trigger(document,"hideSearch",{});
				// load market data
				this.trigger("loadIndexData",{type: 'business'});

			}

			this.marketSelected = function(e,data) {
				this.select('bizSelector').removeClass(this.attr.selectedClass);	
				this.select('dataSelector').removeClass(this.attr.selectedClass);
				this.select('searchSelector').removeClass(this.attr.selectedClass);
				// highlight
				this.select('marketSelector').addClass(this.attr.selectedClass);
				// 
				// load market data
				this.trigger(document,"loadIndexData",{type: 'market'});				
			}

			this.dataSelected = function(e,data) {
				//
				this.select('marketSelector').removeClass(this.attr.selectedClass);
				this.select('bizSelector').removeClass(this.attr.selectedClass);
				this.select('searchSelector').removeClass(this.attr.selectedClass);
				this.select('dataSelector').addClass(this.attr.selectedClass);
				//load data
				this.trigger(document,"hideSearch",{});			
				this.trigger(document,"loadIndexData",{type: 'market'});
			}

			this.searchSelected = function(e,data) {
				this.select('marketSelector').removeClass(this.attr.selectedClass);
				this.select('bizSelector').removeClass(this.attr.selectedClass);
				this.select('dataSelector').removeClass(this.attr.selectedClass);
				//
				this.select('searchSelector').addClass(this.attr.selectedClass);
				//
				this.trigger(document,"onSearch",{});
			}
			this.after('initialize',function ()
			{	
				// default
				this.select('bizSelector').addClass(this.attr.selectedClass);
				//
				this.on("click", {
					bizSelector: this.bizSelected,
					marketSelector: this.marketSelected,
					dataSelector: this.dataSelected,
					searchSelector: this.searchSelected
				});

			});

		} /* uiNavbar */
	}
);
