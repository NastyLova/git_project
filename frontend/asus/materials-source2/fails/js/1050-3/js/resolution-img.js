$.fn.dataImg = function(options) {

  var settings = $.extend({
    sml: 350,
    med: 700,
    lrg: 1050,
    resize: false
  }, options );

  var elements = $(this);

  function getSrc(element) {
    var screen = $(window).width();
    if (screen > settings.med) { 
        return element.data('lrg');
    }
    else if (screen <= settings.med && screen > settings.sml) {
        return element.data('med');
    }
    return element.data('sml');
  }

  function breakpoints() {
    elements.each(function () {
        var e = $(this);
        var src = getSrc(e);
        if(src != undefined){
            if (e.is('img')) {
                e.attr('src', src);
            } 
        }        
    });
  }breakpoints();

  if(settings.resize == true){
    $(window).resize(function(){
      breakpoints();
    });
  }

};