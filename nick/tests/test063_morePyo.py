from pyo import *

s = Server().boot()
s.amp = 0.1

# Creates a source (white noise)
n = Noise().out(0)
s = Sine(2000).out(1)

s.gui(locals())
