from pylab import *
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import random

x = arange(20)
x1 = arange(21)
y = []
for i in range(3):
    y.append([random.choice([0,1]) for i in x])

y[0].insert(0,None)

fig = figure()
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

ax1.plot(x1, y[0], linestyle="steps", label="line 1", lw=2)
ax2.plot(x, y[1], linestyle="steps", label="line 2", lw=2)
ax3.plot(x, y[2], linestyle="steps", label="line 3", lw=2)

plt.axis([0, len(y)-1, -1, 2])
plt.grid(True)
plt.xticks( x )
plt.show()
