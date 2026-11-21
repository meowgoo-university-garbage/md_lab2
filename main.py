import math
import numpy as np
import matplotlib.pyplot as plt
import time




def calc_mu(xs):
    return sum(xs) / len(xs)

def calc_disp(xs, mu):
    disp = 0.0
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

def calc_correlation_pre(xs1, xs2):
    v = 0.0
    for (a, b) in zip(xs1, xs2):
        v += a * b
    v /= float(len(xs1))
    return v






def generate(hs, t):
    v = 0.0
    for (a, f, phi) in hs:
        v += a * math.sin(2 * math.pi * f * t + phi)
    return v




def process_generate(process, t):
    return [ generate(realization, t) for realization in process ]

def calc_process_mu(frame):
    mu = 0.0
    for v in frame:
        mu += v
    mu /= float(len(frame))
    return mu

def calc_process_disp(frame, mu):
    disp = 0.0
    for v in frame:
        disp += (v - mu) ** 2
    disp /= float(len(frame))
    return disp




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




    BENCH = True

    if BENCH:
        ts_my_mu = []
        ts_my_disp = []
        ts_my_corr = []

        ts_np_mu = []
        ts_np_disp = []
        ts_np_corr = []

        CORR_PRE = False

        for i in range(1, 6):
            if True:
                time_start = time.process_time()

                # for _ in range(100):
                _ = calc_mu(ys[0:i*500])

                time_end = time.process_time()
                t = time_end - time_start
                ts_my_mu.append(t)

            if True:
                time_start = time.process_time()

                # for _ in range(100):
                mu = calc_mu(ys[0:i*500])
                _ = calc_disp(ys[0:i*500], mu)

                time_end = time.process_time()
                t = time_end - time_start
                ts_my_disp.append(t)

            if not CORR_PRE:
                time_start = time.process_time()

                f = lambda t: generate(harmonics, t)
                g = f
                # for _ in range(100):
                _ = calc_correlation(f, g, xs[0:i*500], 5.0)

                time_end = time.process_time()
                t = time_end - time_start
                ts_my_corr.append(t)

            if CORR_PRE:
                time_start = time.process_time()

                # for _ in range(100):
                xsp = np.linspace(0.0 + 5.0, 20.0 + 5.0, i*500)
                _ = calc_correlation_pre(ys[0:i*500], [ generate(harmonics, x) for x in xsp ])

                time_end = time.process_time()
                t = time_end - time_start
                ts_my_corr.append(t)



            if True:
                time_start = time.process_time()

                # for _ in range(100):
                _ = np.mean(ys[0:i*500])

                time_end = time.process_time()
                t = time_end - time_start
                ts_np_mu.append(t)

            if True:
                time_start = time.process_time()

                # for _ in range(100):
                _ = np.var(ys[0:i*500])

                time_end = time.process_time()
                t = time_end - time_start
                ts_np_disp.append(t)

            if True:
                time_start = time.process_time()

                # for _ in range(100):
                xsp = np.linspace(0.0 + 5.0, 20.0 + 5.0, i*500)
                _ = np.correlate(ys[0:i*500], [ generate(harmonics, x) for x in xsp ])

                time_end = time.process_time()
                t = time_end - time_start
                ts_np_corr.append(t)

        plt.plot(ts_my_mu,      color = "#ee2222")
        plt.plot(ts_my_disp,    color = "#22ee22")
        plt.plot(ts_my_corr,    color = "#2222ee")

        plt.plot(ts_np_mu,      color = "#ee2222", linestyle = "--")
        plt.plot(ts_np_disp,    color = "#22ee22", linestyle = "--")
        plt.plot(ts_np_corr,    color = "#2222ee", linestyle = "--")
        plt.show()





    lags = np.linspace(0.0, 20.0, 100)
    f = lambda t: generate(harmonics, t)
    g = f
    cors = [ calc_correlation(f, g, xs, lag) for lag in lags ]


    plt.plot(lags, cors)
    plt.axhline(y = 0, color = "red")
    plt.show()




    process = [
        [
            (1.2, 0.2, +0.2),
            (0.9, 0.4, -0.4),
            (0.6, 0.7, +0.7),
            (0.3, 1.0, -1.1),
        ],
        [
            (0.8, 0.2, +0.8),
            (1.1, 0.5, +0.1),
            (0.4, 0.8, -0.6),
            (0.7, 1.1, +0.5),
        ],
        [
            (1.5, 0.3, -0.5),
            (0.5, 0.4, +0.9),
            (0.9, 0.9, +0.3),
            (0.4, 1.2, -0.8),
        ],
        [
            (0.6, 0.1, +1.1),
            (1.3, 0.6, -0.7),
            (0.7, 0.7, +0.4),
            (1.0, 1.3, +0.0),
        ],
    ]

    frames = [ process_generate(process, t) for t in xs ]
    mus = [ calc_process_mu(frame) for frame in frames ]
    disps = [ calc_process_disp(frame, mu) for (frame, mu) in zip(frames, mus) ]
    vas = [ a for [ a, b, c, d ] in frames ]
    vbs = [ b for [ a, b, c, d ] in frames ]
    vcs = [ c for [ a, b, c, d ] in frames ]
    vds = [ d for [ a, b, c, d ] in frames ]

    plt.plot(xs, vas,   label = "A", color = "#777777")
    plt.plot(xs, vbs,   label = "B", color = "#777777")
    plt.plot(xs, vcs,   label = "C", color = "#777777")
    plt.plot(xs, vds,   label = "D", color = "#777777")
    plt.plot(xs, mus,   label = "mean", color = "red")
    plt.plot(xs, disps, label = "dispersion", color = "blue")

    plt.legend()
    plt.show()





    print("Hello, World!")

main()
