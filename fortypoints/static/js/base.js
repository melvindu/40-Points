jQuery.fn.scrollBottom = function() {
  $(this).scrollTop($(this)[0].scrollHeight - $(this).height());
};
