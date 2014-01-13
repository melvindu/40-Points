
PLAYER = (function() {
  var Player = Backbone.Model.extend({
    urlRoot: '/player',
    initialize: function() {
    }
  });

  var Players = Backbone.Collection.extend({
    model: Player
  });

  var PlayerStatusView = Backbone.View.extend({
    tagName: 'span',
    initialize: function() {
      _.bindAll(this, 'render');
      this.model.on('change:active', this.render);
    },
    render: function() {
      var label = ''
      if (this.model.get('active')) {
        label = 'success'
      } else {
        label = 'danger'
      }
      if (this.model.get('name')){
        this.$el.html('<h2><span class="label label-' + label + '">' + this.model.get('name') + '</span></h2>');
      }
      return this;
    }
  });

  var CurrentPlayerView = Backbone.View.extend({
    tagName: 'span',
    initialize: function() {
      _.bindAll(this, 'render');
      this.collection.on('change:active', this.render);
    },

    render: function() {
      var view = this;
      this.collection.each(function(player) {
        if (player.get('active')) {
          view.$el.html('<h2>Turn: ' + player.get('name') + '<h2>');
        };
      });
      return this;
    }
  });

  var PlaysView = Backbone.View.extend({
     initialize: function() {
      _.bindAll(this, 'render');
      this.collection.on('change:play', this.render);
    },
    render: function() {
      var view = this;
      this.collection.each(function(player) {
        var view = $('.play[player_id="' + player.id + '"');
        var cards = []
        var src = ''
        var card = {}
        var card_img = ''
        for (var index in player.get('play')) {
          card = player.get('play')[index]
          card_img = String(card.num) + String(card.suit) + '.jpg'
          src = location.origin + '/static/images/' + card_img
          cards.push('<li class="card" num="' + card.num + '" suit="' + card.suit + '">' + 
            '<img src="' + src + '" alt="' + card_img + '" class="img-thumbnail card"></li>');
          $(view).html('<li class="card" num="' + card.num + '" suit="' + card.suit + '">' + 
            '<img src="' + src + '" alt="' + card_img + '" class="img-thumbnail card"></li>')
        }
      });
      return this;
    }
  });

  var mod = {};
  mod.Player = Player;
  mod.Players = Players;
  mod.PlayerStatusView = PlayerStatusView;
  mod.CurrentPlayerView = CurrentPlayerView;
  mod.PlaysView = PlaysView;
  return mod;
}())