
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
      this.$el.html('<h2><span class="label label-' + label + '">' + this.model.get('name') + '</span></h2>');
      return this;
    }
  });

  var mod = {};
  mod.Player = Player;
  mod.Players = Players;
  mod.PlayerStatusView = PlayerStatusView;
  return mod;
}())