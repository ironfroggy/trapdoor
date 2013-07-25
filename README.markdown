Trapdoor
========

Introduction
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

    /* Nodes begin life with no window, until you create one. */
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

See the `demos/` directory for these examples.


Nodes
-----

Trapdoor launches by initializing a `Node`, which houses a webkit renderer and
JS engine. There is no window, until the WindowManager.createWindow() is called
from inside a Node. This allows an application to sandbox different jobs.

The trapdoor.contrib.nodes plug-in provides a NodeManager extension, which can
allow one node to create others. Only nodes with the NodeManager extension can
do so, as only nodse with WindowManager can create windows for the user. This
security model allows control over code and even execution of 3rd party parts
safely.


Extensions
----------

The Calculator demo above showed a simple `Extension`, which is written in
Python and easily exposed to JavaScript. Creating fine grained extension types
allows easy control over what nodes have what permissions. Creating them is
very easy, consisting essentially of a decorated python class.

`@Extension.method(*types)` - Decorators a method on an Extension subclass as
callable by JavaScript. Supported types are currently int and str.

`@Extension.returns(type)` - Decorates the type returned by such a method and
should come *after* the method decorator. The type can be int, str, or any
Extension type.

Scripts
-------

Beside the extensions, every plugin can include javascript to inject into the
node. These can setup UI elements and event bindings, interact with extensions,
and are the heart of the application logic.

Plugins
-------

A plug-in is a python package that includes a manifest.yaml file. This lists
any extensions, scripts, and other plugins that should be included in a node.
Every node is created empty, and then enhanced with one or more plugins to
create the permissions and abilities applicable to its use.

# Example manifest

    extensions:
     - counter.Counters # Where counter.Counters is an Extension subclass
    js:
     - counterdemo.js
    plugins:
     - trapdoor.contrib.windowmanager
     - trapdoor.contrib.logging

