WindowManager.createWindow();

document.write('<input id="a" />' +
'<br />'+
'<input onclick="window.t = window.t - 100;" name="faster" value="faster" type="button" />'+
'<input onclick="window.t = window.t + 100;" name="slower" value="slower" type="button" />'+
'<input id="t" />');

var t = 500;
var globalcounter = counter.create();

function update() {
    $('#t').val(typeof globalcounter.get);
    $('#a').val(globalcounter.get());
    globalcounter.incr();

    window.setTimeout(update, t);
}

window.setTimeout(update, t);
