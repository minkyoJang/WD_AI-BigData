document.write("<script src='blockURL_list.js'></script>");

let pattern = [
  "https://www.youtube.com/*",
  "https://www.twitch.tv/*",
  "http://www.afreecatv.com/*",
  "https://www.afreecatv.com/*",
  "http://bj.afreecatv.com/*",
  "http://vod.afreecatv.com/*",
  "https://play.afreecatv.com/*",
  "https://bj.afreecatv.com/*",
  "https://vod.afreecatv.com/*",
  "http://sbs.afreecatv.com/*",
  "https://sbs.afreecatv.com/*",
  "http://play.afreecatv.com/*",
  "https://play.afreecatv.com/*"
];

// blocking function
function redirect(requestDetails) {
    for (key in blockUrls) {
        if (requestDetails.url.indexOf(key) != -1) {
            return { cancel: true };
        }
    }
    return {
        redirectUrl: requestDetails.url
    };
}


chrome.webRequest.onBeforeRequest.addListener(
  redirect,
  { urls: pattern },
  ["blocking"]
);
