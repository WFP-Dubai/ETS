function omit_enter(eventObject){
  if (eventObject.keyCode == "13")
    {
    return false;
    } 
}

(function($) {

  $.fn.loadIndicator = function(text) {
    //Append loader indicator
    var loader = $('<div class="loader">'+( text? '<div>'+text+'</div>' : '' )+'</div>');
    loader.height($(this).height());
    loader.width($(this).width());
    return $(this).before(loader).addClass('ajax-loading');
  };

  $.fn.deleteIndicator = function() {
    //Erase loader indicator
    $(this).removeClass('ajax-loading').prev('div.loader').remove();
  };
  
})(jQuery);
