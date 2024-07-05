from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve

from dnc_service.service_curve import ServiceCurve

from dnc_operations.backlog_bound import backlog_bound
from dnc_operations.delay_bound import delay_bound
from dnc_operations.max_length_backlogged_period import max_length_backlogged_period
from solution_checker.deconvolution_solution_checker import deconvolution_solution_check

from plotter import plot_helper

from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svg

import csv

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def custom_plot_a_of_t(x_axis_range=[-15, 25], y_axis_max=25):
    x_axis_min = x_axis_range[0]
    x_axis_max = x_axis_range[1]

    p = figure(title="a(t)", x_axis_label="t", y_axis_label="y")

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


def plot_example(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: ServiceCurve, chapter: int):
    p = figure(title="Example Chapter "+str(chapter), x_axis_label="t", y_axis_label="y")

    plot_helper.add_arrival_curve(p=p, arrival_curve=arrival_curve, x_max=25)
    plot_helper.add_service_curve(p=p, service_curve=service_curve, x_max=25)

    delay_bound_result = delay_bound(arrival_curve=arrival_curve, service_curve=service_curve)
    plot_helper.add_delay_bound(p=p, arrival_curve=arrival_curve, service_curve=service_curve,
                                ta=delay_bound_result[1][1], d=delay_bound_result[0], case=delay_bound_result[1][0])

    q_and_a = backlog_bound(arrival_curve=arrival_curve, service_curve=service_curve, deconvolution_case=True)
    plot_helper.add_backlog_bound(p=p, arrival_curve=arrival_curve, service_curve=service_curve,
                                  backlog_bound_t=q_and_a[1])

    bp = max_length_backlogged_period(arrival_curve=arrival_curve, service_curve=service_curve)
    p.segment(x0=bp, y0=0, x1=bp, y1=arrival_curve.calculate_function_value(bp), line_width=2,
              line_dash='dotted', line_color='purple')

    deconvolution_data = deconvolution_solution_check(arrival_curve=arrival_curve, service_curve=service_curve,
                                                      t_start=0, t_end=25, t_step=0.01,
                                                      s_start=0, s_end=25, s_step=0.1, get_data=True)

    p.line(deconvolution_data[0], deconvolution_data[1], color="green", line_width=2)

    # plot settings
    p.x_range.start = 0 - 1
    p.x_range.end = 25 + 1
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = 25

    p.height = 600
    p.width = 1000

    # show the results
    show(p)


def custom_plot():
    from bokeh.layouts import column, row
    from bokeh.models import ColumnDataSource, CustomJS, Slider, SetValue

    p = figure(title="Custom Plot", x_axis_label="x", y_axis_label="y")

    t = [1, 2, 3, 4, 5]
    a1 = [1, 2, 3, 4, 5]
    a2 = [2, 4, 6, 8, 14]
    a_list = [a1, a2]

    x = [x * 0.005 for x in range(0, 200)]
    y = x

    source = ColumnDataSource(data=dict(x=t, y=a1))

    p.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

    js_code = """
        const f = cb_obj.value
        const a_list = %s
        const x = source.data.x
        const y = a_list[f]
        source.data = { x, y }
    """ % a_list

    callback = CustomJS(args=dict(source=source), code=js_code)

    slider = Slider(start=0, end=1, value=0, step=1, title="power")
    slider.js_on_change('value', callback)

    # show the results
    output_file(filename="../output/html_files/custom_plot.html")
    show(column(p, slider))

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="../output/svg_files/custom_plot.svg")


if __name__ == '__main__':
    custom_plot_a_of_t()
