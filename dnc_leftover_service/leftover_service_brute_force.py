from dnc_arrivals.token_bucket_arrival_curve import TokenBucketArrivalCurve
from dnc_arrivals.piecewise_linear_arrival_curve import PiecewiseLinearArrivalCurve
from dnc_service.rate_latency_service_curve import RateLatencyServiceCurve
from dnc_service.piecewise_linear_service_curve import PiecewiseLinearServiceCurve

from dnc_operations.arrival_curve_shift import token_bucket_arrival_curve_shift
from dnc_operations.arrival_curve_shift import piecewise_linear_arrival_curve_shift

from dnc_operations.max_length_backlogged_period import max_length_backlogged_period

from dnc_leftover_service.letfover_service import FIFO_leftover_service_pwl
from dnc_operations.backlog_bound import backlog_bound
from dnc_operations.delay_bound import delay_bound

from typing import List
import csv
import numpy as np
import os


def FIFO_leftover_service_pwl_brute_force_theta(cross_flow: PiecewiseLinearArrivalCurve,
                                                service_curve: PiecewiseLinearServiceCurve,
                                                foi: PiecewiseLinearArrivalCurve,
                                                theta_interval=[0, 10], theta_step=0.25):
    thetas_latency_backlog_delay = create_csv_FIFO_leftover_service_pwl(cross_flow=cross_flow,
                                                                        service_curve=service_curve,
                                                                        foi=foi,
                                                                        theta_interval=theta_interval,
                                                                        theta_step=theta_step)
    # latency
    min_latency = min(thetas_latency_backlog_delay[1])
    theta_min_latency = thetas_latency_backlog_delay[0].__getitem__(thetas_latency_backlog_delay[1].index(min_latency))
    min_latency_with_theta = [min_latency, theta_min_latency]

    # backlog
    min_backlog = min(thetas_latency_backlog_delay[2])
    theta_min_backlog = thetas_latency_backlog_delay[0].__getitem__(thetas_latency_backlog_delay[2].index(min_backlog))
    min_backlog_with_theta = [min_backlog, theta_min_backlog]

    # delay
    min_delay = float('inf')
    for delay in thetas_latency_backlog_delay[3]:
        if 0 < delay < min_delay:
            min_delay = delay
    theta_min_delay = thetas_latency_backlog_delay[0].__getitem__(thetas_latency_backlog_delay[3].index(min_delay))
    min_delay_with_theta = [min_delay, theta_min_delay]

    print_information(min_latency_with_theta, min_backlog_with_theta, min_delay_with_theta,
                      theta_interval=theta_interval, theta_step=theta_step)


def create_csv_FIFO_leftover_service_pwl(cross_flow: PiecewiseLinearArrivalCurve,
                                         service_curve: PiecewiseLinearServiceCurve,
                                         foi: PiecewiseLinearArrivalCurve,
                                         theta_interval, theta_step):
    thetas = list(np.arange(theta_interval[0], theta_interval[1] + theta_step, theta_step))
    latency = []
    backlog = []
    delay = []

    for theta in thetas:
        leftover_service_curve = FIFO_leftover_service_pwl(cross_flow=cross_flow, service_curve=service_curve,
                                                           theta=theta, print_information=False)
        latency.append(leftover_service_curve.get_initial_latency())
        backlog.append(backlog_bound(arrival_curve=foi, service_curve=leftover_service_curve))
        delay.append(delay_bound(arrival_curve=foi, service_curve=leftover_service_curve))

    csv_data = [thetas, latency, backlog, delay]

    column_names = ["theta", "latency", "backlog", "delay"]
    if "dnc_leftover_service" in os.getcwd():
        with open("../output/csv_files/leftover_service_theta.csv", 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(column_names)

            for i in range(0, len(csv_data[0])):
                new_row = []
                for d in csv_data:
                    new_row.append(str(d[i]))
                writer.writerow(new_row)
    else:
        with open("output/csv_files/leftover_service_theta.csv", 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(column_names)

            for i in range(0, len(csv_data[0])):
                new_row = []
                for d in csv_data:
                    new_row.append(str(d[i]))
                writer.writerow(new_row)

    return csv_data


def print_information(min_latency_with_theta, min_backlog_with_theta, min_delay_with_theta,
                      theta_interval, theta_step):
    print("Leftover Service Brute Force:")
    print("Settings: Theta Interval: " + str(theta_interval) + ", Theta Step: " + str(theta_step))
    print("Min Latency: " + str(min_latency_with_theta[0]) + " (theta=" + str(min_latency_with_theta[1]) + ")")
    print("Min Backlog: " + str(min_backlog_with_theta[0]) + " (theta=" + str(min_backlog_with_theta[1]) + ")")
    print("Min Delay: " + str(min_delay_with_theta[0]) + " (theta=" + str(min_delay_with_theta[1]) + ")")
    print("------------------------")
