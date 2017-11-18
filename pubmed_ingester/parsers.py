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

        super(ParserXmlPubmedArticle, self).__init__(kwargs=kwargs)

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

        if element is None:
            return {}

        chemical_list = {
            "Chemicals": [{
                "Chemical": self.parse_chemical(_element)
            } for _element in element.findall("Chemical")]
        }

        return chemical_list

    def parse_mesh_entry(self, element, entry_name):

        if element is None:
            return {}

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

        mesh_descriptor = self.parse_mesh_entry(element, "DescriptorName")

        return mesh_descriptor

    def parse_mesh_qualifier(self, element):

        mesh_descriptor = self.parse_mesh_entry(element, "QualifierName")

        return mesh_descriptor

    def parse_mesh_heading(self, element):

        if element is None:
            return {}

        mesh_heading = {
            "DescriptorName": self.parse_mesh_descriptor(
                element.find("DescriptorName")
            ),
            "QualifierNames": [{
                "QualifierName": self.parse_mesh_qualifier(_element)
            } for _element in element.findall("QualifierName")]
        }

        return mesh_heading

    def parse_mesh_heading_list(self, element):

        if element is None:
            return {}

        mesh_heading_list = {
            "MeshHeadings": [{
                "MeshHeading": self.parse_mesh_heading(_element)
            } for _element in element.findall("MeshHeading")]
        }

        return mesh_heading_list

    def parse_keyword(self, element):

        if element is None:
            return {}

        keyword = {
            "Keyword": self._et(element),
            "MajorTopicYN": self._eav(element, "MajorTopicYN"),
        }

        keyword["IsMajorTopic"] = convert_yn_boolean(
            keyword["MajorTopicYN"]
        )

        return keyword

    def parse_keyword_list(self, element):

        if element is None:
            return {}

        keyword_list = {
            "Keywords": [{
                "Keyword": self.parse_keyword(_element)
            } for _element in element.findall("Keyword")]
        }

        return keyword_list

    def parse_journal_issue(self, element):

        if element is None:
            return {}

        journal_issue = {
            "CitedMedium": self._eav(element, "CitedMedium"),
            "JournalIssue": {
                "Volume": self._et(element.find("Volume")),
                "Issue": self._et(element.find("Issue")),
                "PubDate": parse_date_element(element.find("PubDate")),
            }
        }

        return journal_issue

    def parse_journal(self, element):

        if element is None:
            return {}

        journal = {
            "ISSN": {
                "ISSN": self._et(element.find("ISSN")),
                "IssnType": self._eav(element.find("ISSN"), "IssnType"),
            },
            "JournalIssue": self.parse_journal_issue(
                element.find("JournalIssue")
            ),
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
            } for _element in element.findall("Affiliation")]
        }

        return affiliation_info

    def parse_author(self, element):

        if element is None:
            return {}

        author = {
            "ValidYN": self._eav(element, "ValidYN"),
            "Author": {
                "LastName": self._et(element.find("LastName")),
                "ForeName": self._et(element.find("ForeName")),
                "Initials": self._et(element.find("Initials")),
                "Suffix": self._et(element.find("Suffix")),
                "Identifier": {
                    "Source": self._eav(element.find("Identifier"), "Source"),
                    "Identifier": self._et(element.find("Identifier"))
                },
                "AffiliationInfo": self.parse_affiliation_info(
                    element.find("AffiliationInfo")
                )
            }
        }

        author["IsValid"] = convert_yn_boolean(author["ValidYN"])

        author_identifier = author["Author"]["Identifier"]
        if author_identifier["Source"] == "ORCID":
            author_identifier["Identifier"] = clean_orcid_identifier(
                author_identifier["Identifier"]
            )

        return author

    def parse_author_list(self, element: etree.Element) -> dict:

        if element is None:
            return {}

        author_list = {
            "CompleteYN": self._eav(element, "CompleteYN"),
            "Authors": [{
                "Author": self.parse_author(_element)
            } for _element in element.findall("Author")]
        }

        author_list["CompleteYN"] = convert_yn_boolean(
            author_list["CompleteYN"]
        )

        return author_list

    def parse_abstract_text(self, element):

        if element is None:
            return {}

        abstract_text = {
            "AbstractText": self._et(element),
            "Label": self._eav(element, "Label"),
            "NlmCategory": self._eav(element, "NlmCategory"),
        }

        return abstract_text

    def parse_abstract(self, element):

        if element is None:
            return {}

        abstract = {
            "AbstractTexts": [{
                "AbstractText": self.parse_abstract_text(_element)
            } for _element in element.findall("AbstractText")]
        }

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

        if element is None:
            return {}

        publication_type_list = {
            "PublicationTypes": [{
                "PublicationType": self.parse_publication_type(_element)
            } for _element in element.findall("PublicationType")]
        }

        return publication_type_list

    def parse_accession_number(self, element):

        if element is None:
            return {}

        accession_number = {
            "AccessionNumber": self._et(element),
        }

        return accession_number

    def parse_accession_number_list(self, element):

        if element is None:
            return {}

        accession_number_list = {
            "AccessionNumbers": [{
                "AccessionNumber": self.parse_accession_number(_element)
            } for _element in element.findall("AccessionNumber")]
        }

        return accession_number_list

    def parse_databank(self, element):

        if element is None:
            return {}

        databank = {
            "DataBankName": self._et(element.find("DataBankName")),
            "AccessionNumberList": self.parse_accession_number_list(
                element.find("AccessionNumberList")
            ),
        }

        return databank

    def parse_databank_list(self, element):

        if element is None:
            return {}

        databank_list = {
            "CompleteYN": self._eav(element, "CompleteYN"),
            "DataBanks": [{
                "DataBank": self.parse_databank(_element)
            } for _element in element.findall("DataBank")]
        }

        databank_list["IsComplete"] = convert_yn_boolean(
            databank_list["CompleteYN"]
        )

        return databank_list

    def parse_article(self, element):

        if element is None:
            return {}

        article = {
            "PubModel": self._eav(element, "PubModel"),
            "Article": {
                "Journal": self.parse_journal(element.find("Journal")),
                "ArticleTitle": self._et(element.find("ArticleTitle")),
                "Pagination": self.parse_pagination(element.find("Pagination")),
                "Abstract": self.parse_abstract(element.find("Abstract")),
                "AuthorList": self.parse_author_list(
                    element.find("AuthorList")),
                "Language": self._et(element.find("Language")),
                "DataBankList": self.parse_databank_list(
                    element.find("DataBankList")
                ),
                "PublicationTypeList": self.parse_publication_type_list(
                    element.find("PublicationTypeList")
                ),
                "ArticleDate": parse_date_element(element.find("ArticleDate"))
            }
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

        if element is None:
            return {}

        article_id_list = {
            "ArticleIds": [{
                "ArticleId": self.parse_article_id(_element)
            } for _element in element.findall("ArticleId")]
        }

        return article_id_list

    def parse_pubmed_data(self, element):

        if element is None:
            return {}

        pubmed_data = {
            # The `<History>` element is skipped.
            # The `<PublicationStatus>` element is skipped.
            "ArticleIdList": self.parse_article_id_list(
                element.find("ArticleIdList")
            )
        }

        return pubmed_data

    def parse_pubmed_article(self, element):

        if element is None:
            return {}

        pubmed_article = {
            "MedlineCitation": self.parse_medline_citation(
                element.find("MedlineCitation")
            ),
            "PubmedData": self.parse_pubmed_data(
                element.find("PubmedData")
            )
        }

        return pubmed_article

    def parse(self, filename_xml):

        msg_fmt = "Parsing Pubmed XML file '{0}'".format(filename_xml)
        self.logger.info(msg=msg_fmt)

        file_xml = self.open_xml_file(filename_xml=filename_xml)

        elements = self.generate_xml_elements(
            file_xml=file_xml,
            element_tag="PubmedArticle"
        )

        for element in elements:
            pubmed_article = self.parse_pubmed_article(element)

            yield pubmed_article
