function demo_src(value) {
    var temp = document.createElement("form");
    temp.action = value;
    temp.method = "post";
    temp.name = "src";
    temp.style.display = "none";
    document.body.appendChild(temp);
    temp.submit();
}


