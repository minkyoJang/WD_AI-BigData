function decode_utf8(s) {
    return decodeURIComponent(escape(s));
}

for_video_1 = decode_utf8('\xed\x95\xb4\xeb\x8b\xb9 \xec\x98\x81\xec\x83\x81\xec\x97\x90\xec\x84\x9c \xec\x9c\xa0\xed\x95\xb4\xeb\x8f\x84\xea\xb0\x80 ');
for_video_2 = decode_utf8(' \xea\xb2\x80\xec\xb6\x9c\xeb\x90\x98\xec\x97\x88\xec\x8a\xb5\xeb\x8b\x88\xeb\x8b\xa4.');

var repeat = setInterval(function () {
    for (key in blockUrls) {

        //Twitch click effect disabled

        $('div[data-a-target="search-result-video"] > a[href="' + key + '"]').parent('div').parent('div').parent('div').click(function () {
            return false;
        });
        //twitch search page videos disabled click event

        $('div[data-js-selector="carousel-content"] > div.preview-card > div.tw-relative > a[href="' + key + '"]').parent('div').parent('div').click(function () {
            return false;
        });
        //twitch bj channel page next video disabled click event


        //Twitch fadeout & hazard detection

        $('div[data-a-target="search-result-video"] > a[href="' + key + '"]').parent('div').parent('div').parent('div').delay(500).fadeOut(3000);
        //twitch search page fadeout
        $('div[data-a-target="search-result-video"] > div.tw-overflow-hidden > div.tw-pd-x-1 > div.tw-ellipsis > div.tw-flex > strong.tw-c-text-alt > a[href="' + key + '"]').replaceWith("<h2 style='color:red'>" + for_video_1 + blockUrls[key] + "%" + for_video_2 + "</h2>");
        //twitch search page show hazard

        $('div[data-js-selector="carousel-content"] > div.preview-card > div.tw-relative > a[href="' + key + '"]').parent('div').parent('div').delay(500).fadeOut(3000);
        //twitch bj channel page next video fadeout
        $('div[data-js-selector="carousel-content"] > div.preview-card > div.tw-flex.tw-flex-nowrap.tw-mg-t-1 > div.preview-card__titles-wrapper.tw-flex-grow-1 > div > a[href="' + key + '"] > h3.tw-ellipsis').replaceWith("<h2 style='color:red'>" + for_video_1 + blockUrls[key] + "%" + for_video_2 + "</h2>");
        //twitch bj channel page next video show hazard

    }
}, 1000);
