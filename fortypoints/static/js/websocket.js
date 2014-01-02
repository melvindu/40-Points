WEBSOCKET = (function() {
  var mod = {};

  var setupWebSocket = function(backboneView, url) {
    var websocket = new WebSocket(url);
    websocket.onopen = function() {
      backboneView.trigger('socket:open');
    };
    websocket.onmessage = function(message) {
      backboneView.trigger('socket:message', message);
    };
    websocket.onerror = function(error) {
      backboneView.trigger('socket:error', error);
    };
    websocket.onclose = function() {
      backboneView.trigger('socket:close');
    };

    backboneView.websocket = websocket;
  }

  mod.setupWebSocket = setupWebSocket;
  return mod;
}());