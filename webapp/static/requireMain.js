requirejs.config({
    baseUrl: '/static',
    urlArgs: "bust=" + (new Date()).getTime()
});