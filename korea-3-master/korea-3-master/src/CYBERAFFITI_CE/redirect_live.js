var count_temp = 0;
var a;

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    console.log(request);
    request = JSON.stringify(request);
    $.ajax({
        url: "http://150.95.153.18:8000/mandoo",
        type: "POST",
        data: { "chat" : request},
        success: function (response) {
            console.log(response);
            if (response != 'N') {
                count_temp += 1;
                obj = JSON.parse(response);
                if (JSON.stringify(a) != JSON.stringify(Object.keys(obj))) {
                    count_temp = 1;
                }
                a = Object.keys(obj);
                b = Object.values(obj);
                blockUrls[a] = b;
                setTimeout(
                    function () {
                        chrome.tabs.getSelected(null, function (tab) {
                            var code = 'window.location.reload();';
                            chrome.tabs.executeScript(tab.id, { code: code });
                        });
                    }, 4000);
                if (count_temp < 2) {
                    alert("해당 영상에서 유해도 " + b + "% 검출되었습니다.");
                }
            }
        },
    });
    
});

