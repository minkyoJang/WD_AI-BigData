
        var any_text = ["______싹__둑__이__는__ 프__로__그__램__이__야__ 빡__다__갤__아__"];
var trigram_weights = [9.8336318e-07,4.7002905e-07,5.3960684e-07,1.2362235e-06,2.6815148e-06
,4.5936445e-06,1.4846571e-04,2.8259281e-04,1.7220747e-04,9.6412536e-05
,8.3343893e-06,1.7176429e-06,4.2530928e-06,9.7773800e-06,1.0577400e-06
,4.9945593e-06,7.1366719e-04,3.8047605e-05,2.3558385e-04,4.9147214e-04
,8.3861496e-06,1.1302336e-06,1.4249827e-06,4.1885924e-06,2.5453017e-08
,3.5657437e-04,3.1122330e-05,6.3829291e-05,1.2501249e-07,6.5878499e-05
,9.0947225e-08,1.6371063e-05,5.5280670e-06,1.6997702e-06,2.3739490e-04
,7.4152261e-08,5.1495713e-06,1.4476079e-04,1.9824880e-07,5.6658633e-04
,1.0306133e-03,4.3956460e-03,9.8281866e-01,1.0038358e-04,7.8265006e-03
,2.5250797e-06,4.6630125e-06,8.2768405e-05,3.1671914e-07,8.2770821e-06];

    var color = "255,0,0";
    var ngram_length = 9;
    var half_ngram = 3;


    var tokens = any_text[0];
    var intensity = new Array(tokens.length);
    var max_intensity = Number.MIN_SAFE_INTEGER;
    var min_intensity = Number.MAX_SAFE_INTEGER;

    for (var i = 0; i < intensity.length; i++) {
        intensity[i] = 0.0;

        for (var j = -half_ngram; j < ngram_length-half_ngram; j++) {
            if (i+j < intensity.length && i+j > -1) {
                intensity[i] += trigram_weights[i + j];
            }
        }
        if (i == 0 || i == intensity.length-1) {
            intensity[i] /= 6.0;
        } else {
            intensity[i] /= 9.0;
        }
        if (intensity[i] > max_intensity) {
            max_intensity = intensity[i];
        }
        if (intensity[i] < min_intensity) {
            min_intensity = intensity[i];
        }
    }
    var denominator = max_intensity - min_intensity;
    for (var i = 0; i < intensity.length; i++) {
        intensity[i] = (intensity[i] - min_intensity) / denominator;
    }
    var heat_text = "<p>";
    var space = "";
    for (var i = 0; i < tokens.length; i++) {
        heat_text += "<span style='background-color:rgba(" + color + "," + intensity[i] + ")'>" + space + tokens[i] + "</span>";
    }
    heat_text += "</p>"
    $('#attention').prepend(heat_text);


