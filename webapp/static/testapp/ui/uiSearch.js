"use strict";

define (['components/flight/lib/component','testapp/template/templates'],
	function (defineComponent,templates) {
	
	var searchComp = function() {
		this.defaultAttrs({
			contentSelector : '#IndexContent',
			btnSelector : '.btn',
			searchTerms : 'input#q'
		});

		this.onSearch = function(e,data) {
			this.$node.html("");
			this.$node.html(templates.searchForm);
		};

		this.onSubmit = function(e,data) {

			var terms = jQuery(this.attr.searchTerms).val();
			// alert("on submit: " + terms);
			this.trigger(document,"onSearchTerms", {terms: terms})
		}

		this.after('initialize',function (){
			this.on(document,"onSearch",this.onSearch);
			this.on("click", { btnSelector: this.onSubmit} );

		});
	};

	return defineComponent(searchComp);

});
