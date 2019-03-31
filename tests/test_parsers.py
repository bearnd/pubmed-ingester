# coding=utf-8

from lxml import etree

from tests.bases import TestBase
from tests.assets.pubmed_sample_xml import pubmed_sample_xml
from tests.assets.pubmed_sample_parsed import pubmed_sample_parsed


class TestParser(TestBase):

    def _parse_sample(self, sample):
        """ Parses a PubMed article XML document and returns the parsed
            document.
        """

        # Perform an XML parsing of the document.
        element = etree.fromstring(text=sample)

        # Parse the pubmed-article XML element.
        article = self.parser.parse_pubmed_article(element=element)

        return article

    def setUp(self):
        super(TestParser, self).setUp()
        tree = etree.fromstring(pubmed_sample_xml.encode("utf-8"))
        self.article = tree.find("PubmedArticle")

    def test_parse_pubmed_article(self):
        """ Tests the `parse_pubmed_article` method of the
            `ParserXmlPubmedArticle` class.
        """

        _refr = pubmed_sample_parsed
        _eval = self.parser.parse_pubmed_article(self.article)

        self.assertEqual(_eval, _refr)

    def test_parse_pubmed_data(self):
        """ Tests the `parse_pubmed_data` method of the `ParserXmlPubmedArticle`
            class.
        """

        _refr = pubmed_sample_parsed["PubmedData"]
        _eval = self.parser.parse_pubmed_data(self.article.find("PubmedData"))

        self.assertEqual(_eval, _refr)

    def test_parse_article_id_list(self):
        """ Tests the `parse_article_id_list` method of the
            `ParserXmlPubmedArticle` class.
        """

        _refr = pubmed_sample_parsed["PubmedData"]["ArticleIdList"]
        _eval = self.parser.parse_article_id_list(
            self.article.find("PubmedData").find("ArticleIdList"),
        )

        self.assertEqual(_eval, _refr)

    def test_parse_article_id(self):
        """ Tests the `parse_article_id` method of the `ParserXmlPubmedArticle`
            class.
        """

        _refr = pubmed_sample_parsed["PubmedData"]["ArticleIdList"][
            "ArticleIds"
        ][0]["ArticleId"]

        _eval = self.parser.parse_article_id(
            self.article.find(
                "PubmedData"
            ).find("ArticleIdList").find("ArticleId"),
        )

        self.assertEqual(_eval, _refr)

    def test_parse_medline_citation(self):
        """ Tests the `parse_medline_citation` method of the
            `ParserXmlPubmedArticle` class.
        """

        _refr = pubmed_sample_parsed["MedlineCitation"]
        _eval = self.parser.parse_medline_citation(
            self.article.find("MedlineCitation")
        )

        self.assertEqual(_eval, _refr)

    def test_parse_article(self):
        """ Tests the `parse_article` method of the `ParserXmlPubmedArticle`
            class.
        """

        _refr = pubmed_sample_parsed["MedlineCitation"]["Article"]
        _eval = self.parser.parse_article(
            self.article.find("MedlineCitation").find("Article")
        )

        self.assertEqual(_eval, _refr)

    def test_parse_journal_issue(self):
        """ Tests the `parse_journal_issue` method of the
            `ParserXmlPubmedArticle` class.
        """

        _refr = pubmed_sample_parsed["MedlineCitation"]["Article"]["Article"][
            "Journal"
        ]["JournalIssue"]
        _eval = self.parser.parse_journal_issue(
            self.article.find("MedlineCitation").find("Article").find(
                "Journal"
            ).find("JournalIssue")
        )

        self.assertEqual(_eval, _refr)

    def test_parse_journal(self):
        """ Tests the `parse_journal` method of the `ParserXmlPubmedArticle`
            class.
        """

        _refr = pubmed_sample_parsed["MedlineCitation"]["Article"]["Article"][
            "Journal"
        ]
        _eval = self.parser.parse_journal(
            self.article.find("MedlineCitation").find("Article").find(
                "Journal"
            )
        )

        self.assertEqual(_eval, _refr)

    def test_parse_medline_journal_info(self):
        """ Tests the `parse_medline_journal_info` method of the
            `ParserXmlPubmedArticle` class.
        """

        _refr = pubmed_sample_parsed["MedlineCitation"]["MedlineJournalInfo"]
        _eval = self.parser.parse_medline_journal_info(
            self.article.find("MedlineCitation").find("MedlineJournalInfo")
        )

        self.assertEqual(_eval, _refr)
