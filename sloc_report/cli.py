# -*- coding: utf-8 -*-
# CLI interface
# TODO - import version from metadata
import report
import sloc_librato
import click
import os


@click.group()
@click.option('--librato-email', default=os.environ.get('LIBRATO_EMAIL'),
              help='Email address associated with the Librato account')
@click.option('--librato-token', default=os.environ.get('LIBRATO_TOKEN'),
              help='Librato API token')
@click.pass_context
def cli_report(ctx, librato_email, librato_token):
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj['librato_email'] = librato_email
    ctx.obj['librato_token'] = librato_token


@cli_report.command()
@click.option('--space', help='Name of the Librato space')
@click.option('--num-days', default=1, type=click.INT,
              help='Number of days to report for')
@click.option('--chart', multiple=True,
              help='Name of the chart(s) within the space')
@click.option('--threshold', multiple=True, type=click.FLOAT,
              help='SLO threshold of the chart(s)')
@click.pass_context
def daily(ctx, **kwargs):
    """Run a daily report."""
    space = kwargs.get('space')
    num_days = kwargs.get('num_days')
    chart = kwargs.get('chart')
    threshold = kwargs.get('threshold')
    librato_email = ctx.obj.get('librato_email')
    librato_token = ctx.obj.get('librato_token')
    api = sloc_librato.LibratoApi(email=librato_email, token=librato_token)
    charts = []
    # TODO - do this with a list comprehension
    for i, v in enumerate(chart):
        charts.append({'chart_name': v, 'threshold': threshold[i]})
    breaches = report.daily_report(api, space, charts, num_days)
    print "{}".format(breaches)
