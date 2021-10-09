(function() { 
    var sendMessage;
    sendMessage = $("#sendMessage");
sendMessage.keyup(function(e) {
    var $this, userMessage;
    if (e.shiftKey && e.which === 13) {
      e.preventDefault();
      return false;
    }
    $this = $(this);
    if (e.which === 13) {
      userMessage = sendMessage.val();
      sendMessage.val('');
      $('.chatwindow').append('<div class="msg-to msg"><p class="msg-text">'+userMessage+'</p></div>');
      return $('.chatwindow').animate({
        scrollTop: $('.chatwindow').prop("scrollHeight")
      }, 500);
    }
  }); 
}).call(this); 

