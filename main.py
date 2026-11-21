import math
import numpy as np
import matplotlib.pyplot as plt




def calc_mu(xs):
    return sum(xs) / len(xs)

def calc_disp(xs):
    mu = calc_mu(xs)

    disp = 0
    for x in xs:
        disp += (x - mu) ** 2
    disp /= (len(xs) - 1)
    return disp

def calc_sigma(xs):
    return math.sqrt(calc_disp(xs))

def calc_correlation(f, g, xs, lag):
    v = 0.0
    for x in xs:
        v += f(x) * g(x + lag)
    v /= float(len(xs))
    return v



def generate(hs, t):
    v = 0.0
    for (a, f, phi) in hs:
        v += a * math.sin(2 * math.pi * f * t + phi)
    return v



def main():
    harmonics = [
        (1.2, 0.2, 0.2),
        (0.9, 0.4, -0.4),
        (0.6, 0.7, 0.7),
        (0.3, 1.0, -1.1),
    ]

    xs = np.linspace(0.0, 20.0, 2500)
    ys = [ generate(harmonics, x) for x in xs ]

    signal_data = np.column_stack((xs, ys))
    np.savetxt("./signal.csv", signal_data, delimiter=",", header="t,signal", comments="")

    plt.plot(xs, ys)
    plt.axhline(y = calc_mu(ys), color = "red")
    plt.show()


    lags = np.linspace(0.0, 20.0, 1000)
    f = lambda t: generate(harmonics, t)
    g = f
    cors = [ calc_correlation(f, g, xs, lag) for lag in lags ]


    plt.plot(lags, cors)
    plt.axhline(y = 0, color = "red")
    plt.show()


    print("Hello, World!")

main()
