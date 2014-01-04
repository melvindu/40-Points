CARD = (function() {
  var mod = {};


var HandView = Backbone.View.extend({
    tagName: 'span',
    initialize: function() {
        _.bindAll(this, 'render');
        this.model.on('change:cards', this.render);
    },
    render: function() {
      var cards = []
      var src = ''
      var card = {}
      var card_img = ''
      console.log(this.model)
      for (var index in this.model.get('cards')) {
        card = this.model.get('cards')[index]
        card_img = card.num + card.suit + '.jpg'
        src = location.origin + '/static/images/' + card_img
        cards.push('<li><img src="' + src + '" alt="' + card_img + '" class="img-thumbnail card"></li>')
      }
      console.log(cards.join(''))
      this.$el.html(cards.join(''))
      return this;
    }
});

  mod.HandView = HandView;
  return mod;
}());