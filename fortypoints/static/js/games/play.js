$(document).ready(function() {
  var chatView = new CHAT.ChatView()
  var gameUpdater = new WebSocket('ws://' + location.host + '/game/update-stream/' + GAME_ID)
  console.log('foo')
  gameUpdater.onmessage = function(message) {
    console.log(message);
  };
});