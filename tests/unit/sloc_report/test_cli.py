# -*- coding: utf-8 -*-
from click.testing import CliRunner
from sloc_report import cli


def test_slocr_help():
    """Assert basic output of root --help switch"""
    runner = CliRunner()
    result = runner.invoke(cli.cli_report, ['--help'])
    assert result.exit_code == 0
    assert '--librato-email' in result.output
    assert '--librato-token' in result.output
    assert 'daily' in result.output
    assert '--space' not in result.output


def test_slocr_list_charts_help():
    """Test basic output of list_charts subcommand with --help switch"""
    runner = CliRunner()
    result = runner.invoke(cli.cli_report, ['list_charts', '--help'])
    assert result.exit_code == 0
    assert '--librato-email' not in result.output
    assert '--librato-token' not in result.output
    assert '--space' in result.output


def test_slocr_daily_help():
    """Test basic output of daily subcommand with --help switch"""
    runner = CliRunner()
    result = runner.invoke(cli.cli_report, ['daily', '--help'])
    assert result.exit_code == 0
    assert '--librato-email' not in result.output
    assert '--librato-token' not in result.output
    assert '--space' in result.output
