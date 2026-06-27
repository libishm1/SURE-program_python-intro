#code to plot a parabola using matplotlib and show the trapezoids used for integration

import matplotlib.pyplot as plt
import numpy as np

# Smooth curve for reference
x = np.linspace(-10, 10, 400)
y = x**2

# Coarse points define the trapezoids (fewer = more visible)
xt = np.linspace(-10, 10, 12)
yt = xt**2

# Numerical integration over the coarse points
area = np.trapezoid(yt, xt)

plt.plot(x, y, color='black', linewidth=2, label='y = x²')

# Draw each trapezoid as a filled colored polygon
cmap = plt.cm.viridis
for i in range(len(xt) - 1):
    poly_x = [xt[i], xt[i + 1], xt[i + 1], xt[i]]
    poly_y = [0, 0, yt[i + 1], yt[i]]
    plt.fill(poly_x, poly_y,
             facecolor=cmap(i / (len(xt) - 1)),
             edgecolor='white', alpha=0.7)

plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Trapezoidal integration (area ≈ {area:.1f})')
plt.legend()
plt.grid(True)
plt.show()


print("Area under the curve:", area)