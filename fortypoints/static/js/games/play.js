$(document).ready(function() {
  var chatView = new CHAT.ChatView()
  var views = [chatView]
  var gameUpdater = new WebSocket('ws://' + location.host + '/game/update-stream/' + GAME_ID)

  gameUpdater.onmessage = function(message) {
    for (index in views) {
      views[index].trigger(message.data.event);
    }
  };

  window.onbeforeunload = function() {
    gameUpdater.close()
  };
});