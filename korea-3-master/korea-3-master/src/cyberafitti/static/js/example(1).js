
var any_text = ["하__하__ 이__ 착__한__ 친__구__는__ 개__뿔__ 개__ 병__신__새__끼__야__"];
var trigram_weights = [2.79722343e-07,3.49881102e-09,4.83404256e-06,4.59655985e-06
,6.47511627e-07,4.82076494e-08,1.73649787e-05,7.19956370e-06
,5.28936610e-08,1.01974714e-04,1.32498371e-06,8.46053561e-10
,2.51826826e-09,4.81616098e-06,1.17719230e-06,1.53636847e-05
,4.14287524e-06,2.19732356e-05,2.74537774e-06,5.61215359e-07
,3.12405817e-08,1.02193608e-05,2.70842679e-06,8.36312483e-06
,2.03598647e-05,4.96865340e-08,1.46964680e-07,4.43327532e-04
,2.22350587e-04,4.03618088e-07,2.41379053e-06,2.37262284e-04
,2.01294966e-07,1.56685728e-05,1.03675848e-04,2.82502297e-04
,1.58582588e-05,2.02453084e-04,1.85463301e-04,9.85134780e-01
,3.20105897e-07,4.18046788e-08,1.92963597e-07,1.26792097e-08
,2.05858669e-06,1.29193217e-02,4.90205650e-07,5.14439797e-08
,7.32107974e-09,1.43050343e-07];

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


