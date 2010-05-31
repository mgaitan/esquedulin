class A(object):
    def __init__(self):
        print "A"
        self.a = 1
        self.metodo()

    def metodo(self):
        print "metodo de A"

class B(object):
    def __init__(self):
        print "B"
        self.b = 2

class C(A):
    def __init__(self):
        print "C"
        A.__init__(self)
        self.c = 3

    def metodo(self):
        print "metodo de C2"
