function decode_utf8(s) {
    return decodeURIComponent(escape(s));
}

for_video_1 = decode_utf8('\xed\x95\xb4\xeb\x8b\xb9 \xec\x98\x81\xec\x83\x81\xec\x97\x90\xec\x84\x9c \xec\x9c\xa0\xed\x95\xb4\xeb\x8f\x84\xea\xb0\x80 ');
for_video_2 = decode_utf8(' \xea\xb2\x80\xec\xb6\x9c\xeb\x90\x98\xec\x97\x88\xec\x8a\xb5\xeb\x8b\x88\xeb\x8b\xa4.');

setInterval(function () {
    for (key in blockUrls) {

        // Afreeca fadeout & hazard detection

        $('ul#vodSlider > li > div.cast_box > a[href*="' + key + '"]').parent('div').parent('li').delay(500).fadeOut(3000);
        //afreeca main page vod video fadeout
        $('ul#vodSlider > li > div.cast_box > a[href*="' + key + '"] > span.subject').replaceWith("<h2 class='subject' style='color:red'>" + for_video_1 + blockUrls[key] + "%" + for_video_2 + "</h2>");
        //afreeca main page vod video show hazard

        $('div.more_vod > ul > li > a[href*="' + key + '"]').parent('li').delay(500).fadeOut(3000);
        //afreeca main page vod-tab video fadeout
        $('div.more_vod > ul > li > a[href*="' + key + '"]').parent('li').find('div.information > span.link > a > strong').replaceWith("<h2 class='subject' style='color:red'>" + for_video_1 + blockUrls[key] + "%" + for_video_2 + "</h2>");
        //afreeca main page vod-tab video show hazard

        $('div#video_list > ul.vod_w > li > a[href*="' + key + '"]').parent('li').delay(500).fadeOut(3000);
        //afreeca search page vod video fadeout
        $('div#video_list > ul.vod_w > li > a[href*="' + key + '"] > span.tit').replaceWith("<h2 class='subject' style='color:red'>" + for_video_1 + blockUrls[key] + "%" + for_video_2 + "</h2>");
        //afreeca search page vod video show hazard

        $('ul#detailVideoPageList > li > div.tit > a[href*="' + key + '"]').parent('div').parent('li').delay(500).fadeOut(3000);
        //afreeca search page vod tap video fadeout
        $('ul#detailVideoPageList > li > div.tit > a[href*="' + key + '"] > span').replaceWith("<h2 class='subject' style='color:red'>" + for_video_1 + blockUrls[key] + "%" + for_video_2 + "</h2>");
        //afreeca search page vod tap video show hazard

        $('div.list_video  > div.bx-wrapper > div.bx-viewport > ul.video_list > li >  a[href*="' + key + '"]').parent('li').delay(500).fadeOut(3000);
        //afreeca vod -> E-sprot tap video fadeout
        $('div.list_video  > div.bx-wrapper > div.bx-viewport > ul.video_list > li >  a[href*="' + key + '"] > span.tit').replaceWith("<h2 class='subject' style='color:red'>" + for_video_1 + blockUrls[key] + "%" + for_video_2 + "</h2>");
        //afreeca vod -> E-sprot tap video fadeout

    }
}, 1000);


