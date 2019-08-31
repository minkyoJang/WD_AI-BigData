function attention(query, padded, trigram_weights){
    var any_text =query;
        var padded = padded;
        var trigram_weights = trigram_weights;
        var color = "255,0,0";
        var ngram_length = 3;
        var half_ngram = 1;
        var tokens = any_text.split(" ");
        var intensity = new Array(tokens.length);
        var max_intensity = Number.MIN_SAFE_INTEGER;
        var min_intensity = Number.MAX_SAFE_INTEGER;
        for (var i = 0; i < intensity.length; i++) {
            intensity[i] = 0.0;
            for (var j = -half_ngram; j < ngram_length - half_ngram; j++) {
                if (i + j < intensity.length && i + j > -1) {
                    intensity[i] += trigram_weights[i + j];
                }
            }
            if (i == 0 || i == intensity.length - 1) {
                intensity[i] /= 2.0;
            } else {
                intensity[i] /= 3.0;
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
            if (space == "") {
                space = " ";
            }
        }
        heat_text += "</p>";
        console.log("heat_text = "+heat_text);
        $("#attention").append( heat_text);
};