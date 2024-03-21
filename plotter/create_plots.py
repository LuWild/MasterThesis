from dnc_service.service_curve import ServiceCurve
from dnc_arrivals.arrival_curve import ArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve

from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svg
from typing import List

from plotter import plot_helper

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def plot_arrival_and_service_curve(arrival_curve: ArrivalCurve,
                                   service_curve: ServiceCurve,
                                   x_axis_max: int, y_axis_max: int):
    x_axis_min = -1

    p = figure(title="Arrival and Service Curve (PWL)", x_axis_label="t", y_axis_label="y")

    plot_helper.add_arrival_curve(p=p, arrival_curve=arrival_curve, x_max=x_axis_max)
    plot_helper.add_service_curve(p=p, service_curve=service_curve, x_max=x_axis_max)

    # plot settings
    p.x_range.start = x_axis_min - 1
    p.x_range.end = x_axis_max + 1
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = y_axis_max

    p.height = 600
    p.width = 1000

    show(p)


def plot_leftover_service_curve(leftover_service_curve: PiecewiseLinearServiceCurve, used_theta: float,
                                x_axis_max: int, y_axis_max: int, arrival_curve=None, cross_flow=None):
    x_axis_min = -1

    p = figure(title="Leftover Service Curve", x_axis_label="t", y_axis_label="y")

    if arrival_curve is not None:
        plot_helper.add_arrival_curve(p=p, arrival_curve=arrival_curve, x_max=x_axis_max)
    if cross_flow is not None:
        plot_helper.add_arrival_curve(p=p, arrival_curve=cross_flow, x_max=x_axis_max)
    plot_helper.add_leftover_service_curve(p=p, leftover_service_curve=leftover_service_curve, used_theta=used_theta,
                                           x_max=x_axis_max)

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
    output_file(filename="output/html_files/leftover_service_curve.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="output/svg_files/leftover_service_curve.svg")


def plot_backlog_bound(arrival_curve: ArrivalCurve,
                       service_curve: ServiceCurve,
                       backlog_bound_t: float,
                       x_axis_max: int, y_axis_max: int):
    x_axis_min = -1

    p = figure(title="Backlog Bound", x_axis_label="t", y_axis_label="y")

    plot_helper.add_arrival_curve(p=p, arrival_curve=arrival_curve, x_max=x_axis_max)
    plot_helper.add_service_curve(p=p, service_curve=service_curve, x_max=x_axis_max)
    plot_helper.add_backlog_bound(p=p, arrival_curve=arrival_curve, service_curve=service_curve,
                                  backlog_bound_t=backlog_bound_t)

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
    output_file(filename="output/html_files/backlog_bound.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="output/svg_files/backlog_bound.svg")


def plot_delay_bound(arrival_curve: ArrivalCurve,
                     service_curve: ServiceCurve,
                     ta: float, d: float,
                     x_axis_max: int, y_axis_max: int,
                     case=1):
    x_axis_min = -1

    p = figure(title="Delay Bound", x_axis_label="t", y_axis_label="y")

    plot_helper.add_arrival_curve(p=p, arrival_curve=arrival_curve, x_max=x_axis_max)
    plot_helper.add_service_curve(p=p, service_curve=service_curve, x_max=x_axis_max)
    plot_helper.add_delay_bound(p=p, arrival_curve=arrival_curve, service_curve=service_curve, ta=ta, d=d, case=case)

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
    output_file(filename="output/html_files/delay_bound.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="output/svg_files/delay_bound.svg")


def plot_deconvolution_n2(arrival_curve: PiecewiseLinearArrivalCurve,
                          service_curve: RateLatencyServiceCurve,
                          x_axis_range: List[int], y_axis_max: int):
    x_axis_min = x_axis_range[0]
    x_axis_max = x_axis_range[1]

    p = figure(title="Deconvolution (n=2)", x_axis_label="t", y_axis_label="y")

    plot_helper.add_arrival_curve(p=p, arrival_curve=arrival_curve, x_max=x_axis_max)
    plot_helper.add_service_curve(p=p, service_curve=service_curve, x_max=x_axis_max)
    plot_helper.add_deconvolution_n2(p=p, arrival_curve=arrival_curve, service_curve=service_curve,
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
    output_file(filename="output/html_files/deconvolution_n2.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="output/svg_files/deconvolution_n2.svg")


def plot_deconvolution(arrival_curve: ArrivalCurve, service_curve: ServiceCurve,
                       x_axis_range: List[int], y_axis_max: int):
    x_axis_min = x_axis_range[0]
    x_axis_max = x_axis_range[1]

    p = figure(title="Deconvolution", x_axis_label="t", y_axis_label="y")

    plot_helper.add_arrival_curve(p=p, arrival_curve=arrival_curve, x_max=x_axis_max)
    plot_helper.add_service_curve(p=p, service_curve=service_curve, x_max=x_axis_max)
    plot_helper.add_deconvolution(p=p, arrival_curve=arrival_curve, service_curve=service_curve,
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
    output_file(filename="output/html_files/deconvolution.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="output/svg_files/deconvolution.svg")


def plot_convolution(arrival_curve: ArrivalCurve,
                     service_curve: ServiceCurve,
                     x_axis_range: List[int], y_axis_max: int):
    x_axis_min = x_axis_range[0]
    x_axis_max = x_axis_range[1]

    p = figure(title="Convolution", x_axis_label="t", y_axis_label="y")

    plot_helper.add_arrival_curve(p=p, arrival_curve=arrival_curve, x_max=x_axis_max)
    plot_helper.add_service_curve(p=p, service_curve=service_curve, x_max=x_axis_max)
    plot_helper.add_convolution(p=p, arrival_curve=arrival_curve, service_curve=service_curve,
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
    output_file(filename="output/html_files/convolution.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="output/svg_files/convolution.svg")
