# -*- coding: utf-8 -*-
import pytest
from sloc_report import sloc_time


@pytest.fixture
def fixed_pit():
    """A fixed point in time"""
    return 1478276024


@pytest.fixture
def a_day_of_seconds():
    return 24 * 3600


@pytest.fixture
def time_now_minus_one_day(now_time=sloc_time.time_now()):
    '''Return time minus one day'''
    return now_time - (24 * 3600)


def test_get_minus_day_time():
    """Get the times for minus 1 days"""
    assert sloc_time.get_day_times(-1) == []


def test_get_zero_day_time():
    """Get the times for no days"""
    assert sloc_time.get_day_times(0) == []


def test_get_one_day_time():
    """Get the times for one day"""
    yesterday = (fixed_pit() - a_day_of_seconds())
    assert sloc_time.get_day_times(1, fixed_pit()) == \
        [(yesterday, fixed_pit())]


def test_get_three_day_time():
    """Get the times for three days"""
    yesterday = (fixed_pit() - a_day_of_seconds())
    day_before_yesterday = (yesterday - a_day_of_seconds())
    day_before_day_before = (day_before_yesterday - a_day_of_seconds())
    assert sloc_time.get_day_times(3, fixed_pit()) == \
        [(day_before_day_before, day_before_yesterday),
         (day_before_yesterday, yesterday),
         (yesterday, fixed_pit())]
