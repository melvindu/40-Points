CHAT = (function() {
  var mod = {};

  var ChatView = Backbone.View.extend({
    initialize: function() {
      WEBSOCKET.setupWebSocket(this, 'ws://localhost:5000/chat/game/9');
      this.render();
    },

    render: function() {
      var template = _.template($("#chat").html(), {});
      this.$el.html(template);
    }
  });

  mod.ChatView = ChatView;
  return mod;
}());