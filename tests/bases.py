# coding=utf-8

import unittest

from fform.dals_pubmed import DalPubmed
from fform.orm_base import Base

from pubmed_ingester.ingesters import IngesterDocumentPubmedArticle
from pubmed_ingester.parsers import ParserXmlPubmedArticle
from pubmed_ingester.config import import_config


class TestBase(unittest.TestCase):
    """Unit-test base-class."""

    def setUp(self):
        """Instantiates the DAL and creates the schema."""

        # Load the configuration.
        self.cfg = import_config(
            fname_config_file="/etc/pubmed-ingester/pubmed-ingester-test.json",
        )

        self.dal = DalPubmed(
            sql_username=self.cfg.sql_username,
            sql_password=self.cfg.sql_password,
            sql_host=self.cfg.sql_host,
            sql_port=self.cfg.sql_port,
            sql_db=self.cfg.sql_db
        )

        self.ingester = IngesterDocumentPubmedArticle(dal=self.dal)

        self.parser = ParserXmlPubmedArticle()

        # Drop any schema remnants and recreate it.
        Base.metadata.drop_all(self.dal.engine)
        Base.metadata.create_all(self.dal.engine)

    def tearDown(self):
        """Drops the DB schema created during setup."""

        Base.metadata.drop_all(self.dal.engine)
