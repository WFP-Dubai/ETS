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


function getDataFromTable( oTable, format ) {
    var oSettings = oTable.fnSettings();
    aoData = oTable._fnAjaxParameters( oSettings );
    aoData.push( { "name": "data_format", "value": format } );
    oSettings.fnServerData.call( oSettings.oInstance, oSettings.sAjaxSource, aoData, function(json) {
        window.location = json.redirect_url;
        return false;
    }, oSettings );
};
