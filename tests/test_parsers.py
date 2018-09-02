# coding=utf-8

import io
import pytest

from lxml import etree

from pubmed_ingester.parsers import ParserXmlPubmedArticle

from tests.assets.pubmed_sample_xml import pubmed_sample_xml
from tests.assets.pubmed_sample_parsed import pubmed_sample_parsed


@pytest.fixture(name="parser")
def get_parser():
    return ParserXmlPubmedArticle()


@pytest.fixture(name="element_pubmed_article")
def get_element_pubmed_article():
    tree = etree.fromstring(pubmed_sample_xml.encode("utf-8"))
    return tree.find("PubmedArticle")


@pytest.fixture(name="element_citation")
def get_element_citation():
    element_pubmed_article = get_element_pubmed_article()
    return element_pubmed_article.find("MedlineCitation")


@pytest.fixture(name="element_article")
def get_element_article():
    element_citation = get_element_citation()
    return element_citation.find("Article")


@pytest.fixture(name="element_medline_journal_info")
def get_element_medline_journal_info():
    element_citation = get_element_citation()
    return element_citation.find("MedlineJournalInfo")


@pytest.fixture(name="element_journal")
def get_element_journal():
    element_article = get_element_article()
    return element_article.find("Journal")


def test_parse_pubmed_article(parser, element_pubmed_article):
    """Tests the `parse_pubmed_article` method of the `ParserXmlPubmedArticle`
    class."""

    pubmed_article_refr = pubmed_sample_parsed

    pubmed_article_eval = parser.parse_pubmed_article(element_pubmed_article)

    assert pubmed_article_eval == pubmed_article_refr


def test_parse_pubmed_data(
    parser,
    element_pubmed_article,
):
    """Tests the `parse_pubmed_data` method of the `ParserXmlPubmedArticle`
    class."""

    pubmed_data_refr = pubmed_sample_parsed["PubmedData"]

    pubmed_data_eval = parser.parse_pubmed_data(
        element_pubmed_article.find("PubmedData"),
    )

    assert pubmed_data_eval == pubmed_data_refr


def test_parse_article_id_list(
    parser,
    element_pubmed_article,
):
    """Tests the `parse_article_id_list` method of the `ParserXmlPubmedArticle`
    class."""

    article_id_list_refr = pubmed_sample_parsed["PubmedData"]["ArticleIdList"]

    article_id_list_eval = parser.parse_article_id_list(
        element_pubmed_article.find("PubmedData").find("ArticleIdList"),
    )

    assert article_id_list_eval == article_id_list_refr


def test_parse_article_id(
    parser,
    element_pubmed_article,
):
    """Tests the `parse_article_id` method of the `ParserXmlPubmedArticle`
    class."""

    article_id_refr = pubmed_sample_parsed[
        "PubmedData"
    ]["ArticleIdList"]["ArticleIds"][0]["ArticleId"]

    article_id_eval = parser.parse_article_id(
        element_pubmed_article.find(
            "PubmedData"
        ).find("ArticleIdList").find("ArticleId"),
    )

    assert article_id_eval == article_id_refr


def test_parse_medline_citation(
    parser,
    element_citation,
):
    """Tests the `parse_medline_citation` method of the `ParserXmlPubmedArticle`
    class."""

    medline_citation_refr = pubmed_sample_parsed["MedlineCitation"]

    medline_citation_eval = parser.parse_medline_citation(element_citation)

    assert medline_citation_eval == medline_citation_refr


def test_parse_article(
    parser,
    element_article,
):
    """Tests the `parse_article` method of the `ParserXmlPubmedArticle`
    class."""

    article_refr = pubmed_sample_parsed["MedlineCitation"]["Article"]

    article_eval = parser.parse_article(element_article)

    assert article_eval == article_refr


def test_parse_journal_issue(parser, element_journal):
    """Tests the `parse_journal_issue` method of the `ParserXmlPubmedArticle`
    class."""

    journal_issue_refr = pubmed_sample_parsed[
        "MedlineCitation"
    ]["Article"]["Article"]["Journal"]["JournalIssue"]

    element_journal_issue = element_journal.find("JournalIssue")
    journal_issue_eval = parser.parse_journal_issue(element_journal_issue)

    keys = ["JournalIssue", "CitedMedium"]
    for key in keys:
        assert journal_issue_eval[key] == journal_issue_refr[key]


def test_parse_journal(parser, element_journal):
    """Tests the `parse_journal` method of the `ParserXmlPubmedArticle`
    class."""

    journal_refr = pubmed_sample_parsed[
        "MedlineCitation"
    ]["Article"]["Article"]["Journal"]

    journal_eval = parser.parse_journal(element_journal)

    keys = ["ISSN", "Title", "ISOAbbreviation"]
    for key in keys:
        assert journal_eval[key] == journal_refr[key]


def test_parse_medline_journal_info(
    parser,
    element_citation,
):
    """Tests the `parse_medline_journal_info` method of the
    `ParserXmlPubmedArticle` class."""

    medline_journal_info_refr = pubmed_sample_parsed[
        "MedlineCitation"
    ]["MedlineJournalInfo"]

    medline_journal_info_eval = parser.parse_medline_journal_info(
        element_citation.find("MedlineJournalInfo"),
    )

    keys = ["Country", "ISSNLinking", "MedlineTA", "NlmUniqueID"]

    for key in keys:
        assert medline_journal_info_eval[key] == medline_journal_info_refr[key]

