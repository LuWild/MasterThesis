import copy
import bokeh

from bokeh.plotting import figure, show
from bokeh.models import CrosshairTool
from bokeh.models import HoverTool
from bokeh.models import Band
from bokeh.models import Legend
from bokeh.io import export_svg

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def create_plot_aobn2_caseI():
    """
    Setting für plot:
    R = 1.5
    T = 5

    r_1 = 2.5
    b_1 = 4

    r_2 = 0.5
    b_2 = 10

    t_1 = 3
    """

    # prepare the data
    beta_x = list(range(0, 21))
    beta_y = rate_latency_function_calculator(R=1.5, T=5, values=beta_x)

    alpha_x = list(range(0, 21))
    gamma_array = [[2.5, 4], [0.5, 10]]
    alpha_y = piecewise_linear_function_calculator(gamma_array=gamma_array, values=alpha_x)

    gamma_2_x_dotted = [0, 1, 2, 3]
    gamma_2_y_dotted = [10, 10.5, 11, 11.5]

    # Case Ia:

    # 2*(t+5)+10
    case_Iaa_x = [-12, -11, -10, -9, -8, -7, -6, -5]
    case_Iaa_y = linear_function_calculator(r=1.5, a=5, b=10, values=case_Iaa_x)

    # 0.5*(t+5)+10
    case_Iab_x = [-5, -4, -3]
    case_Iab_y = linear_function_calculator(r=0.5, a=5, b=10, values=case_Iab_x)

    # Case Ib:

    # Intersection t = (0.5*5 - 2.5*3 + 10 - 4) / 2 = 0.5

    # 0.5(t+5)+10
    case_Iba_x = [-3, -2, -1, 0, 0.5]
    case_Iba_y = linear_function_calculator(r=0.5, a=5, b=10, values=case_Iba_x)

    # 2.5(t+3)+4
    case_Ibb_x = [0.5, 1, 3, 5, 7]
    case_Ibb_y = linear_function_calculator(r=2.5, a=3, b=4, values=case_Ibb_x)

    # create a new plot with a title and axis labels
    p = figure(title="aob(t)", x_axis_label="x", y_axis_label="y")

    # add multiple renderers
    p.line(beta_x, beta_y, color="red", line_width=2)
    p.line(alpha_x, alpha_y, color="blue", line_width=2)
    p.line(gamma_2_x_dotted, gamma_2_y_dotted, color="blue", line_width=2, line_dash="dotted")

    p.line(case_Iaa_x, case_Iaa_y, color="green", line_width=2)
    p.line(case_Iab_x, case_Iab_y, color="green", line_width=2)
    p.line(case_Iba_x, case_Iba_y, color="green", line_width=2)
    p.line(case_Ibb_x, case_Ibb_y, color="green", line_width=2)

    # plot settings
    p.x_range.start = -20
    p.x_range.end = 20
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = 25

    p.height = 600
    p.width = 1000

    # show the results
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="test.svg")


def create_plot_a_o_b_n2_caseII():
    R = 1.5
    T = 4

    r_1 = 2
    b_1 = 3

    r_2 = 0.5
    b_2 = 12

    t_1 = 6

    # prepare the data
    beta_x = list(range(0, 21))
    beta_y = rate_latency_function_calculator(R=R, T=T, values=beta_x)

    alpha_x = list(range(0, 21))
    gamma_array = [[r_1, b_1], [r_2, b_2]]
    alpha_y = piecewise_linear_function_calculator(gamma_array=gamma_array, values=alpha_x)

    gamma_2_x_dotted = [0, 1, 2, 3, 4, 5, 6]
    gamma_2_y_dotted = linear_function_calculator(r=r_2, a=0, b=b_2, values=gamma_2_x_dotted)

    # Case IIa:
    # bis [..., -6]
    # 0.5*(t+6) + 1.5*(4-6) + 12 = 0.5*(t+6) + 9
    case_IIa_x = list(range(-25, -5))
    case_IIa_y = linear_function_calculator(r=r_2, a=t_1, b=(R * (T - t_1) + b_2), values=case_IIa_x)

    # Case IIb:
    # ab [-5, ...]
    # Case IIba:
    intersection = ((r_2 - R) * t_1 + (R - r_1) * T + b_2 - b_1) / (r_1 - r_2)
    # Case_IIbaa:
    case_IIbaa_x = [-6, -5, -4, -3, -2, -1, 0, intersection]
    case_IIbaa_y = linear_function_calculator(r=r_2, a=t_1, b=(R * (T - t_1) + b_2), values=case_IIbaa_x)
    # Case_IIbab:
    case_IIbab_x = [intersection] + list(range(1, 21))
    case_IIbab_y = linear_function_calculator(r=r_1, a=T, b=b_1, values=case_IIbab_x)

    # create a new plot with a title and axis labels
    p = figure(title="aob(t)", x_axis_label="x", y_axis_label="y")

    # add multiple renderers
    p.line(beta_x, beta_y, color="red", line_width=2)
    p.line(alpha_x, alpha_y, color="blue", line_width=2)
    p.line(gamma_2_x_dotted, gamma_2_y_dotted, color="blue", line_width=2, line_dash="dotted")

    p.line(case_IIa_x, case_IIa_y, color="green", line_width=2)
    p.line(case_IIbaa_x, case_IIbaa_y, color="green", line_width=2)
    p.line(case_IIbab_x, case_IIbab_y, color="green", line_width=2)

    # plot settings
    p.x_range.start = -26
    p.x_range.end = 20
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = 25

    p.height = 600
    p.width = 1000

    # show the results
    show(p)

    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="test1.svg")


def linear_function_calculator(r, a, b, values):
    """
    Calculates function values for a given array of values. The function has the following form:
    r(t+a)+b
    :param r: rate
    :param a: x-axis shift
    :param b: y-axis shift
    :param values: values for which the function values are calculated for
    :return: array of function values
    """
    function_values = []
    for t in values:
        f_t = r * (t + a) + b
        function_values.append(f_t)

    return function_values


def piecewise_linear_function_calculator(gamma_array, values):
    """
    :param gamma_array: array of gamma arrays e.g.: [[gamma1_r, gamma1_b], [gamma2_r, gamma2_b], ...]
    :param values: values for which the function values are calculated for
    :return: array of function values
    """

    function_values = []
    function_value_candidate = []
    for t in values:
        for gamma in gamma_array:
            r = gamma[0]
            b = gamma[1]
            f_t = r * t + b
            function_value_candidate.append(f_t)
        function_values.append(min(function_value_candidate))
        function_value_candidate = []

    return function_values


def rate_latency_function_calculator(R, T, values):
    """
    :param R: rate
    :param T: latency
    :param values: values for which the function values are calculated for
    :return: array of function values
    """

    function_values = []
    for t in values:
        if t <= T:
            f_t = 0
        else:
            f_t = R * (t - T)
        function_values.append(f_t)

    return function_values


if __name__ == '__main__':
    create_plot_aobn2_caseI()
    create_plot_a_o_b_n2_caseII()
    print("test")


