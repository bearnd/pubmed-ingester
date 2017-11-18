# -*- coding: utf-8 -*-

from pubmed_ingester.excs import InvalidArguments


def lists_equal_length(func):
    """Decorator that ensures all ``list`` objects in a method's arguments
    have the same length"""
    # Define the wrapper function.
    def wrapper(self, *args, **kwargs):

        # Collect all `list` objects from `args`.
        lists_args = [arg for arg in args if isinstance(arg, list)]
        # Collecgt all `list` object from `kwargs`.
        lists_kwargs = [arg for arg in kwargs.values() if isinstance(arg, list)]
        # Concatenate the lists of `list` objects.
        lists = lists_args + lists_kwargs

        # Check whether all the `list` objects have the same length.
        do_have_same_length = len(set(map(len, lists))) == 1

        # Raise an `InvalidArguments` exception if there's a length mismatch.
        if not do_have_same_length:
            msg_fmt = "The argument lists must have the same length."
            raise InvalidArguments(msg_fmt)

        # Simply execute the decorated method with the provided arguments
        # and return the result.
        return func(self, *args, **kwargs)

    return wrapper
