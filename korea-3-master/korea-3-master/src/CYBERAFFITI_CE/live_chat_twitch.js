var text;

var priv = Math.floor(Math.random() * 100000) + 1;

let text_saver = [];

var repeat2 = setInterval(function () {


        $('div[data-a-target="right-column-chat-bar"] > div.tw-block > div.channel-root__right-column > div.room-selector > section[data-test-selector="chat-room-component-layout"] > div.chat-room__content > div.chat-list > div.chat-list__lines > div.simplebar-scroll-content > div.simplebar-content > div.tw-flex-grow-1 > div.chat-line__message > span.text-fragment').each(function () {

            if (text_saver.some(el =>  document.URL.includes(el))) {
            }
            else {
                text = document.URL;
                text_saver.push(text);
            }

            if (text_saver.length > 10000) {
                clearInterval(repeat2);
            }

            if (text_saver.some(el =>  $(this).text().includes(el))) {
            }
            else {
                text = $(this).text();
                text_saver.push(text);
                
                chrome.runtime.sendMessage({ private : priv, url: text_saver[0], chat: text });
            }
        });
}, 1000);
