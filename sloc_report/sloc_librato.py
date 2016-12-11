# -*- coding: utf-8 -*-
# Helpers for python-librato module
import exceptions
import librato


class LibratoApi(object):
    """Api wraps the librato API"""

    def __init__(self, **kwargs):
        self.email = kwargs.pop('email', None)
        self.token = kwargs.pop('token', None)
        if (self.email or self.token) is None:
            raise exceptions.MissingRequiredConfig(
                'Missing authentication info')
        self.connection = librato.connect(self.email, self.token)

    def charts_for_space(self, space):
        """Return all of the charts within a space"""
        space = self.connection.find_space(space)
        charts = []
        for chart in space.charts():
            charts.insert(0, SlocChart(chart))
        return charts


def _validate_chart(chart):
    """Validate that a chart object matches what we expect"""
    if len(chart.streams) == 0:
        raise exceptions.NoStreamsFound(
            'Chart has no streams')
    elif len(chart.streams) > 1:
        raise exceptions.TooManyStreamsFound(
            'Chart has more streams than expected')


def _composite_options(**kwargs):
    """Return a string representation of options that can be appended to a
    composite metric query
    """
    string = '{'
    num_keys = len(kwargs.keys()) - 1
    for index, key in enumerate(kwargs):
        string += '{}'.format(key)
        string += ': '
        string += '"{}"'.format(kwargs[key])
        if not index >= num_keys:
            string += ', '
    string += '}'
    return string


def _quote_string(string):
    """Double-quote a string"""
    return '"{}"'.format(string)


def _transform_function(function, options={}, *args):
    """Return a string representation of a transformation function

    NOTE: This is only compatible with max/mean/min and similar functions in
    current state
    """
    string = '{}(s('.format(function)
    string += ', '.join(map(_quote_string, args))
    if options:
        string += ', {}'.format(options)
    string += '))'
    return string


# TODO: better way of working out whether or not a chart has composite metrics
class SlocChart(object):
    """Helper methods around a librato Chart object

    Currently, only charts with a single stream are supported
    """
    def __init__(self, chart, **kwargs):
        _validate_chart(chart)
        self.chart = chart
        self.period = kwargs.get('period', 3600)
        self.threshold = kwargs.get('threshold')
        self.is_composite = kwargs.get('is_composite', True)
        self.space_name = kwargs.get('space_name')

    def group_function(self):
        return self.chart.streams[0].group_function

    def source(self):
        return self.chart.streams[0].source

    def metric(self):
        return self.chart.streams[0].metric

    def group_transform(self):
        """Return a string representation of a metric transformation function
        configured for whatever the charts group_function is
        Only relevent when is_composite is True
        """
        options = _composite_options(period=self.period)
        return _transform_function(
            self.group_function(),
            options,
            self.metric(),
            self.source(),
        )
