var CHAT = (function() {

  var ChatView = Backbone.View.extend({
    initialize: function() {
      //setupWebSocket(this);
      this.render();
    },

    render: function() {
      var template = _.template($("#chat").html(), {});
      this.$el.html(template);
    }
  });

}());