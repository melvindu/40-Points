CHAT = (function() {
  var mod = {};

FriendView = Backbone.View.extend({

    tagName: 'li',

    events: {
        'click #add-input':  'getFriend',
    },

    initialize: function() {
        this.friendslist = new FriendList;
        _.bindAll(this, 'render');
    }, 

    getFriend: function() {
        var friend_name = $('#input').val();
        this.friendslist.add( {name: friend_name} );
    },

    render: function( model ) {
        $("#friends-list").append("<li>"+ model.get("name")+"</li>");
        console.log('rendered')
    },

});

  var ChatView = Backbone.View.extend({
    el: '#chat',

    initialize: function() {
      WEBSOCKET.setupWebSocket(this, 'ws://localhost:5000/chat/game/9');
      this.on('socket:open', this.showConnected);
      this.on('socket:message', this.showChat);
      this.on('socket:close', this.showClosed);
      _.bindAll(this, 'render');
    },

    render: function(chatItem) {
        this.$el.find('.chats').append(chatItem);
        console.log('rendered');
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
        this.websocket.send($(keypress.target).val());
        $(keypress.target).val('');
        return false;
      }
    }
  });

  mod.ChatView = ChatView;
  return mod;
}());