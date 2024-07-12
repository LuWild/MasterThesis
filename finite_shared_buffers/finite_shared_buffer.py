from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from convolution_two_convex_pwl import create_convolution
from bokeh.plotting import figure, show
from bokeh.io import export_svg
from typing import List
import numpy as np

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def finite_shared_buffer_pwl(beta1: PiecewiseLinearServiceCurve, beta2: PiecewiseLinearServiceCurve, buffer_size: float,
                             x_axis_max=50, y_axis_max=50):

    B = buffer_size

    beta_FB = create_convolution(service_curve1=beta1, service_curve2=beta2)

    print("........... convolution of the PWL SCs from above: ")
    beta_FB.print_all_information()

    T = beta_FB.get_initial_latency()

    time = []
    data_list = []
    for t in list(np.arange(0, x_axis_max + 0.01, 0.01)):
        time.append(t)

    for n in range(0, 9):
        data = []
        beta_FB.set_shift((n * T))
        for t in list(np.arange(0, x_axis_max + 0.01, 0.01)):
            data.append(n * B + beta_FB.calculate_function_value(t))
        data_list.append(data)
        beta_FB.set_shift(-(n * T))

    plot(time=time, data_list=data_list, x_axis_max=x_axis_max, y_axis_max=y_axis_max)


def finite_shared_buffer_rl(beta1: RateLatencyServiceCurve, beta2: RateLatencyServiceCurve, buffer_size: float,
                            x_axis_max=50, y_axis_max=50):
    R1 = beta1.rate
    T1 = beta1.latency
    R2 = beta2.rate
    T2 = beta2.latency

    R = min(R1, R2)
    T = T1 + T2

    B = buffer_size

    beta_FB = RateLatencyServiceCurve(rate=R, latency=T)

    time = []
    data_list = []
    for t in list(np.arange(0, x_axis_max + 0.01, 0.01)):
        time.append(t)

    for n in range(0, 9):
        data = []
        for t in list(np.arange(0, x_axis_max + 0.01, 0.01)):
            beta_FB.latency = (n+1) * T
            data.append(n * B + beta_FB.calculate_function_value(t))
        data_list.append(data)

    plot(time=time, data_list=data_list, x_axis_max=x_axis_max, y_axis_max=y_axis_max)


def plot(time: List[float], data_list: List[List[float]], x_axis_max, y_axis_max):
    p = figure(title="Finite Shared Buffer", x_axis_label="t", y_axis_label="data")

    for data in data_list:
        p.line(time, data, color="red", line_width=2)

    # plot settings
    p.x_range.start = 0 - 1
    p.x_range.end = x_axis_max + 1
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = y_axis_max

    p.height = 600
    p.width = 1000

    # show the results
    show(p)

    p.output_backend = "svg"
    export_svg(p, filename="finite_shared_buffer_svg.svg")


def relation_checker(beta1: PiecewiseLinearServiceCurve, beta2: PiecewiseLinearServiceCurve, buffer_size: float):
    B = buffer_size

    beta_FB = create_convolution(service_curve1=beta1, service_curve2=beta2)

    R = beta_FB.rhos[-1].rate
    T = beta_FB.get_initial_latency()

    print("__________________________________")
    print("B = " + str(B) + "; R * T = " + str(R) + " * " + str(T) + " = " + str(R*T))

    if B < R * T:
        print("B < R * T")
    else:
        print("B >= R * T")


if __name__ == '__main__':

    b1 = RateLatencyServiceCurve(rate=2, latency=2)
    b2 = RateLatencyServiceCurve(rate=2, latency=1)
    B = 3

    # finite_shared_buffer_rl(beta1=b1, beta2=b2, buffer_size=B)

    rl1 = RateLatencyServiceCurve(rate=0.5, latency=1)
    rl2 = RateLatencyServiceCurve(rate=1.5, latency=4)
    pwl_sc1 = PiecewiseLinearServiceCurve(rhos=[rl1, rl2])
    pwl_sc1.print_all_information()

    rl1 = RateLatencyServiceCurve(rate=1.0, latency=1+1)
    rl2 = RateLatencyServiceCurve(rate=2.5, latency=7+1)
    pwl_sc2 = PiecewiseLinearServiceCurve(rhos=[rl1, rl2])
    pwl_sc2.print_all_information()
    B = 5

    finite_shared_buffer_pwl(beta1=pwl_sc1, beta2=pwl_sc2, buffer_size=B)
    relation_checker(beta1=pwl_sc1, beta2=pwl_sc2, buffer_size=B)


