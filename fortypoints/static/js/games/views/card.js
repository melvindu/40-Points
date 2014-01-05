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
      for (var index in this.model.get('cards')) {
        card = this.model.get('cards')[index]
        card_img = String(card.num) + String(card.suit) + '.jpg'
        src = location.origin + '/static/images/' + card_img
        cards.push('<li num="' + card.num + '" suit="' + card.suit + '">' + 
                    '<img src="' + src + '" alt="' + card_img + '" class="img-thumbnail card"></li>')
      }
      this.$el.html(cards.join(''))
      return this;
    }
  });

  var DrawView = Backbone.View.extend({
    el: '#draw-card',
    initialize: function() {
      _.bindAll(this, 'draw');
    },
    events: {
      'click': 'draw'
    },
    draw: function() {
      $.post(this.$el.attr('url'), function(data) {
        if (!data.status) {
          $('.game-alert').html('<div class="alert alert-warning">' + data.data + '</div>');
          $('.game-alert').show();
          $('.game-alert').delay(1000).fadeOut('slow');
        }
      });
      return this;
    }
  });

  var FlipView = Backbone.View.extend({
  el: '#flip-card',
  initialize: function() {
    _.bindAll(this, 'flip');
  },
  events: {
    'click': 'flip'
  },
  flip: function() {
    $.post(this.$el.attr('url'), {cards: [{num: 2, suit: 2}]}, function(data) {
      if (!data.status) {
        $('.game-alert').html('<div class="alert alert-warning">' + data.data + '</div>');
        $('.game-alert').show();
        $('.game-alert').delay(1000).fadeOut('slow');
      }
    });
    return this;
  }
});

  mod.HandView = HandView;
  mod.DrawView = DrawView;
  mod.FlipView = FlipView;
  return mod;
}());