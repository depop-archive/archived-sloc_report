# -*- coding: utf-8 -*-
# Run Service Level Objective Compliance reports
import exceptions
import sloc_time
import sloc_librato
import librato.exceptions


def _validate_charts(space, charts):
    """Validate that every chart within the space exists

    :param space: A Librato Space object
    :param charts: Enumerable/List of chart names within the Space object
    """
    charts = list(charts)
    to_find = len(charts)
    for i in space.charts():
        if i.name in charts:
            # chart found - remove it from list so not searched for again
            charts.remove(i.name)
            to_find -= 1
            if to_find == 0:
                # found all of them - return without searching any further
                return True
    if to_find != 0:
        raise exceptions.ChartNotFound(
            'Could not find charts {} in space {}'.format(charts, space)
        )


def _enumerate_sloc_charts(api, space_name, charts, default_period=3600):
    """Returns a list of enumerated SlocChart objects

    :param api: LibratoApi object
    :param space_name: The name of the space where the charts are located
    :param charts: List of dicts containing chart configuration
    :param default_period: The period to apply the SLO thresholds to in
                           seconds if this is not specified within the incoming
                           data.  Default is 3600 (one hour), resulting in 24
                           measurements and comparisons against the SLO
                           threshold

    Example structure for charts:
    [ { threshold: 100, chart_name: 'a', is_composite: False, period: 3600 },
      { threshold: 150, chart_name: 'another chart' } ]
    """
    # validate that the space actually
    space = api.connection.find_space(space_name)
    if not space:
        raise exceptions.SpaceNotFound(
            'Could not find space "{}"'.format(space_name)
        )
    # Validate that all charts exist
    chart_names = map(lambda x: x['chart_name'], charts)
    _validate_charts(space, chart_names)
    sloc_charts = []
    # create a list of SlocChart objects
    for chart in charts:
        # set the default period unless one is explicitly defined
        period = chart.get('period', default_period)
        # all charts are assumed to be composites unless explicitly configured
        is_composite = chart.get('is_composite', True)
        if is_composite is False:
            raise NotImplementedError(
                'non-composite metrics not supported yet'
            )
        sloc_charts.append(
            sloc_librato.SlocChart(
                api.connection.find_chart(chart['chart_name'], space),
                period=period,
                threshold=chart['threshold'],
                is_composite=is_composite,
                space_name=space_name,
            )
        )
    return sloc_charts


def _get_composite_with_retry(api, chart, **kwargs):
    """Returns: dict response of the LibratoConnection.get_composite()'

    Current version of librato API appears to return a 400 with no error
    message if we request a composite metric for a time period, and it does not
    have data at the requested resolution available.

    This function will attempt to retrive the composite metric at the
    configured resolution; if it raises a 400 BadRequest, it will then retry
    for retries attempts, multiplying resolution by 2 each time

    :param api: LibratoApi object
    :param chart: SlocChart object
    :param retries: Number of retries

    :Keyword Arguments:
        * *start_time* (``int``) --
          REQUIRED -  Start time as unix time to start from
        * *end_time* (``int``) --
          REQUIRED - End time as unix time
        * *resolution* (``int``) --
          Intial resolution (in seconds) to request data for. Default: 30
        * *retries* (``int``) --
          Number of retries to attempt. Default: 10
    """
    resolution = kwargs.get('resolution', 30)
    retries = kwargs.get('retries', 10)
    end_time = kwargs.get('end_time')
    start_time = kwargs.get('start_time')
    if (start_time or end_time) is None:
        raise ValueError('Need both start_time and end_time kwargs')
    for attempt in range(retries):
        try:
            response = api.connection.get_composite(
                chart.group_transform(),
                start_time=start_time,
                end_time=end_time,
                resolution=resolution,
            )
        except librato.exceptions.BadRequest:
            resolution = (resolution * 2)
        else:
            break
    else:
        raise exceptions.MaxRetriesAttempted(
            'Tried {} times to get composite '.format(attempt + 1) +
            'metric. Last attempt was at resolution {} seconds'
            .format(resolution)
        )
    return response


def daily_report(api, space_name, charts, num_days=1, end_time=None):
    """Get a report of SLO Compliance for the previous day(s)

    Returns: list of dicts of threshold breaches. Example Dict format:
    {u'measure_time': 1478462400, u'value': 115.58158333333334}

    :param api: An instance of sloc_report.LibratoApi
    :param space_name: The name of the space where the charts are located
    :param charts: A list of dicts containing the SLO thresholds, indexed
                   by the chart names (see _enumerate_sloc_charts() for an
                   example data structure)
    :param num_days: Number of days to get report for. Default is 1 day
    :param end_time: The time that the report should count back from.
                     Default: now
    """
    sloc_charts = _enumerate_sloc_charts(api, space_name, charts)
    if end_time is None:
        end_time = sloc_time.time_now()

    # get start and end times for each day
    days = sloc_time.get_day_times(num_days, end_time)
    threshold_breaches = []

    # loop through every day for every chart
    # TODO: decide on a better data structure - or return an object per chart?
    for chart in sloc_charts:
        chart_breaches = {
            'chart_name': chart.metric(), 'total': 0, 'breaches': []
        }
        for day in days:
            response = _get_composite_with_retry(
                api, chart,
                start_time=day[0],
                end_time=day[1]
            )
            # build a list of threshold breaches
            for s in response['measurements'][0]['series']:
                if s['value'] > chart.threshold:
                    chart_breaches['total'] += 1
                    # chart_breaches['breaches'].append(s)
        threshold_breaches.append(chart_breaches)
    return threshold_breaches
