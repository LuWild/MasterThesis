from arrival_curves import *
from services_curves import *
import plot_helper

from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svg
from typing import List

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def create_plot_deconvolution_n2(arrival_curve: PiecewiseLinearArrivalCurve,
                                 service_curve: RateLatencyServiceCurve,
                                 x_axis_range: List[int], y_axis_max: int):
    x_axis_min = x_axis_range[0]
    x_axis_max = x_axis_range[1]

    p = figure(title="Deconvolution (n=2)", x_axis_label="x", y_axis_label="y")

    plot_helper.plot_arrival_curve_piecewise_linear(p=p, arrival_curve=arrival_curve, x_max=x_axis_max)
    plot_helper.plot_service_curve_rate_latency(p=p, service_curve=service_curve, x_max=x_axis_max)
    plot_helper.plot_deconvolution_n2(p=p, arrival_curve=arrival_curve, service_curve=service_curve,
                                      x_axis_range=x_axis_range)

    # plot settings
    p.x_range.start = x_axis_min - 1
    p.x_range.end = x_axis_max + 1
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = y_axis_max

    p.height = 600
    p.width = 1000

    # show the results
    output_file(filename="plots/html_files/deconvolution_n2.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="plots/svg_files/deconvolution_n2.svg")


def create_plot_deconvolution(arrival_curve: PiecewiseLinearArrivalCurve,
                              service_curve: RateLatencyServiceCurve,
                              x_axis_range: List[int], y_axis_max: int):
    x_axis_min = x_axis_range[0]
    x_axis_max = x_axis_range[1]

    p = figure(title="Deconvolution", x_axis_label="x", y_axis_label="y")

    plot_helper.plot_arrival_curve_piecewise_linear(p=p, arrival_curve=arrival_curve, x_max=x_axis_max)
    plot_helper.plot_service_curve_rate_latency(p=p, service_curve=service_curve, x_max=x_axis_max)
    plot_helper.plot_deconvolution(p=p, arrival_curve=arrival_curve, service_curve=service_curve,
                                   x_axis_range=x_axis_range)

    # plot settings
    p.x_range.start = x_axis_min - 1
    p.x_range.end = x_axis_max + 1
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = y_axis_max

    p.height = 600
    p.width = 1000

    # show the results
    output_file(filename="plots/html_files/deconvolution.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="plots/svg_files/deconvolution.svg")


if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=1.0, burst=8)
    tb2 = TokenBucketArrivalCurve(rate=0.5, burst=10)
    pwl = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2])
    sc = RateLatencyServiceCurve(rate=1.5, latency=5)

    create_plot_deconvolution_n2(arrival_curve=pwl, service_curve=sc, x_axis_range=[-15, 20], y_axis_max=25)
