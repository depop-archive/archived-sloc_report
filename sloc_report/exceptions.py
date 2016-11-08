# -*- coding: utf-8 -*-
# Exceptions module


class MaxRetriesAttempted(Exception):
    pass


class ChartNotFound(ValueError):
    pass


class SpaceNotFound(ValueError):
    pass


class TooManyStreamsFound(ValueError):
    pass


class NoStreamsFound(ValueError):
    pass


class MissingRequiredConfig(ValueError):
    pass
