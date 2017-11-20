# -*- coding: utf-8 -*-

import decorator

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


def log_ingestion_of_documents(
    document_name: str
):

    # Define the actual decorator. This three-tier decorator functions are
    # necessary when defining decorator functions with arguments.
    def log_ingestion_of_entries_decorator(func):
        # Define the wrapper function.
        def wrapper(self, *args, **kwargs):

            documents = kwargs.get("documents")
            if documents is None:
                for arg in args:
                    if isinstance(arg, list):
                        documents = arg
                        break
            if documents is None:
                msg_fmt = "No `list` argument found."
                raise InvalidArguments(msg_fmt)

            msg = "Ingesting {} '{}' documents"
            msg_fmt = msg.format(len(documents), document_name)
            self.logger.debug(msg_fmt)

            # Simply execute the decorated method with the provided arguments
            # and return the result.
            return func(self, *args, **kwargs)

        return wrapper

    return log_ingestion_of_entries_decorator


def log_ingestion_of_document(
    document_name: str
):

    # Define the actual decorator. This three-tier decorator functions are
    # necessary when defining decorator functions with arguments.
    def log_ingestion_of_document_decorator(func):
        # Define the wrapper function.
        def wrapper(self, *args, **kwargs):

            msg = "Ingesting '{}' document"
            msg_fmt = msg.format(document_name)
            self.logger.debug(msg_fmt)

            # Simply execute the decorated method with the provided arguments
            # and return the result.
            return func(self, *args, **kwargs)

        return wrapper

    return log_ingestion_of_document_decorator
