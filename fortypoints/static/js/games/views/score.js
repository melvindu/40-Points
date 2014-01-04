SCORE = (function() {
  var mod = {};


var ScoreView = Backbone.View.extend({
    tagName: 'span',
    initialize: function() {
        _.bindAll(this, 'render');
        this.model.on('change:score', this.render);
    },
    render: function() {
        this.$el.html('<b>' + this.model.get('name') + '</b>: ' + this.model.score);
        return this;
    }
});

  mod.ScoreView = ScoreView;
  return mod;
}());