WindowManager.createWindow();

var t = 500;

document.write('<input id="a" />' +
'<br />'+
'<input onclick="window.t = window.t - 100;" name="faster" value="faster" type="button" />'+
'<input onclick="window.t = window.t + 100;" name="slower" value="slower" type="button" />'+
'<input id="t" />');

function update() {
    $('#t').val(t);
    $('#a').val(Counter.get());
    Counter.incr();

    window.setTimeout(update, t);
}

window.setTimeout(update, t);
