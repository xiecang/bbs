var log = function() {
    console.log(arguments)
}

var markdown_preview = function() {
    document.getElementById("markdown-preview").style.display = "block";
    markdown_convert()
}

var markdown_convert = function() {
    var text = document.getElementById("content").value;
    var converter = new showdown.Converter();
    var html = converter.makeHtml(text);
    document.getElementById("markdown-preview").innerHTML = html;
}
