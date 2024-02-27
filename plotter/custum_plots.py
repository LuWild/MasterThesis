from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve

from plotter import plot_helper

from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svg

import csv

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def custom_plot_a_of_t(x_axis_range=[-15, 25], y_axis_max=25):
    x_axis_min = x_axis_range[0]
    x_axis_max = x_axis_range[1]

    p = figure(title="a(t)", x_axis_label="x", y_axis_label="y")

    t = []
    a = []

    file_name = "output/csv_files/a_of_t_deconvolution.csv"
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        first_row = False
        for row in reader:
            if first_row:
                t.append(float(row['t']))
                a.append(float(row['a']))
            else:
                first_row = True

    p.line(t, a, color="green", line_width=2)

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
    output_file(filename="output/html_files/custom_plot_a_of_t.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="output/svg_files/custom_plot_a_of_t.svg")


def custom_plot():
    p = figure(title="Custom Plot", x_axis_label="x", y_axis_label="y")

    # show the results
    output_file(filename="../output/html_files/custom_plot.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="../output/svg_files/custom_plot.svg")


if __name__ == '__main__':
    custom_plot_a_of_t()
