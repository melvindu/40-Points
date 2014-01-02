CHAT = (function() {
  var mod = {};

  var ChatView = Backbone.View.extend({
    el: '#chat',

    initialize: function() {
      WEBSOCKET.setupWebSocket(this, 'ws://' + location.host + '/chat/game/' + GAME_ID);
      this.on('socket:open', this.showConnected);
      this.on('socket:message', this.showChat);
      this.on('socket:close', this.showClosed);
      _.bindAll(this, 'render');
    },

    render: function(chatItem) {
      this.$el.find('.chats').append(chatItem );
    },

    events: {
      'keypress .chat-input': 'sendChat'
    },

    showConnected: function() {

    },

    showChat: function(message) {
      this.render(message.data);
      $('.chats').scrollTop($('.chats')[0].scrollHeight - $('.chats').height());
    },

    showClosed: function() {

    },

    sendChat: function(keypress) {
      if (keypress.which == 13) {
        this.websocket.send(JSON.stringify({
          user: USER,
          message: $(keypress.target).val()
        }));
        $(keypress.target).val('');
        return false;
      }
    }
  });

  mod.ChatView = ChatView;
  return mod;
}());