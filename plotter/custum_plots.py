from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve

from plotter import plot_helper

from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svg

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def custom_plot():
    p = figure(title="Custom Plot", x_axis_label="x", y_axis_label="y")

    # show the results
    output_file(filename="output/html_files/custom_plot.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="output/svg_files/custom_plot.svg")


if __name__ == '__main__':
    custom_plot()
