/*jslint node: true */
"use strict";

define (['components/flight/lib/component','testapp/template/templates'],
	function (defineComponent,templates) {
	
	var searchComp = function() {
		this.defaultAttrs({
			contentSelector : '#SearchContent',
			btnSelector : '.btn',
			searchTerms : 'input#q',
			searchItem : 'a'
		});

		this.onSearch = function(e,data) {
			this.$node.html("");
			if (data && data.markup) {
				this.$node.html(templates.searchForm);
				this.$node.append(data.markup);	
			}else {
				this.$node.html(templates.searchForm);
			}
			
		};

		this.onSubmit = function(e,data) {

			var terms = jQuery(this.attr.searchTerms).val();
			// alert("on submit: " + terms);
			this.trigger(document,"onSearchTerms", {terms: terms});
		};

		this.onItem = function(e,data) {
			alert("uiSearch click");
        	if (e.target && e.target.href){
                var _ref = e.target.href.split("#");
                this.trigger(document,"loadNewsData",{ref:_ref[_ref.length -1]}); 
                jQuery(e.target).addClass("visited");
            }
		};

		this.onHideSearch = function(e,data) {
			alert("onhidesearch");
			if (this.$node.html() !== ""){
				this.$node.html("");	
			}
		};

		this.after('initialize',function (){
			this.on(document,"onSearch",this.onSearch);
			this.on(document,"hideSearch",this.onHideSearch);
			this.on("click", { 
				btnSelector: this.onSubmit,
				searchItem: this.onItem
			} );

		});
	};

	return defineComponent(searchComp);

});
