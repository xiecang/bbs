var log = function() {
    console.log(arguments)
}

var content_show = function() {
    var text = document.getElementById("content").innerText;
    var converter = new showdown.Converter();
    var html = converter.makeHtml(text);
    document.getElementById("content-show").innerHTML = html;
}

window.onload = function() {
    content_show();
}
