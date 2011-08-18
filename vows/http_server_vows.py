#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import urlopen
from pyvows import Vows, expect

from rod import RodContext

@Vows.batch
class AllTests(Vows.Context):
    class TestingHelloWorld(RodContext):
        def configure(self):
            self.rod_port = 2000

        def topic(self):
            self.say(method="GET",
                      url="/hello.html",
                      body="Hello World")

            return urlopen('http://localhost:2000/hello.html').read()

        def should_not_be_empty(self, topic):
            expect(topic).not_to_be_empty()

        def should_be_equal_to_hello_world(self, topic):
            expect(topic).to_equal('Hello World')


    class TestOtherRouteSamePort(RodContext):
        def configure(self):
            self.rod_port = 2001

        def topic(self):
            self.say(method="GET",
                     url="/other.html",
                     body="Other World")

            return urlopen('http://localhost:2001/other.html').read()

        def should_not_be_empty(self, topic):
            expect(topic).not_to_be_empty()

        def should_be_equal_to_hello_world(self, topic):
            expect(topic).to_equal('Other World')
