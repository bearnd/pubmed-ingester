# -*- coding: utf-8 -*-

""" Custom application-wide exception classes.

This module contains custom exception classes that can be used to wrap other
exception and allow for consistent error-handling across the application.
"""

from __future__ import unicode_literals


class UnhandledError(Exception):
    def __init__(self, message, *args):
        super(UnhandledError, self).__init__(message, *args)


class ConfigFileNotFound(Exception):
    """Exception raised when a JSON configuration file is missing."""
    def __init__(self, message, *args):
        super(ConfigFileNotFound, self).__init__(message, *args)


class ConfigFileInvalid(Exception):
    """Exception raised when a JSON configuration file is invalid."""
    def __init__(self, message, *args):
        super(ConfigFileInvalid, self).__init__(message, *args)


class RecordExists(Exception):
    """Exception raised when a required DB record does not exist."""
    def __init__(self, message, *args):
        super(RecordExists, self).__init__(message, *args)


class RecordDoesNotExist(Exception):
    """Exception raised when an existing DB record is overwritten."""
    def __init__(self, message, *args):
        super(RecordDoesNotExist, self).__init__(message, *args)


class InvalidArguments(Exception):
    """Exception raised when the arguments to a function/method call are
    invalid."""
    def __init__(self, message, *args):
        super(InvalidArguments, self).__init__(message, *args)
