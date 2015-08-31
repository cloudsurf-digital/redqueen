// Initialize your app
var myApp = new Framework7({
    animateNavBackIcon:true
});

// Export selectors engine
var $$ = Dom7;

// Add main View
var mainView = myApp.addView('.view-main', {
    // Enable dynamic Navbar
    dynamicNavbar: true,
    // Enable Dom Cache so we can use all inline pages
    domCache: true
});

$$('form.ajax-submit-onchange').on('beforeSubmit', function (e) {
  var xhr = e.detail.xhr; // actual XHR object
 
  var data = e.detail.data; // Ajax repsonse from action file
  // do something with response data
});
