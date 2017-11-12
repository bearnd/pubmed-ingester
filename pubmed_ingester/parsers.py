# -*- coding: utf-8 -*-

import abc
import gzip
from lxml import etree

import vivodict

from .loggers import create_logger
from .parser_utils import parse_date_element
from .parser_utils import convert_yn_boolean


class ParserXmlBase(object):
    def __init__(self, **kwargs):

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

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

    def parse_medline_journal_info(self, element_medline_journal_info):

        if element_medline_journal_info is None:
            return {}

        medline_journal_info = {
            "Country": self._et(
                element_medline_journal_info.find("Country")
            ),
            "MedlineTA": self._et(
                element_medline_journal_info.find("MedlineTA")
            ),
            "NlmUniqueID": self._et(
                element_medline_journal_info.find("NlmUniqueID")
            ),
            "ISSNLinking": self._et(
                element_medline_journal_info.find("ISSNLinking")
            ),
        }

        return medline_journal_info

    def parse_chemical(self, element_chemical):

        if element_chemical is None:
            return {}

        chemical = {
            "RegistryNumber": self._et(element_chemical.find("RegistryNumber")),
            "NameOfSubstance": {
                "UI": self._eav(element_chemical.find("NameOfSubstance"), "UI"),
                "NameOfSubstance": self._et(element_chemical.find(
                    "NameOfSubstance")
                ),
            },
        }

        return chemical

    def parse_chemical_list(self, element_chemical_list):

        chemicals = []

        if element_chemical_list is None:
            return chemicals

        for element_chemical in element_chemical_list.getchildren():
            chemical = self.parse_chemical(element_chemical=element_chemical)
            chemicals.append(chemical)

        return chemicals

    def parse_mesh_entry(self, element_mesh_entry, entry_name):

        mesh_entry = {}

        if element_mesh_entry is None:
            return mesh_entry

        mesh_entry = {
            entry_name: self._et(element_mesh_entry),
            "UI": self._eav(element_mesh_entry, "UI"),
            "MajorTopicYN": self._eav(element_mesh_entry, "MajorTopicYN"),
        }

        mesh_entry["IsMajorTopic"] = convert_yn_boolean(
            yn_boolean_raw=mesh_entry["MajorTopicYN"]
        )

        return mesh_entry

    def parse_mesh_descriptor(self, element_mesh_descriptor):

        mesh_descriptor = self.parse_mesh_entry(
            element_mesh_entry=element_mesh_descriptor,
            entry_name="DescriptorName"
        )

        return mesh_descriptor

    def parse_mesh_qualifier(self, element_mesh_qualifier):

        mesh_descriptor = self.parse_mesh_entry(
            element_mesh_entry=element_mesh_qualifier,
            entry_name="QualifierName"
        )

        return mesh_descriptor

    def parse_mesh_heading(self, element_mesh_heading):

        if element_mesh_heading is None:
            return {}

        mesh_heading = {
            "DescriptorName": self.parse_mesh_descriptor(
                element_mesh_heading.find("DescriptorName")
            ),
            "QualifierList": [
                self.parse_mesh_qualifier(
                    element_mesh_qualifier=qualifier for qualifier in
                    element_mesh_heading.findall("QualifierName")
                )
            ]
        }

        return mesh_heading

    def parse_mesh_heading_list(self, element_mesh_heading_list):

        mesh_headings = []

        if element_mesh_heading_list is None:
            return mesh_headings

        for element_mesh_heading in element_mesh_heading_list.getchildren():
            mesh_heading = self.parse_mesh_heading(
                element_mesh_heading=element_mesh_heading
            )
            mesh_headings.append(mesh_heading)

        return mesh_headings

    def parse_keyword(self, element_keyword):

        if element_keyword is None:
            return {}

        keyword = {
            "Keyword": self._et(element_keyword),
            "UI": self._eav(element_keyword, "UI"),
            "MajorTopicYN": self._eav(element_keyword, "MajorTopicYN"),
        }

        element_keyword["IsMajorTopic"] = convert_yn_boolean(
            yn_boolean_raw=element_keyword["MajorTopicYN"]
        )

        return keyword

    def parse_keyword_list(self, element_keyword_list):

        keywords = []

        if element_keyword_list is None:
            return keywords

        for element_keyword in element_keyword_list.getchildren():
            keyword = self.parse_keyword(element_keyword=element_keyword)
            keywords.append(keyword)

        return keywords

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
            # TODO
            "Article": None,
            "MedlineJournalInfo": self.parse_medline_journal_info(
                element_medline_journal_info=element.find("MedlineJournalInfo")
            ),
            "ChemicalList": self.parse_chemical_list(
                element_chemical_list=element.find("ChemicalList")
            ),
            # The `<CitationSubset>` element is skipped.
            "MeshHeadingList": self.parse_mesh_heading_list(
                element_mesh_heading_list=element.find("MeshHeadingList")
            ),
            "KeywordList": self.parse_keyword_list(
                element_keyword_list=element.find("KeywordList")
            )
        }

        return medline_citation

    def parse_article_id(self, element_article_id):

        if element_article_id is None:
            return {}

        keyword = {
            "ArticleId": self._et(element_article_id),
            "IdType": self._eav(element_article_id, "IdType"),
        }

        return keyword

    def parse_article_id_list(self, element_article_id_list):

        article_ids = []

        if element_article_id_list is None:
            return article_ids

        for element_article_id in element_article_id_list.getchildren():
            article_id = self.parse_keyword(element_keyword=element_article_id)
            article_ids.append(article_id)

        return article_ids

    def parse_pubmed_data(self, element):

        pubmed_data = {
            # The `<History>` element is skipped.
            # The `<PublicationStatus>` element is skipped.
            "ArticleIdList": self.parse_article_id_list(
                element_article_id_list=element.find("ArticleIdList")
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
            pubmed_article = vivodict.VivoDict.vivify({
                "citation": self.parse_medline_citation(
                    element_pubmed_article.find("MedlineCitation")
                ),
                "pubmed": self.parse_pubmed_data(
                    element_pubmed_article.find("PubmedData")
                )
            })

            yield pubmed_article
