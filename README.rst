Introduction
============

rod is an http server for you to use in your tests.

Usage
=====

Using it is really simple::

    @with_rod
    def test_something(rod):
        rod.say(method="GET",
                url="/hello.html",
                body="Hello World")

        contents = urlopen('http://localhost:%d/hello.html' % rod.port).read()
        assert contents == 'Hello World'

Or with PyVows::

    class TestingGoogle(RodContext):
        def say(self, rod):
            rod.say(method="GET",
                url="/hello.html",
                body="Hello World")

        def topic(self):
            return urlopen('http://localhost:%d/hello.html' % rod.port).read()

        def should_not_be_empty(self, topic):
            expect(topic).not_to_be_empty()

        def should_be_equal_to_hello_world(self, topic):
            expect(topic).to_equal('Hello World')
