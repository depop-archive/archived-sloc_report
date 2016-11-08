# -*- coding: utf-8 -*-
import time


def time_now():
    """returns current unix time as an integer"""
    return int(time.time())


def get_day_times(num_days=1, end_time=time_now()):
    """returns a list of tuples, where each tuple contains the start and end
    times (in unix time format, as integers) of the day(s). The end_time is by
    default the current time.

    :param num_days: Number of days to return
    :param end_time: The time to start counting back from. Default: now
    """
    day_times = []
    for day in range(0, num_days):
        start_time = end_time - (24 * 3600)
        # day_times.insert(0, (start_time, end_time))
        day_times.insert(0, (start_time, end_time))
        end_time -= (24 * 3600)
    return day_times
