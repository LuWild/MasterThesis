from plot_helper import *

from bokeh.plotting import figure, show
from bokeh.io import export_svg
import csv
import numpy as np

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def deconvolution_n2_solution_check(pwl: PiecewiseLinearArrivalCurve, sc: RateLatencyServiceCurve,
                                    t_start: float, t_end: float, t_step: float,
                                    s_start: float, s_end: float, s_step: float):
    """

    :param pwl:
    :param sc:
    :param t_start:
    :param t_end:
    :param t_step:
    :param s_start:
    :param s_end:
    :param s_step:
    :return:
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
            value = pwl.calculate_function_value(t + s) - sc.calculate_function_value(s)
            if value > current_max:
                max_s = s
                current_max = value
        s_values_used.append(max_s)
        function_values.append(current_max)
        pwl_values.append(pwl.calculate_function_value(t + max_s))
        sc_values.append(sc.calculate_function_value(max_s))
        gamma_used.append(pwl.get_used_gamma_number(t + max_s))

    csv_data = [t_values, s_values_used, function_values, pwl_values, sc_values, gamma_used]

    column_names = ["t", "s", "alpha(t+s)-beta(s)", "alpha(t+s)", "beta(s)", "gamma_used"]
    create_csv_file(file_name="deconvolution_n2_solution_checker_csv.csv", column_names=column_names, data=csv_data)

    plot_data = [t_values, function_values]
    create_plot(pwl=pwl, sc=sc, data=plot_data, x_axis_range=[int(t_start) - 1, int(t_end) + 1], y_axis_max=25)

    print_important_information(pwl=pwl, sc=sc)


def create_csv_file(file_name: str, column_names: List[str], data: List[list]):
    """

    :param file_name:
    :param column_names:
    :param data:
    :return:
    """
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(column_names)

        for i in range(0, len(data[0])):
            new_row = []
            for d in data:
                new_row.append(str(d[i]))
            writer.writerow(new_row)


def create_plot(pwl: PiecewiseLinearArrivalCurve, sc: RateLatencyServiceCurve, data: List[list],
                x_axis_range: List[int], y_axis_max: int):
    """

    :param pwl:
    :param sc:
    :param data:
    :param x_axis_range:
    :param y_axis_max:
    :return:
    """
    p = figure(title="Deconvolution Solution Checker (n=2)", x_axis_label="x", y_axis_label="y")

    plot_arrival_curve_piecewise_linear(p=p, arrival_curve=pwl, x_max=x_axis_range[1] - 1)
    plot_service_curve_rate_latency(p=p, service_curve=sc, x_max=x_axis_range[1] - 1)

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
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="deconvolution_n2_solution_checker_svg.svg")


def print_important_information(pwl: PiecewiseLinearArrivalCurve, sc: RateLatencyServiceCurve):
    print("Important Information about the setting:")
    print("t1 = %f" % pwl.intersections[0])
    print("T = %f" % sc.latency)
    dif = pwl.intersections[0]-sc.latency
    print("t1-T = %f" % dif)


if __name__ == '__main__':
    tb1 = TokenBucketArrivalCurve(rate=1.0, burst=8)
    tb2 = TokenBucketArrivalCurve(rate=0.5, burst=10)
    tb3 = TokenBucketArrivalCurve(rate=0.25, burst=14)
    pwl = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2])
    sc = RateLatencyServiceCurve(rate=1.5, latency=5)

    t = [-15, 20, 0.1]
    s = [0, 100, 0.1]
    print("Starting Solution Check")
    print("...")
    deconvolution_n2_solution_check(pwl=pwl, sc=sc,
                                    t_start=t[0], t_end=t[1], t_step=t[2],
                                    s_start=s[0], s_end=s[1], s_step=s[2])
    print("Solution Check Completed")
