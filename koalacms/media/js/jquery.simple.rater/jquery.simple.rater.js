/*
 * jQuery simple rater
 *
 * Copyright (c) 2008 Yılmaz Uğurlu, <yilugurlu@gmail.com>, http://www.2nci.com
 * Licensed under the MIT License:
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * $Version: 1.0, 2008.11.15, rev. 29
 */
 
(function($) {
  $.fn.rater = function(options){
    var defaults = {
      url: 'vote.php',
      enabled: true,
      favstar: false,
      favtitle: 'save as favorite',
      mediapath: '.',
      value: 0,
      indicator: true,
      callback: false
    };
    // işlem yapılan html elemanı
    var holder = $(this);
    // gelenle, varsayılanı birleştirelim
    var opts = $.extend(defaults, options);
    // problem çıkmaması için gelen parametreyi yuvarlayalım, düzenleyelim
    opts.value = Math.abs(Math.round(opts.value));
    opts.value = opts.value > 5 ? 5 : opts.value;
    var ratingui = ''; // içerik tutucu
    // yıldız biçimlendirmesi için css sınıfları
    var ratingcls = 'star_'+opts.value;
    // oy verme arayüzü için
    if(!opts.favstar)
    {
    	ratingui += '<ul class="rating '+ratingcls+'">';
	    for (var i = 1; i <= 5; i++) 
	    {
	    	if(opts.enabled)
	    	 ratingui += '<li class="s_'+i+'"><a href="#" title="'+i+'">'+i+'</a></li>';
	    	else
	    	 ratingui += '<li class="s_'+i+'"><span>'+i+'</span></li>';
	    }
    }
    else // favorilere ekleme arayüzü için
    {
    	ratingui += '<ul class="fav '+ratingcls+'"><li class="s_1">';
    	if(opts.enabled)
    	 ratingui += '<a href="#" title="'+opts.favtitle+'">'+(opts.value==1 ? 0 : 1)+'</a></li>';
      else
        ratingui += '<span>'+(opts.value==1 ? 0 : 1)+'</span></li>';
    }
    // indicator gösterilmek isteniyorsa
    if(opts.indicator && !opts.favstar)
      ratingui += '<li class="indicator"><img src="'+opts.mediapath+'indicator.gif" alt="loading" /></li>';
    
    ratingui += '</ul>';
    // oluşturulan arayüzü html içerisine gömelim    
    holder.html(ratingui);
    // yükleniyor animasyonunu gösterecek html elemanı
    var indicator = holder.find('ul > li.indicator');
    // yıldızlardan birine tıklandığında
    holder.find('ul > li > a').click(function(){
      var value  = $(this).html();
      // eğer bir callback fonksiyon atanmış ise
    	if(opts.callback != false)
    	{
    		opts.callback(value);
    		return false;
    	}
      
      // yükleniyor içeriği
      if(opts.indicator && !opts.favstar)
        indicator.show();
      // ajax üzerinden verilermizi post edelim
	  //$.post(opts.url,  { vote: value }, function(data){alert("Data Loaded: " + data);});
      $.post(opts.url,
        { vote: value },
        function(data){
        	// hide indicator
        	if(opts.indicator && !opts.favstar)
        	 indicator.hide();
			  }
			);
			// tıkladığımız yıldızın uzunuluğunu css sınıfları içerisinden seçelim
			var newcls = 'star_'+value;
			holder.find('ul').removeClass(ratingcls).addClass(newcls);
      ratingcls = newcls;
      // eğer favorilere ekleme yıldızı değilse, tüm elemanları devre dışı bırakalım
      if(!opts.favstar)
      {
      	$(holder.find('ul > li')).each(function(i){
      		if($(this).attr('class') != 'indicator') // if element is not indicator
	         $(this).html('<span>'+i+'</span>');
	      });
      }
      else
      {
      	$(this).html(value==1 ? '0' : '1');
      }
      
      return false;
    });
    
    return this;
  }
})(jQuery);

