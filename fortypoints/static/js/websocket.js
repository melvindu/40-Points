(function() {

  var setupWebSocket = function(backboneView, url) {
    var websocket = new WebSocket(url);
    websocket.onopen = function() {
      backboneView.trigger('socket:open');
    };
    websocket.onmessage = function() {
      backboneView.trigger('socket:message');
    };
    websocket.onerror = function() {
      backboneView.trigger('socket:error');
    };

    backboneView.websocket = websocket;
    backboneView.send = function(data) {
      backboneView.websocket.send(data);
    }
  }
}());