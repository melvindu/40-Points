SCORE = (function() {
  var mod = {};

  var ScoreBoardView = Backbone.View.extend({
    el: '#scoreboard',

    initialize: function() {
      this.on('scoreboard:update', this.updateScore);
      _.bindAll(this, 'render');
    },

    render: function(){
      var template = _.template( $("#scoreboard").html(), {} );
      this.$el.html(template);
    },     

    updateScore: function(update) {
      this.$el.find('.scores').html(update.data);
      this.render();
    }
  });

  mod.ScoreBoardView = ScoreBoardView;
  return mod;
}());