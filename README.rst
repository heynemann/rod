Introduction
============

rod is an http server for you to use in your tests.

Usage
=====

@with_rod
def test_something(rod):
    rod.say(method="GET",
            url="/hello.html",
            body="Hello World")

    contents = urlopen('http://localhost:%d/hello.html' % rod.port).read()
    assert contents == 'Hello World'
