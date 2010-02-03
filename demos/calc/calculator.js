WindowManager.createWindow();


document.write('<input id="a" />');
document.write('<span> + </span>');
document.write('<input id="b" />');
document.write('<span> = </span>');
document.write('<input id="c" />');

function update() {
    var a = $('#a').val();
    var b = $('#b').val();
    $('#c').val(Calculator.add(a, b));
};

$('#a').keyup(update).focus();
$('#b').keyup(update);

$('#c').focus(function() { $('#a').focus(); });

