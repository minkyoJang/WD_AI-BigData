
        var any_text = ["_____________________ㅂ__1ㅅ__ㅋ__ㅋ__ㅋ__ㅋ__ 잘__하__네__"];
var trigram_weights = [6.5338550e-06,3.1230595e-06,3.5853620e-06,8.2139595e-06,1.7817047e-05
,3.0521998e-05,4.2260657e-05,5.1312727e-05,5.7473175e-05,6.1088518e-05
,6.2957028e-05,6.3861975e-05,6.4339838e-05,6.4669570e-05,6.4959211e-05
,6.5232118e-05,6.5481938e-05,6.5698485e-05,6.5877110e-05,6.6018743e-05
,6.6128072e-05,1.8746563e-05,2.8224342e-06,9.5033371e-01,1.4893106e-02
,2.0708407e-03,4.4983256e-04,3.9190927e-04,1.1340775e-02,1.0934055e-02
,1.0534308e-03,1.5968182e-04,8.5768371e-04,2.5134355e-05,2.3220642e-05
,2.1804104e-05,8.6235705e-06,1.0925903e-05,5.2100781e-06,1.3796022e-05
,1.3274783e-03,8.1740244e-04,7.9486083e-04,1.2882653e-07,5.5673020e-04
,8.9474173e-07,4.0501554e-06,1.5940520e-06,8.3164166e-05,2.8011887e-03];

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
    var heat_text = "<p>"
    var space = "";
    for (var i = 0; i < tokens.length; i++) {
        heat_text += "<span style='background-color:rgba(" + color + "," + intensity[i] + ")'>" + space + tokens[i] + "</span>";
    }
    heat_text += "</p>"
    $('#attention').prepend(heat_text);
    
    
    