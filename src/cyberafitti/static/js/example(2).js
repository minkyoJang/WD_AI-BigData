
        var any_text = ["__________________________________이__ 씳__빫__새__야__"];
var trigram_weights = [3.0323130e-04,1.4493885e-04,1.6639395e-04,3.8120386e-04,8.2687655e-04
,1.4165029e-03,1.9612862e-03,2.3813874e-03,2.6672881e-03,2.8350721e-03
,2.9217897e-03,2.9637890e-03,2.9859650e-03,3.0012687e-03,3.0147082e-03
,3.0273763e-03,3.0389673e-03,3.0490202e-03,3.0573099e-03,3.0638818e-03
,3.0689554e-03,3.0728050e-03,3.0757077e-03,3.0778938e-03,3.0795408e-03
,3.0807862e-03,3.0817327e-03,3.0824556e-03,3.0830011e-03,3.0834186e-03
,3.0837362e-03,3.0839818e-03,3.0841639e-03,3.0843024e-03,7.0988320e-02
,1.9804256e-03,6.9005386e-04,1.4296915e-01,2.3274498e-02,1.9098094e-03
,5.4443581e-04,9.6680976e-02,5.5268788e-01,1.3831164e-03,8.7841973e-04
,6.0860458e-04,1.8405559e-04,1.8478435e-02,2.5075270e-04,1.6027607e-04];

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


    