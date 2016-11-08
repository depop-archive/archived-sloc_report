# -*- coding: utf-8 -*-
import pytest
import librato
from sloc_report import exceptions
from sloc_report import sloc_librato


@pytest.fixture
def empty_stream():
    """An empty librato stream"""
    return librato.streams.Stream()


@pytest.fixture
def chart_with_streams(num_streams=0):
    """Return a librato chart object with 0 or more streams"""
    # dummy libratoConnection
    connection = 'foo'
    chart = librato.Chart(connection)
    for stream in range(0, num_streams):
        chart.streams.append(empty_stream())
        chart.streams[0].group_function = 'max'
        chart.streams[0].metric = 'foo.bar'
    return chart


def test_slocchart_group_transform():
    """Test the output of group_transform"""
    sloc_chart = sloc_librato.SlocChart(chart_with_streams(1))
    assert sloc_chart.group_transform() == \
        'max(s("foo.bar", "*", {period: "3600"}))'


def test_slocchart_composite_options():
    """Test the output of composite options"""
    assert sloc_librato._composite_options() == \
        '{}'
    assert sloc_librato._composite_options(foo='bar') == \
        '{foo: "bar"}'
    assert sloc_librato._composite_options(num=999, baz='bar') == \
        '{num: "999", baz: "bar"}'


def test_slocchart_transform_function():
    """Test the output of transform function"""
    assert sloc_librato._transform_function('mean', {}, 'foo.bar', '*') == \
        'mean(s("foo.bar", "*"))'
    options = sloc_librato._composite_options(function='mean', period=3600)
    assert sloc_librato._transform_function(
        'mean',
        options,
        'foo.bar', '*prod*'
    ) == 'mean(s("foo.bar", "*prod*", {function: "mean", period: "3600"}))'


def test_slocchart_source():
    """Test that we get a default source back"""
    sloc_chart = sloc_librato.SlocChart(chart_with_streams(1))
    assert sloc_chart.source() == '*'


def test_slocchart_no_streams():
    """Test behavior when we pass a chart with no streams"""
    chart_with_zero_streams = chart_with_streams(0)
    with pytest.raises(exceptions.NoStreamsFound) as cred_err:
        sloc_librato.SlocChart(chart_with_zero_streams)
    assert 'Chart has no streams' in str(cred_err.value)


def test_slocchart_two_streams():
    """Test behavior when we pass a chart with two streams"""
    chart_with_two_streams = chart_with_streams(2)
    with pytest.raises(exceptions.TooManyStreamsFound) as cred_err:
        sloc_librato.SlocChart(chart_with_two_streams)
    assert 'Chart has more streams than expected' in str(cred_err.value)


def test_api_raises_on_no_credentials():
    '''Verify that it raises when we have no credentials'''
    with pytest.raises(exceptions.MissingRequiredConfig) as cred_err:
        sloc_librato.LibratoApi()
    assert 'Missing authentication info' in str(cred_err.value)
