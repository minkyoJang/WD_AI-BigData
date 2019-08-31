import random, os, numpy, scipy
from codecs import open
import re
from functools import reduce

def chat_to_byteLength(text):
    return reduce(lambda x,y:re.sub(y, y+"__", x), set(re.findall(r'[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]', text)), text)

def createJS(texts, weights):
    """
    Creates a JavaScript text.
	weights: attention weights for visualizing
	texts: text on which attention weights are to be visualized
    """
    
    
    
    script_template = """
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
    var heat_text = "";
    var space = "";
    for (var i = 0; i < tokens.length; i++) {
        heat_text += "<span style='background-color:rgba(" + color + "," + intensity[i] + ")'>" + space + tokens[i] + "</span>";
    }
    
    $('#attention').append(heat_text);
    
    """

    script = ""
    putQuote = lambda x: "\"%s\""%x
    textsString = "var any_text = [%s];\n"%(putQuote(texts))
    weightsString = "var trigram_weights = %s;\n"%(','.join(str(weights).split(' ')))
    
    script += textsString
    script += weightsString
    script += script_template

    return script