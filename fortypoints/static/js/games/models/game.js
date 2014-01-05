GAME = (function() {
  var Game = Backbone.Model.extend({
    urlRoot: '/game',
    initialize: function() {
    }
  });

  var GameStateView = Backbone.View.extend({
    tagName: 'span',
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
      this.$el.html('<h2><span class="game-state">' + state + '</span></h2>');
      return this;
    }
  });

  var mod = {};
  mod.Game = Game
  mod.GameStateView = GameStateView;
}())