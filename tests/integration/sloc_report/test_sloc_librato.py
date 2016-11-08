# -*- coding: utf-8 -*-
import pytest
import os
from sloc_report import sloc_librato


@pytest.fixture
def librato_email(email=os.environ.get('LIBRATO_EMAIL')):
    """Return librato email from an environment variable"""
    return email


@pytest.fixture
def librato_token(token=os.environ.get('LIBRATO_TOKEN')):
    """Return librato API token from an environment variable"""
    return token


@pytest.fixture
def librato_test_space(test_space=os.environ.get('LIBRATO_TEST_SPACE')):
    """Return librato test space from an environment variable"""
    return test_space


def test_charts_for_space():
    api = sloc_librato.LibratoApi(email=librato_email(), token=librato_token())
    charts = api.charts_for_space(librato_test_space())
    assert len(charts) >= 1
