#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main module."""

import os
import argparse

from fform.dals_pubmed import DalPubmed

from pubmed_ingester.ingesters import IngesterDocumentPubmedArticle
from pubmed_ingester.parsers import ParserXmlPubmedArticle
from pubmed_ingester.config import import_config


def load_config(args):
    if args.config_file:
        cfg = import_config(fname_config_file=args.config_file)
    elif "PUBMED_INGESTER_CONFIG" in os.environ:
        fname_config_file = os.environ["PUBMED_INGESTER_CONFIG"]
        cfg = import_config(fname_config_file=fname_config_file)
    else:
        msg_fmt = "Configuration file path not defined."
        raise ValueError(msg_fmt)

    return cfg


def main(args):
    cfg = load_config(args=args)

    dal = DalPubmed(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host=cfg.sql_host,
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )
    ingester = IngesterDocumentPubmedArticle(dal=dal)

    parser = ParserXmlPubmedArticle()
    for filename in args.filenames:
        pubmed_articles = parser.parse(filename_xml=filename)

        for pubmed_article in pubmed_articles:
            ingester.ingest(document=pubmed_article)


# main sentinel
if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(
        description=("pubmed-ingester: Pubmed XML dump parser and SQL"
                     " ingester.")
    )
    argument_parser.add_argument(
        "filenames",
        nargs="+",
        help="Pubmed XML files to ingest.",
    )
    argument_parser.add_argument(
        "--config-file",
        dest="config_file",
        help="configuration file",
        required=False
    )
    arguments = argument_parser.parse_args()

    main(args=arguments)
