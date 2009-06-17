from pylab import *
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import random

x = arange(20)
y = [random.choice([0,1]) for i in x]

fig = figure()
ax = fig.add_subplot(111)
ax.plot(x, y, linestyle="steps", label="line 1", lw=2)

plt.fill(x, y)

plt.axis([0, len(y)-1, -1, 2])
plt.grid(True)
xticks( x )
plt.show()
