
PLAYER = (function() {
  var Player = Backbone.Model.extend({
    urlRoot: '/player',
    initialize: function() {
    }
  });

  var Players = Backbone.Collection.extend({
    model: Player
  });

  var mod = {};
  mod.Player = Player;
  mod.Players = Players;
  return mod;
}())