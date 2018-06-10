# coding=utf-8

from pubmed_ingester.excs import InvalidArguments


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
