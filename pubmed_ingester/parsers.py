# -*- coding: utf-8 -*-

import abc
import gzip
from lxml import etree

from .loggers import create_logger
from .parser_utils import parse_date_element
from .parser_utils import convert_yn_boolean
from .parser_utils import clean_orcid_identifier


class ParserXmlBase(object):
    def __init__(self, **kwargs):

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

    @staticmethod
    def _et(element):
        """Extracts the element text (ET)"""

        text = None
        if element is not None:
            text = element.text

        return text

    @staticmethod
    def _eav(element, attribute):
        """Extracts the element attrbiute value (EAV)"""

        value = None
        if element is not None:
            value = element.get(attribute)

        return value

    @staticmethod
    def generate_xml_elements(file_xml, element_tag=None):

        document = etree.iterparse(
            file_xml,
            events=("start", "end"),
            tag=element_tag
        )

        _, element_root = next(document)
        start_tag = None
        for event, element in document:
            if event == 'start' and start_tag is None:
                start_tag = element.tag
            if event == 'end' and element.tag == start_tag:
                yield element
                start_tag = None
                element_root.clear()

    def open_xml_file(self, filename_xml):

        msg_fmt = "Opening XML file '{0}'".format(filename_xml)
        self.logger.info(msg=msg_fmt)

        if filename_xml.endswith(".gz"):
            file_xml = gzip.GzipFile(filename=filename_xml, mode="rb")
        else:
            file_xml = open(filename_xml, "rb")

        return file_xml

    @abc.abstractmethod
    def parse(self, filename_xml):
        raise NotImplementedError


