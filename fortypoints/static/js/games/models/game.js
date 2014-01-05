GAME = (function() {
  var Game = Backbone.Model.extend({
    urlRoot: '/game',
    initialize: function() {
    }
  });

  var GameStateView = Backbone.View.extend({
    tagName: 'h2',
    initialize: function() {
      _.bindAll(this, 'render');
      this.model.on('change:state', this.render);
    },
    render: function() {
      var state = this.model.get('state');
      if (state == 0) {
        state = 'DRAW';
      } else if (state == 1) {
        state = 'COVER';
      } else if (state == 2) {
        state = 'PLAY'
      } else if (state == 3) {
        state = 'COMPLETE'
      }
      if (typeof this.model.get('state') != 'undefined') {
        this.$el.html('<span class="label label-info">' + state + '</span>');
      }
      return this;
    }
  });

  var TrumpView = Backbone.View.extend({
    tagName: 'h2',
    initialize: function() {
      _.bindAll(this, 'render');
      this.model.on('change:trump_number', this.render);
      this.model.on('change:trump_suit', this.render);
    },
    render: function() {
      var number = String(this.model.get('trump_number'));
      this.$el.html(number + ' <span style="color:lightgray">of</span> ');
      if (typeof this.model.get('trump_suit') != 'undefined' && this.model.get('trump_suit') != null) {
        var suit_src = '/static/images/' + String(this.model.get('trump_suit')) + '.png';
        this.$el.append('<img src="' + suit_src + '" alt="' + suit_src + '" class="img-rounded trump-suit">');
      } else {
        this.$el.append('?');
      }
      return this;
    }
  });

  var mod = {};
  mod.Game = Game;
  mod.GameStateView = GameStateView;
  mod.TrumpView = TrumpView;
  return mod;
}())