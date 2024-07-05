# Deterministic Network Calculus with Piecewise Linear Curves

Performance bound calculations with visualization is implemented in this toolbox. The focus is on piecewise linear (PWL) arrival and service curves in a single flow single server setting.

## Prerequisites

- Python 3.8 or higher
- Python packages in `requiremets.txt`

## Introduction

The easiest start is to use `main.py`. Create a arrival curve and service curve:

```python
tb1 = TokenBucketArrivalCurve(rate=2.0, burst=3)
tb2 = TokenBucketArrivalCurve(rate=1.0, burst=5)
tb3 = TokenBucketArrivalCurve(rate=0.50, burst=10)
arrival_curve = PiecewiseLinearArrivalCurve(gammas=[tb1, tb2, tb3])

rl1 = RateLatencyServiceCurve(rate=0.5, latency=1)
rl2 = RateLatencyServiceCurve(rate=1.25, latency=4)
rl3 = RateLatencyServiceCurve(rate=2.0, latency=7)
service_curve = PiecewiseLinearServiceCurve(rhos=[rl1, rl2, rl3])
```

After creating the arrival and service curve, we can use the different "show" methods:

```python
show_arrival_and_service_curve(ac=arrival_curve, sc=service_curve)
show_interactive_plot(ac=arrival_curve, sc=service_curve)
show_leftover_service_curve(ac=arrival_curve, sc=service_curve, theta=10)
show_backlog_bound(ac=arrival_curve, sc=service_curve)
show_delay_bound(ac=arrival_curve, sc=service_curve)
show_max_bp(ac=arrival_curve, sc=service_curve)
show_convolution(ac=arrival_curve, sc=service_curve)
show_deconvolution(ac=arrival_curve, sc=service_curve)
```

Each plot will be opened in your browser.

## Using the Examples

To use one of the two examples referenced in the master thesis, open the file `numerical_example_chapter_3.py` or `numerical_example_chapter_4.py` directly.

Then run the code of the file and the resulting plot will be opened in your browser.

## Status of Implementation

Arrival curves:

- Token bucket
- Piecewise linear arrival curve

Service curves:

- Rate-Latency
- Piecewise linear service curve

Network Calculus operations:

- Convolution (PWL)
- Deconvolution (PWL)
- Leftover service (FIFO, PWL)

Performance Metrics:

- Backlog bound (PWL)
- Delay bound (PWL)
- Max length of backlogged period (PWL)

Topologies / settings:

- Single server

## Folder Structure

- dnc_arrivals:
  Token bucket and piecewise linear arrival curve and the abstract class ArrivalCurve
- dnc_leftover_service:
  FIFO leftover service 
- dnc_operations:
  Network Calculus operations, (de-)convolution and computation of performance bounds (delay, backlog, ...)
- dnc_service:
  Rate-Latency and piecewise linear service curve and the abstract class ServiceCurve
- examples:
  Examples that are referenced in the master thesis
- finite_shared_buffers:
  Operations needed for finite shared buffers setting
- output:
  The created outputs, like .html and .svg files can be found there
- plotter:
  The code to create each plot
- solution_checker:
  Brute force approaches for (de-)convolution
