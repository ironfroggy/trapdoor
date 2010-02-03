Trapdoor
========

Intrdocution
------------

Trapdoor is a web-based desktop framework. Confused yet?
The idea is to leverage how much energy is put into the
web today and make developing a desktop application *fun*
again. Again? For the first time?

*   Modular. Trapdoor projects are split into plugins,
    where each plugin can provide *extensions* and *scripts*.
*   Extensions. A dirt simple Python API exposes new APIs
    to JavaScript.
*   Scripts. All the jQuery we know and love can be used to
    build UIs using all the tried and true webkit-powered
    experiences.

Example
-------

This is the calculator demo. It provides two inputs in an
HTML form, using jQuery to ask Python to add them. Stupid,
but gives the idea.

# calculator.py - the extension library

    from trapdoor.extension import Extension

    class Calculator(Extension):

        @Extension.method(int, int)
        @Extension.returns(int)
        def add(self, a, b):

            # For now, this is needed because of trickiness
            # with PyQt4 + our decorators. Sorry :-(
            self._result = a + b

# calculator.js - the script

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

See the `demos/` directory for these examples.
