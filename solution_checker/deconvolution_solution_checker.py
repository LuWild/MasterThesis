from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from plotter.plot_helper import *

from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svg
import csv
import numpy as np
import os

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def deconvolution_solution_check(arrival_curve: ArrivalCurve, service_curve: ServiceCurve,
                                 t_start: float, t_end: float, t_step: float,
                                 s_start: float, s_end: float, s_step: float):
    """
    Brute forced way to calculate the deconvolution (n=2). Checks all combinations of t and s.
    Creates a .svg and a .html with the plot and a .csv with the values and calculation results.

    :param arrival_curve: PiecewiseLinearArrivalCurve
    :param service_curve: RateLatencyServiceCurve
    :param t_start: start value for t
    :param t_end: end value for t
    :param t_step: step size for t
    :param s_start: start value for s
    :param s_end: end value for t
    :param s_step: step size for s
    :return: -
    """
    t_values = list(np.arange(t_start, t_end, t_step))
    s_values = list(np.arange(s_start, s_end, s_step))

    s_values_used = []
    function_values = []
    pwl_values = []
    sc_values = []
    gamma_used = []
    for t in t_values:
        current_max = float('-inf')
        max_s = float('-inf')
        for s in s_values:
            value = arrival_curve.calculate_function_value(t + s) - service_curve.calculate_function_value(s)
            if value > current_max:
                max_s = s
                current_max = value
        s_values_used.append(max_s)
        function_values.append(current_max)
        pwl_values.append(arrival_curve.calculate_function_value(t + max_s))
        sc_values.append(service_curve.calculate_function_value(max_s))
        if isinstance(arrival_curve, PiecewiseLinearArrivalCurve):
            gamma_used.append(arrival_curve.get_used_gamma_number(t + max_s))
        else:
            gamma_used.append(1)

    csv_data = [t_values, s_values_used, function_values, pwl_values, sc_values, gamma_used]

    column_names = ["t", "s", "alpha(t+s)-beta(s)", "alpha(t+s)", "beta(s)", "gamma_used"]
    """
    if "solution_checker" in os.getcwd():
        create_csv_file(file_name="../output/csv_files/deconvolution_solution_check.csv",
                        column_names=column_names, data=csv_data)
    else:
        create_csv_file(file_name="output/csv_files/deconvolution_solution_check.csv",
                        column_names=column_names, data=csv_data)
    """

    plot_data = [t_values, function_values]
    create_plot(arrival_curve=arrival_curve, service_curve=service_curve,
                data=plot_data, x_axis_range=[int(t_start) - 1, int(t_end) + 1], y_axis_max=25)

    # print_important_information(arrival_curve=arrival_curve, service_curve=service_curve)


def create_csv_file(file_name: str, column_names: List[str], data: List[list]):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(column_names)

        for i in range(0, len(data[0])):
            new_row = []
            for d in data:
                new_row.append(str(d[i]))
            writer.writerow(new_row)


def create_plot(arrival_curve: ArrivalCurve, service_curve: ServiceCurve, data: List[list],
                x_axis_range: List[int], y_axis_max: int):
    p = figure(title="Deconvolution Solution Checker", x_axis_label="x", y_axis_label="y")

    add_arrival_curve(p=p, arrival_curve=arrival_curve, x_max=x_axis_range[1] - 1)
    add_service_curve(p=p, service_curve=service_curve, x_max=x_axis_range[1] - 1)

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
        output_file(filename="../output/html_files/deconvolution_solution_check.html")
    else:
        output_file(filename="output/html_files/deconvolution_solution_check.html")
    show(p)

    # export .svg
    p.output_backend = "svg"
    if "solution_checker" in os.getcwd():
        export_svg(p, filename="../output/svg_files/deconvolution_solution_check.svg")
    else:
        export_svg(p, filename="output/svg_files/deconvolution_solution_check.svg")


if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=1.5, burst=4)
    tb2 = TokenBucketArrivalCurve(rate=0.5, burst=7)
    pwl_ac = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2])

    rl1 = RateLatencyServiceCurve(rate=1.0, latency=3)
    rl2 = RateLatencyServiceCurve(rate=2.5, latency=7)
    pwl_sc = PiecewiseLinearServiceCurve(rhos=[rl1, rl2])

    print("pwl_ac intersections: " + str(pwl_ac.intersections))
    print("pwl_sc intersections: " + str(pwl_sc.intersections))

    t = [-15, 25, 0.1]
    s = [0, 100, 0.1]
    print("Starting Solution Check")
    print("...")
    deconvolution_solution_check(arrival_curve=pwl_ac, service_curve=pwl_sc,
                                 t_start=t[0], t_end=t[1], t_step=t[2],
                                 s_start=s[0], s_end=s[1], s_step=s[2])
    print("Solution Check Completed")