class ParserXmlPubmedArticle(ParserXmlBase):
    def __init__(self, **kwargs):

        super(ParserXmlPubmedArticle).__init__(kwargs=kwargs)

    def parse_medline_journal_info(self, element):

        if element is None:
            return {}

        medline_journal_info = {
            "Country": self._et(element.find("Country")),
            "MedlineTA": self._et(element.find("MedlineTA")),
            "NlmUniqueID": self._et(element.find("NlmUniqueID")),
            "ISSNLinking": self._et(element.find("ISSNLinking")),
        }

        return medline_journal_info

    def parse_chemical(self, element):

        if element is None:
            return {}

        chemical = {
            "RegistryNumber": self._et(element.find("RegistryNumber")),
            "NameOfSubstance": {
                "UI": self._eav(element.find("NameOfSubstance"), "UI"),
                "NameOfSubstance": self._et(element.find("NameOfSubstance")),
            },
        }

        return chemical

    def parse_chemical_list(self, element):

        chemicals = []

        if element is None:
            return chemicals

        for _element in element.getchildren():
            chemical = self.parse_chemical(_element)
            chemicals.append(chemical)

        return chemicals

    def parse_mesh_entry(self, element, entry_name):

        mesh_entry = {}

        if element is None:
            return mesh_entry

        mesh_entry = {
            entry_name: self._et(element),
            "UI": self._eav(element, "UI"),
            "MajorTopicYN": self._eav(element, "MajorTopicYN"),
        }

        mesh_entry["IsMajorTopic"] = convert_yn_boolean(
            mesh_entry["MajorTopicYN"]
        )

        return mesh_entry

    def parse_mesh_descriptor(self, element):

        mesh_descriptor = self.parse_mesh_entry(
            element=element,
            entry_name="DescriptorName"
        )

        return mesh_descriptor

    def parse_mesh_qualifier(self, element):

        mesh_descriptor = self.parse_mesh_entry(
            element=element,
            entry_name="QualifierName"
        )

        return mesh_descriptor

    def parse_mesh_heading(self, element):

        if element is None:
            return {}

        mesh_heading = {
            "DescriptorName": self.parse_mesh_descriptor(
                element.find("DescriptorName")
            ),
            "Qualifiers": [{
                "Qualifier": self.parse_mesh_qualifier(
                    _element for _element in
                    element.findall("Qualifier")
                )
            }]
        }

        return mesh_heading

    def parse_mesh_heading_list(self, element):

        mesh_headings = []

        if element is None:
            return mesh_headings

        for _element in element.getchildren():
            mesh_heading = self.parse_mesh_heading(_element)
            mesh_headings.append(mesh_heading)

        return mesh_headings

    def parse_keyword(self, element):

        if element is None:
            return {}

        keyword = {
            "Keyword": self._et(element),
            "UI": self._eav(element, "UI"),
            "MajorTopicYN": self._eav(element, "MajorTopicYN"),
        }

        keyword["IsMajorTopic"] = convert_yn_boolean(
            keyword["MajorTopicYN"]
        )

        return keyword

    def parse_keyword_list(self, element):

        keywords = []

        if element is None:
            return keywords

        for _element in element.getchildren():
            keyword = self.parse_keyword(_element)
            keywords.append(keyword)

        return keywords

    def parse_journal(self, element):

        if element is None:
            return {}

        journal = {
            "ISSN": {
                "ISSN": self._et(element.find("ISSN")),
                "IssnType": self._eav(
                    element=self._et(element.find("ISSN")),
                    attribute="IssnType"
                )
            },
            "JournalIssue": {
                "Volume": self._et(element.find("Volume")),
                "Issue": self._et(element.find("Issue")),
                "PubDate": parse_date_element(element.find("PubDate")),
            },
            "Title": self._et(element.find("Title")),
            "ISOAbbreviation": self._et(element.find("ISOAbbreviation")),
        }

        return journal

    def parse_affiliation_info(self, element):

        if element is None:
            return {}

        affiliation_info = {
            "Identifier": {
                "Source": self._eav(element.find("Identifier"), "Source"),
                "Identifier": self._et(element.find("Identifier"))
            },
            "Affiliations": [{
                "Affiliation": self._et(_element)
                for _element in element.getchildren()
            }]
        }

        return affiliation_info

    def parse_author(self, element):

        if element is None:
            return {}

        author = {
            "ValidYN": self._eav(element, "ValidYN"),
            "LastName": self._et(element.find("LastName")),
            "ForeName": self._et(element.find("ForeName")),
            "Initials": self._et(element.find("Initials")),
            "Identifier": {
                "Source": self._eav(element.find("Identifier"), "Source"),
                "Identifier": self._et(element.find("Identifier"))
            },
            "AffiliationInfo": self.parse_affiliation_info(
                element.find("AffiliationInfo")
            )
        }

        author["IsValid"] = convert_yn_boolean(author["ValidYN"])

        if author["Identifier"]["Source"] == "ORCID":
            author["Identifier"]["Identifier"] = clean_orcid_identifier(
                author["Identifier"]["Identifier"]
            )

    def parse_author_list(self, element: etree.Element) -> dict:

        if element is None:
            return {}

        author_list = {
            "CompleteYN": self._eav(element, "CompleteYN"),
            "Authors": [{
                "Author": self.parse_author(_element)
                for _element in element.findall("Author")
            }]
        }

        return author_list

    def parse_abstract(self, element):

        abstract = []

        if element is None:
            return abstract

        for element_abstract_text in element.getchildren():
            abstract_text = {
                "AbstractText": self._et(
                    element_abstract_text.find("AbstractText")
                ),
                "Label": self._eav(
                    element_abstract_text.find("AbstractText"),
                    "Label"
                ),
                "NlmCategory": self._eav(
                    element_abstract_text.find("AbstractText"), "NlmCategory"
                ),
            }
            abstract.append(abstract_text)

        return abstract

    def parse_pagination(self, element: etree.Element) -> dict:

        if element is None:
            return {}

        pagination = {
            "MedlinePgn": self._et(element.find("MedlinePgn"))
        }

        return pagination

    def parse_publication_type(self, element):

        if element is None:
            return {}

        publication_type = {
            "PublicationType": self._et(element),
            "UI": self._eav(element, "UI"),
        }

        return publication_type

    def parse_publication_type_list(self, element):

        publication_type_list = []

        if element is None:
            return publication_type_list

        for _element in element.getchildren():
            publication_type = self.parse_publication_type_list(_element)
            publication_type_list.append(publication_type)

        return publication_type_list

    def parse_article(self, element):

        article = {
            "Journal": self.parse_journal(element.find("Journal")),
            "ArticleTitle": self._et(element.find("ArticleTitle")),
            "Pagination": self.parse_pagination(element.find("Pagination")),
            "Abstract": self.parse_abstract(element.find("Abstract")),
            "AuthorList": self.parse_author_list(element.find("AuthorList")),
            "Language": self._et(element.find("Language")),
            # TODO
            "DataBankList": None,
            "PublicationTypeList": self.parse_publication_type_list(
                element.find("PublicationTypeList")
            ),
            "ArticleDate": parse_date_element(element.find("ArticleDate"))
        }

        return article

    def parse_medline_citation(self, element):

        medline_citation = {
            "Status": self._eav(element, "Status"),
            "Owner": self._eav(element, "Owner"),
            "PMID": {
                "PMID": self._et(element.find("PMID")),
                "Version": self._eav(element.find("PMID"), "Version")
            },
            "DateCreated": parse_date_element(
                date_element=element.find("DateCreated")
            ),
            "DateCompleted": parse_date_element(
                date_element=element.find("DateCompleted")
            ),
            "DateRevised": parse_date_element(
                date_element=element.find("DateRevised")
            ),
            "Article": self.parse_article(element.find("Article")),
            "MedlineJournalInfo": self.parse_medline_journal_info(
                element.find("MedlineJournalInfo")
            ),
            "ChemicalList": self.parse_chemical_list(
                element.find("ChemicalList")
            ),
            # The `<CitationSubset>` element is skipped.
            "MeshHeadingList": self.parse_mesh_heading_list(
                element.find("MeshHeadingList")
            ),
            "KeywordList": self.parse_keyword_list(
                element.find("KeywordList")
            )
        }

        return medline_citation

    def parse_article_id(self, element):

        if element is None:
            return {}

        article_id = {
            "ArticleId": self._et(element),
            "IdType": self._eav(element, "IdType"),
        }

        return article_id

    def parse_article_id_list(self, element):

        article_ids = []

        if element is None:
            return article_ids

        for _element in element.getchildren():
            article_id = self.parse_article_id(_element)
            article_ids.append(article_id)

        return article_ids

    def parse_pubmed_data(self, element):

        pubmed_data = {
            # The `<History>` element is skipped.
            # The `<PublicationStatus>` element is skipped.
            "ArticleIdList": self.parse_article_id_list(
                element.find("ArticleIdList")
            )
        }

        return pubmed_data

    def parse(self, filename_xml):

        msg_fmt = "Parsing Pubmed XML file '{0}'".format(filename_xml)
        self.logger.info(msg=msg_fmt)

        file_xml = self.open_xml_file(filename_xml=filename_xml)

        elements_pubmed_articles = self.generate_xml_elements(
            file_xml=file_xml,
            element_tag="PubmedArticle"
        )

        for element_pubmed_article in elements_pubmed_articles:
            pubmed_article = {
                "citation": self.parse_medline_citation(
                    element_pubmed_article.find("MedlineCitation")
                ),
                "pubmed": self.parse_pubmed_data(
                    element_pubmed_article.find("PubmedData")
                )
            }

            yield pubmed_article
