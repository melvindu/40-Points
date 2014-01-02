CHAT = (function() {
  var mod = {};

  var ChatView = Backbone.View.extend({
    initialize: function() {
      WEBSOCKET.setupWebSocket(this, 'ws://localhost:5000/chat/game/9');
      this.render();
      this.on('socket:open', this.showConnected);
      this.on('socket:message', this.showChat);
      this.on('socket:close', this.showClosed);
    },
    render: function() {
      var template = _.template($("#chat").html(), {});
      this.$el.html(template);
    },
    events: {
    },

    showConnected: function() {

    },

    showChat: function(message) {
      $(this.el).find('.chats').append(message.data);
      this.render()
    },

    showClosed: function() {

    }
  });

  mod.ChatView = ChatView;
  return mod;
}());