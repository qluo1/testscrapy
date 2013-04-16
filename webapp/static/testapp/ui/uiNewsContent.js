/*jslint node: true */
'use strict';

define (['components/flight/lib/component'],
	function(defineComponent) {

		var newsContent = function (){

			this.defaultAttrs({
				newsSelector: '#news'
			});

			this.onNewsDataReady = function(e, data) {
				// alert(data.markup);
				this.$node.html(data.markup);
				this.$node.show();
			};

			this.after("initialize", function() {

				this.on(document,"onNewsDataReady",this.onNewsDataReady);
				//this.on("click", {});
			});

		};
		return defineComponent(newsContent);


	});

