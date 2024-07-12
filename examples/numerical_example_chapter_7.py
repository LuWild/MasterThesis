import math
from typing import List
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.io import export_svg

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


def create_plot(buffer_size: List[float], data_mac: List[float], data_ca: List[float]):
    p = figure(title="Case Study", x_axis_label="buffer size", y_axis_label="delay bound")

    p.line(buffer_size, data_mac, color="red", line_width=2)
    p.line(buffer_size, data_ca, color="blue", line_width=2)

    # plot settings
    p.x_range.start = buffer_size[0]
    p.x_range.end = buffer_size[-1]
    # """
    p.yaxis.fixed_location = 0
    p.y_range.start = 0
    p.y_range.end = 10

    p.height = 600
    p.width = 1000

    # show the results
    output_file(filename="numerical_example_chapter_7.html")
    show(p)

    """
    # export .svg
    p.output_backend = "svg"
    export_svg(p, filename="numerical_example_chapter_7_svg.svg")
    """


def logic_checker():
    if B_div_T > r_H:
        buffer_size_check = True
        for b in buffer_size:
            if b <= v_H:
                print("Buffer Size: " + str(b))
                print("v_h = " + str(v_H))
                buffer_size_check = False
        if buffer_size_check:
            print("Logic Check Successful.")
        else:
            print("Logic Check NOT Successful. (Buffer Size)")
    else:
        print("B_div_T = " + str(B_div_T))
        print("r_H = " + str(r_H))
        print("Logic Check NOT Successful. (B_div_T)")


if __name__ == '__main__':
    r_L = 2.5
    b_L = 2

    r_H = 2.5
    b_H = 1

    R_1 = 15
    T_1 = 0.5

    R_2 = 15
    T_2 = 0.5

    R = min(R_1, R_2)
    T = T_1 + T_2

    v_L = b_L + r_L * T
    v_H = b_H + r_H * T

    buffer_min = 4
    buffer_max = 10
    buffer_step = 0.5

    rL_list = [1.0, 2.0]
    for rL in rL_list:
        buffer_size = []
        data_mac = []
        data_ca = []
        for b in list(np.arange(buffer_min, buffer_max + buffer_step, buffer_step)):
            # print(".........")
            # print("Buffer size: " + str(b))
            buffer_size.append(b)

            if T > 0:
                B_div_T = b / T
            else:
                B_div_T = R

            T_alpha_L = v_L / B_div_T
            r_underline_L = rL

            h = (v_H + v_L) / (B_div_T - r_H)
            z = T_alpha_L + (v_H / r_underline_L)
            """
            if h > z:
                print("h Case")
            else:
                print("z Case")
            """
            d_mac = max(h, z)

            if b != v_H:
                i_star = math.ceil(v_L / (b - v_H))

                if v_H <= (b - v_H):
                    # print("First Case Eq 50")
                    d_ca = (v_H + v_L) / (B_div_T - r_H)
                else:
                    # print("Second Case Eq 50")
                    T_res = v_H / (B_div_T - r_H)
                    d_ca = (v_L - (i_star - 1) * (b - v_H)) / (B_div_T - r_H) + i_star * T_res
            else:
                d_ca = -1

            data_mac.append(d_mac)
            data_ca.append(d_ca)

        create_plot(buffer_size=buffer_size, data_mac=data_mac, data_ca=data_ca)
        # logic_checker()
