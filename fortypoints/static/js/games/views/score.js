SCORE = (function() {
  var mod = {};


var ScoreView = Backbone.View.extend({
    tagName: 'span',
    initialize: function() {
        _.bindAll(this, 'render');
        this.model.on('change:score', this.render);
    },
    render: function() {
      if (this.model.get('name')) {
        this.$el.html('<b>' + this.model.get('name') + '</b>: ' + this.model.get('score') + '<hr/>');
      }
      return this;
    }
});

var ScoreBoardView = Backbone.View.extend({
  initialize: function() {
    _.bindAll(this, 'render');
    _.bindAll(this, 'add');
    this.collection.on('add', this.add);
  },
  render: function() {
    return this;
  },

  add: function(model) {
    var scoreView = new ScoreView({model: model});
    this.$el.append(scoreView.el);
    scoreView.render()
    return this;
  }
})

  mod.ScoreView = ScoreView;
  mod.ScoreBoardView = ScoreBoardView;
  return mod;
}());