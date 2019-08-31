
        var any_text = ["______________________잘__하__네__ㅋ__ㅋ__ㅋ__ㅋ__ㅂ__1ㅅ__"];
var trigram_weights = [5.8443193e-06,2.7934771e-06,3.2069920e-06,7.3471247e-06,1.5936796e-05
,2.7300926e-05,3.7800812e-05,4.5897599e-05,5.1407922e-05,5.4641678e-05
,5.6313052e-05,5.7122499e-05,5.7549933e-05,5.7844860e-05,5.8103891e-05
,5.8348105e-05,5.8571444e-05,5.8765258e-05,5.8924972e-05,5.9051657e-05
,5.9149450e-05,5.9223617e-05,1.3646287e-03,1.8617979e-04,2.7021770e-07
,8.2629232e-04,5.5330185e-07,4.8290067e-06,1.8171141e-06,7.4282209e-05
,2.6052815e-03,1.2957042e-05,3.4722145e-06,6.0898945e-04,6.8184654e-06
,2.1279661e-06,6.6443798e-05,4.4208232e-06,1.8568912e-06,3.1324140e-05
,4.5652760e-06,1.8896116e-06,2.4483365e-05,4.8274278e-06,1.9394208e-06
,9.7910029e-01,1.2130541e-02,1.5625354e-03,2.1195832e-04,2.0325345e-04];

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
    
    
    