// Facebook sharer code
window.fbAsyncInit = function() {
  FB.init({
    appId      : '206165553087422',
    xfbml      : true,
    version    : 'v2.5'
  });
};

(function(d, s, id){
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement(s); js.id = id;
   js.src = '//connect.facebook.net/en_US/sdk.js';
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));

// Event handler for share link
window.onload = function() {
  var a = document.getElementById('fbshare');

  a.onclick = function() {
    FB.ui({
     method: 'share',
     href: a.href,
     }, function(response){});

     return false;
   };
 };
