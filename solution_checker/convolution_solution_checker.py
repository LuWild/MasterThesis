from plot_helper import *

from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svg
import csv
import numpy as np
import os

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def convolution_solution_check(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve,
                               t_end: float, step: float):
    t_values = list(np.arange(0, t_end+step, step))

    s_values_used = []
    function_values = []
    pwl_values = []
    sc_values = []
    gamma_used = []
    for t in t_values:
        s_values = list(np.arange(0, t+step, step))
        current_min = float('inf')
        min_s = float('inf')
        for s in s_values:
            value = arrival_curve.calculate_function_value(t - s) + service_curve.calculate_function_value(s)
            if value < current_min:
                min_s = s
                current_min = value
        s_values_used.append(min_s)
        function_values.append(current_min)
        pwl_values.append(arrival_curve.calculate_function_value(t - min_s))
        sc_values.append(service_curve.calculate_function_value(min_s))
        gamma_used.append(arrival_curve.get_used_gamma_number(t - min_s))

    csv_data = [t_values, s_values_used, function_values, pwl_values, sc_values, gamma_used]

    column_names = ["t", "s", "alpha(t-s)+beta(s)", "alpha(t-s)", "beta(s)", "gamma_used"]
    if "solution_checker" in os.getcwd():
        create_csv_file(file_name="../csv_files/convolution_solution_check.csv",
                        column_names=column_names, data=csv_data)
    else:
        create_csv_file(file_name="csv_files/convolution_solution_check.csv",
                        column_names=column_names, data=csv_data)

    plot_data = [t_values, function_values]
    create_plot(arrival_curve=arrival_curve, service_curve=service_curve,
                data=plot_data, x_axis_range=[0 - 1, int(t_end) + 1], y_axis_max=25)


def create_csv_file(file_name: str, column_names: List[str], data: List[list]):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(column_names)

        for i in range(0, len(data[0])):
            new_row = []
            for d in data:
                new_row.append(str(d[i]))
            writer.writerow(new_row)


def create_plot(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: RateLatencyServiceCurve, data: List[list],
                x_axis_range: List[int], y_axis_max: int):
    p = figure(title="Convolution Solution Checker", x_axis_label="x", y_axis_label="y")

    plot_arrival_curve_piecewise_linear(p=p, arrival_curve=arrival_curve, x_max=x_axis_range[1] - 1)
    plot_service_curve_rate_latency(p=p, service_curve=service_curve, x_max=x_axis_range[1] - 1)

    p.line(data[0], data[1], color="green", line_width=2)

    # plot settings
    p.x_range.start = x_axis_range[0]
    p.x_range.end = x_axis_range[1]
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = y_axis_max

    p.height = 600
    p.width = 1000

    # show the results
    if "solution_checker" in os.getcwd():
        output_file(filename="../plots/html_files/convolution_solution_check.html")
    else:
        output_file(filename="plots/html_files/convolution_solution_check.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    if "solution_checker" in os.getcwd():
        export_svg(p, filename="../plots/svg_files/convolution_solution_check.svg")
    else:
        export_svg(p, filename="plots/svg_files/convolution_solution_check.svg")


if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=1.0, burst=3)
    tb2 = TokenBucketArrivalCurve(rate=0.5, burst=6)
    tb3 = TokenBucketArrivalCurve(rate=0.25, burst=9)
    pwl = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])
    sc = RateLatencyServiceCurve(rate=1.0, latency=3)

    t_end = 35
    step = 0.01
    print("Starting Solution Check")
    print("...")
    convolution_solution_check(arrival_curve=pwl, service_curve=sc, t_end=t_end, step=step)
    print("Solution Check Completed")
