from dnc_service.service_curve import ServiceCurve
from dnc_arrivals.arrival_curve import ArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve
from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve

from dnc_operations.backlog_bound import backlog_bound

from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svg
from typing import List

from plotter import plot_helper

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, SetValue, Label

import numpy as np

import copy


def plot_interactive_backlog_bound(arrival_curve: PiecewiseLinearArrivalCurve,
                                   service_curve: PiecewiseLinearServiceCurve,
                                   x_axis_max: int, y_axis_max: int):
    p = figure(title="Interactive Backlog Bound", x_axis_label="t", y_axis_label="y")

    plot_helper.add_service_curve(p, service_curve=service_curve, x_max=x_axis_max)

    shift = arrival_curve.get_shift()

    t = list(np.arange(0, x_axis_max + 0.01, 0.01))

    ac_data_range = x_axis_max
    ac_data_start = -ac_data_range
    ac_data_end = ac_data_range
    ac_data_step = 0.25
    index_f_0 = ac_data_range / ac_data_step
    ac_and_bb_data = create_ac_and_bb_data(arrival_curve=arrival_curve, service_curve=service_curve,
                                           x_axis_max=x_axis_max,
                                           ac_data_start=ac_data_start, ac_data_end=ac_data_end,
                                           ac_data_step=ac_data_step)

    ac_data = ac_and_bb_data[0]
    bb_data = ac_and_bb_data[1]

    source_ac = ColumnDataSource(data=dict(x=t, y=ac_data[int(index_f_0)]))

    p.line('x', 'y', source=source_ac, color="blue", line_width=2)

    initial_bb = bb_data[int(index_f_0)]
    source_bb = ColumnDataSource(dict(
            x0=[initial_bb[0]],
            y0=[initial_bb[1]],
            x1=[initial_bb[2]],
            y1=[initial_bb[3]],
        )
    )

    p.segment(source=source_bb, x0='x0', y0='y0', x1='x1', y1='y1', line_width=2,
              line_dash='dotted', line_color='purple')

    js_code = """
        const t = cb_obj.value
        
        const ac_data = %s
        const ac_step = %s
        const index_f_0 = %s
        const x = source.data.x
        
        const i = index_f_0 + (t / ac_step)
        
        const y = ac_data[i]
        
        source.data = { x, y }
        
        const bb_data = %s 
        const bb_data_f_0 = bb_data[i]
        
        const x0 = [bb_data_f_0[0]]
        const y0 = [bb_data_f_0[1]]
        const x1 = [bb_data_f_0[2]]
        const y1 = [bb_data_f_0[3]]
        
        source1.data = { x0, y0, x1, y1 }
    """ % (ac_data, ac_data_step, index_f_0, bb_data)

    callback = CustomJS(args=dict(source=source_ac, source1=source_bb), code=js_code)

    slider = Slider(start=ac_data_start, end=ac_data_end, value=0, step=ac_data_step, title="t")
    slider.js_on_change('value', callback)

    # plot settings
    p.x_range.start = - 1
    p.x_range.end = x_axis_max + 1
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = y_axis_max

    p.height = 600
    p.width = 1000

    # show the results
    show(column(p, slider))
    p.output_backend = "svg"
    export_svg(p, filename="output/svg_files/interactive_plot.svg")


def create_ac_and_bb_data(arrival_curve: PiecewiseLinearArrivalCurve, service_curve: PiecewiseLinearServiceCurve,
                          x_axis_max: int, ac_data_start: float, ac_data_end: float, ac_data_step: float):
    time = list(np.arange(0.01, x_axis_max + 0.01, 0.01))

    arrival_curves = []
    ac_data = []

    for t_shift in list(np.arange(ac_data_start, ac_data_end + ac_data_step, ac_data_step)):
        shifted_arrival_curve = copy.deepcopy(arrival_curve)
        shifted_arrival_curve.set_shift(shift=t_shift)
        arrival_curves.append(shifted_arrival_curve)
        # arrival_curves.append(piecewise_linear_arrival_curve_shift(arrival_curve=arrival_curve, t_shift=t_shift))

    for ac in arrival_curves:
        if ac.get_shift() == 0:
            ac_values = [ac.get_initial_burst()]
        else:
            ac_values = []
        for t in time:
            ac_values.append(ac.calculate_function_value(t))
        ac_data.append(ac_values)

    bb_data = []
    for ac in arrival_curves:
        q_and_a = backlog_bound(arrival_curve=ac, service_curve=service_curve, deconvolution_case=True)
        a = q_and_a[1]
        y0 = service_curve.calculate_function_value(a)
        y1 = ac.calculate_function_value(a)
        bb_data.append([a, y0, a, y1])

    return [ac_data, bb_data]
