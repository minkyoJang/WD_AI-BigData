function decode_utf8(s) {
    return decodeURIComponent(escape(s));
}

for_video_1 = decode_utf8('\xed\x95\xb4\xeb\x8b\xb9 \xec\x98\x81\xec\x83\x81\xec\x97\x90\xec\x84\x9c \xec\x9c\xa0\xed\x95\xb4\xeb\x8f\x84\xea\xb0\x80 ');
for_video_2 = decode_utf8(' \xea\xb2\x80\xec\xb6\x9c\xeb\x90\x98\xec\x97\x88\xec\x8a\xb5\xeb\x8b\x88\xeb\x8b\xa4.');


setInterval(function () {
    for (key in blockUrls) {

        //Youtube fadeout & hazard detection

        $('div#dismissable.style-scope.ytd-video-renderer > ytd-thumbnail > a[href*="' + key + '"]').parent('ytd-thumbnail').parent('div').delay(500).fadeOut(3000);
        //youtube search page fadeout
        $('div#dismissable.style-scope.ytd-video-renderer > div.text-wrapper > div#meta > div#title-wrapper > h3 > a[href*="' + key + '"]').replaceWith("<h2 style='color:red'>" + for_video_1 + blockUrls[key] + "%" + for_video_2 + "</h2>");
        //youtube search page show hazard

        $('div#dismissable.style-scope.ytd-grid-video-renderer > ytd-thumbnail > a[href*="' + key + '"]').parent('ytd-thumbnail').parent('div').delay(500).fadeOut(3000);
        //youtube main page fadeout
        $('div#dismissable.style-scope.ytd-grid-video-renderer > div#details > div#meta > h3 > a[href*="' + key + '"]').replaceWith("<h2 style='color:red'>" + for_video_1 + blockUrls[key] + "%" + for_video_2 + "</h2>");
        //youtube main page show hazard

        $('div#dismissable.style-scope.ytd-compact-video-renderer > ytd-thumbnail > a[href*="' + key + '"]').parent('ytd-thumbnail').parent('div').delay(500).fadeOut(3000);
        //youtube next video list fadeout
        $('div#dismissable.style-scope.ytd-compact-video-renderer > div.metadata > a[href*="' + key + '"] > h3.style-scope > span#video-title').replaceWith("<h2 style='color:red'>" + for_video_1 + blockUrls[key] + "%" + for_video_2 + "</h2>");
        //youtube next video show hazard

    }
}, 1000);


