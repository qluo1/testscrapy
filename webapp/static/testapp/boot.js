'use strict';

define(

  [
    'testapp/homecomp',
  ],

  function(homecomp) {

    function initialize() {
      alert("attach to menu")
      homecomp.attachTo('#top_menu', {});
    }
    return initialize;
  }
);
