window.fbAsyncInit = function() {
  function checkLoginState() {
    FB.getLoginStatus(changeLoginState);
  }

  FB.init({
    appId      : '904320642985464',
    cookie     : true,
    xfbml      : true,
    version    : 'v2.5'
  });

  function changeLoginState(response) {
    if (response.status === 'connected') {
      FB.api('/me/picture?height=10000', function(response) {
        $('input[type="file"]').ezdz('preview', response.data.url);
        $('input[type="hidden"]').attr('value', response.data.url);
      });
      document.getElementById('status').innerHTML = 'Logged in!';
    } else if (response.status === 'not_authorized') {
      document.getElementById('status').innerHTML = 'Logged in to FB, not app.';
    } else {
      document.getElementById('status').innerHTML = 'Not logged into FB.';
    }
  }

  FB.getLoginStatus(changeLoginState);
};

(function(d, s, id){
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) {
    return;
  }
  js = d.createElement(s); js.id = id;
  js.src = "https://connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

$(document).ready(function() {
  $('input[type="file"]').ezdz({
    text: 'drop or click'
  });

  $('#fb-share').click(function() {
    var url = $('#fb-share').attr('data-url');

    FB.api('/me/photos', 'post', {
      url: url,
    }, function(response) {
      $('#fb-share').text('Submitted!');
      $('#fb-share').prop('disabled', true);
    });
  });

  $('#image-upload').submit(function(e) {
    e.preventDefault();
    $(this).ajaxSubmit({
      method: $(this).attr('method'),
      url: $(this).attr('action'),
      success: function(responseText, statusText, xhr, $form) {
        $('#after').attr('src', responseText);
        var href = window.location.href;
        var url = href.substring(0, href.length - 1) + responseText;
        var link = $('<a>', {
          href: url,
          text: url,
          title: 'Image',
        });
        $('#output-url').html(link);
        $('#fb-share').attr('data-url', url);
        $('#output').show();
      },
    });

    return false;
  });
});
