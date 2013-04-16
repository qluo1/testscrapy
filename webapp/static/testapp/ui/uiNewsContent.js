/*jslint node: true */
'use strict';

define (['components/flight/lib/component'],
	function(defineComponent) {

		var newsContent = function (){

			this.defaultAttrs({
				newsSelector: '#news',
				btnCloseSelector: '.close',
				btnSelector: '.btn' 
			});

			this.onNewsDataReady = function(e, data) {
				// alert(data.markup);
				this.$node.html(data.markup);
				this.$node.show();
			};

			this.onClose = function(e,data) {
				// alert(e.target);
				if (e.target && e.target.className === 'close') this.$node.html("").hide();
				if (e.target) {
					var ref = e.target.href.split("#");
					if (ref[ref.length -1] === 'close') {
						this.$node.html("").hide();
					}else {
						alert(ref[ref.length -1]);
					}
				}
			};

			this.onEscape = function(e,data){
				if (e && e.keyCode && e.keyCode === 27) this.$node.html("").hide();
			};

			this.after("initialize", function() {

				this.on(document,"onNewsDataReady",this.onNewsDataReady);
				this.on("click", {
					btnSelector: this.onClose,
					btnCloseSelector : this.onClose

				});
				this.on(document,"keyup",this.onEscape);
			});

		};
		return defineComponent(newsContent);

	});

