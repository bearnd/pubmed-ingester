#!/usr/bin/python
# -*- coding: utf-8 -*-

import pubmed_ingester

cfg = pubmed_ingester.config.import_config(
    "/etc/pubmed-ingester/pubmed-ingester.json"
)

dal = pubmed_ingester.dals.DalPubmed(
    sql_username=cfg.sql_username,
    sql_password=cfg.sql_password,
    sql_host=cfg.sql_host,
    sql_port=cfg.sql_port,
    sql_db=cfg.sql_db,
)

parser = pubmed_ingester.parsers.ParserXmlPubmedArticle()
pubmed_articles = parser.parse(filename_xml="medsample1.xml.gz")

ingester = pubmed_ingester.ingesters.IngesterDocumentPubmedArticle(dal=dal)

for pubmed_article in pubmed_articles:
    ingester.ingest(document=pubmed_article)
