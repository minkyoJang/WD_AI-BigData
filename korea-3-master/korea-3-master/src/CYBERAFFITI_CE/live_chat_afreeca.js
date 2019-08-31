var text2;

var priv2 = Math.floor(Math.random() * 100000) + 1;

let text_saver2 = [];

var repeat3 = setInterval(function () {


    $('div#webplayer > div#webplayer_scroll > div#webplayer_contents > div#chatting_area > div#chatbox > div#chat_area > dl > dd').each(function () {

        if (text_saver2.some(el =>  document.URL.includes(el))) {
        }
        else {
            text2 = document.URL;
            text_saver2.push(text2);
        }

        if (text_saver2.length > 10000) {
            clearInterval(repeat3);
        }

        if (text_saver2.some(el =>  $(this).text().includes(el))) {
        }
        else {
            text2 = $(this).text();
            text_saver2.push(text2);

            chrome.runtime.sendMessage({ private: priv2, url: text_saver2[0], chat: text2 });
        }
    });
}, 1000);
