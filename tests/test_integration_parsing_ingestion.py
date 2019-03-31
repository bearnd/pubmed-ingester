# coding=utf-8

from lxml import etree

from tests.bases import TestBase
from tests.assets.PMID1 import document as doc_pmid1
from tests.assets.PMID30516271 import document as doc_pmid30516271
from tests.assets.PMID30516272 import document as doc_pmid30516272
from tests.assets.PMID30516273 import document as doc_pmid30516273
from tests.assets.PMID30516284 import document as doc_pmid30516284
from tests.assets.PMID30516287 import document as doc_pmid30516287
from tests.assets.PMID30518562 import document as doc_pmid30518562


class TestIntegrationParsingIngestion(TestBase):
    """Full integration tests including parsing and ingestion."""

    def _parse_sample(self, sample):
        """ Parses a PubMed article XML document and returns the parsed
            document.
        """

        # Perform an XML parsing of the document.
        element = etree.fromstring(text=sample)

        # Parse the pubmed-article XML element.
        article = self.parser.parse_pubmed_article(element=element)

        return article

    def test_integration_ingest_pmid1(self):
        """ Tests the `ingest` method of the `IngesterDocumentPubmedArticle`
            class by ingesting the PMID1 PubMed article XML document
            asserting that parsing and ingestion were successful.
        """

        article = self._parse_sample(sample=doc_pmid1)

        # Ingest the parsed article document.
        obj_id = self.ingester.ingest(document=article)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_pmid30516271(self):
        """ Tests the `ingest` method of the `IngesterDocumentPubmedArticle`
            class by ingesting the PMID30516271 PubMed article XML document
            asserting that parsing and ingestion were successful.
        """

        article = self._parse_sample(sample=doc_pmid30516271)

        # Ingest the parsed article document.
        obj_id = self.ingester.ingest(document=article)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_pmid30516272(self):
        """ Tests the `ingest` method of the `IngesterDocumentPubmedArticle`
            class by ingesting the PMID30516272 PubMed article XML document
            asserting that parsing and ingestion were successful.
        """

        article = self._parse_sample(sample=doc_pmid30516272)

        # Ingest the parsed article document.
        obj_id = self.ingester.ingest(document=article)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_pmid30516273(self):
        """ Tests the `ingest` method of the `IngesterDocumentPubmedArticle`
            class by ingesting the PMID30516273 PubMed article XML document
            asserting that parsing and ingestion were successful.
        """

        article = self._parse_sample(sample=doc_pmid30516273)

        # Ingest the parsed article document.
        obj_id = self.ingester.ingest(document=article)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_pmid30516284(self):
        """ Tests the `ingest` method of the `IngesterDocumentPubmedArticle`
            class by ingesting the PMID30516284 PubMed article XML document
            asserting that parsing and ingestion were successful.
        """

        article = self._parse_sample(sample=doc_pmid30516284)

        # Ingest the parsed article document.
        obj_id = self.ingester.ingest(document=article)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_pmid30516287(self):
        """ Tests the `ingest` method of the `IngesterDocumentPubmedArticle`
            class by ingesting the PMID30516287 PubMed article XML document
            asserting that parsing and ingestion were successful.
        """

        article = self._parse_sample(sample=doc_pmid30516287)

        # Ingest the parsed article document.
        obj_id = self.ingester.ingest(document=article)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_pmid30518562(self):
        """ Tests the `ingest` method of the `IngesterDocumentPubmedArticle`
            class by ingesting the PMID30518562 PubMed article XML document
            asserting that parsing and ingestion were successful.
        """

        article = self._parse_sample(sample=doc_pmid30518562)

        # Ingest the parsed article document.
        obj_id = self.ingester.ingest(document=article)

        self.assertEqual(obj_id, 1)
