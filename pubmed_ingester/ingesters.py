# -*- coding: utf-8 -*-

import abc
from typing import List, Dict

from pubmed_ingester.loggers import create_logger
from fform.dals_pubmed import DalPubmed
from fform.orm_pubmed import Author
from fform.orm_pubmed import ArticleIdentifierType
from fform.orm_pubmed import AbstractText
from fform.orm_pubmed import AbstractTextCategory
from fform.orm_pubmed import Affiliation
from fform.orm_pubmed import ArticlePubModel
from fform.orm_pubmed import PmKeyword
from fform.orm_pubmed import Journal
from fform.orm_pubmed import JournalIssnType
from fform.orm_pubmed import Article
from fform.orm_pubmed import Databank
from fform.orm_pubmed import AccessionNumber
from fform.orm_pubmed import Grant
from fform.orm_mt import Descriptor
from fform.orm_mt import Qualifier
from pubmed_ingester.utils import log_ingestion_of_document
from pubmed_ingester.utils import log_ingestion_of_documents


class IngesterDocumentBase(object):
    def __init__(self, dal, **kwargs):

        self.dal = dal

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

    @abc.abstractmethod
    def ingest(
        self,
        document: Dict
    ):
        raise NotImplementedError


class IngesterDocumentPubmedArticle(IngesterDocumentBase):
    def __init__(
        self,
        dal: DalPubmed,
        **kwargs
    ):

        super(IngesterDocumentPubmedArticle, self).__init__(
            dal=dal,
            kwargs=kwargs
        )

    @staticmethod
    def _convert_enum_value(value: str):
        """Converts enumeration values to a form compatible with PostgreSQL by
        converting them to lowercase and replacing dashes with underscores.

        Args:
            value (str): The enumeration value to be converted.

        Returns:
            str: The converted value.
        """

        if value:
            value = value.replace("-", "_").lower()
        else:
            value = None

        return value

    def retrieve_chemicals(
        self,
        documents: List[Dict]
    ) -> List[int]:

        descriptor_obj_ids = []
        for document in documents:
            ui = document["Chemical"]["NameOfSubstance"]["UI"]
            descriptor = self.dal.get_by_attr(
                orm_class=Descriptor,
                attr_name="ui",
                attr_value=ui,
            )  # type: Descriptor

            if descriptor:
                descriptor_obj_ids.append(descriptor.descriptor_id)

        return descriptor_obj_ids

    @log_ingestion_of_document(document_name="JournalInfo")
    def ingest_journal_info(
        self,
        document: Dict
    ) -> int:

        journal_info_id = self.dal.iodi_journal_info(
            nlmid=document["NlmUniqueID"],
            issn=document["ISSNLinking"],
            country=document["Country"],
            abbreviation=document["MedlineTA"],
        )

        return journal_info_id

    @log_ingestion_of_document(document_name="Journal")
    def ingest_journal(
        self,
        document: Dict
    ) -> int:

        journal_obj = Journal()
        journal_obj.issn = document["ISSN"]["ISSN"]
        journal_obj.issn_type = JournalIssnType.get_member(
            value=self._convert_enum_value(document["ISSN"]["IssnType"]),
        )
        journal_obj.title = document["Title"]
        journal_obj.abbreviation = document["ISOAbbreviation"]

        journal_id = self.dal.iodi_journal(
            issn=journal_obj.issn,
            issn_type=journal_obj.issn_type,
            title=journal_obj.title,
            abbreviation=journal_obj.abbreviation,
            md5=journal_obj.md5
        )

        return journal_id

    @log_ingestion_of_documents(document_name="AbstractText")
    def ingest_abstract_texts(
        self,
        documents: List[Dict]
    ) -> List[int]:

        labels = []
        categories = []
        texts = []
        md5s = []

        for entry in documents:
            data = entry["AbstractText"]

            # Skip empty abstract entries.
            if not data:
                continue

            abstract_text = AbstractText()
            abstract_text.label = data["Label"]
            abstract_text.category = AbstractTextCategory.get_member(
                value=self._convert_enum_value(data["NlmCategory"]),
            )
            abstract_text.text = data["AbstractText"]

            labels.append(abstract_text.label)
            categories.append(abstract_text.category)
            texts.append(abstract_text.text)
            md5s.append(abstract_text.md5)

        abstract_text_obj_ids = self.dal.biodi_abstract_texts(
            labels=labels,
            categories=categories,
            texts=texts,
            md5s=md5s
        )

        return abstract_text_obj_ids

    @log_ingestion_of_documents(document_name="ArticleId")
    def ingest_article_ids(
        self,
        citation_id: int,
        documents: Dict,
    ):

        identifier_types = []
        identifiers = []

        for entry in documents:
            data = entry["ArticleId"]

            identifier_types.append(ArticleIdentifierType.get_member(
                value=self._convert_enum_value(data["IdType"]),
            ))
            identifiers.append(data["ArticleId"])

        self.dal.biodi_citation_identifiers(
            citation_id=citation_id,
            identifier_types=identifier_types,
            identifiers=identifiers
        )

    @log_ingestion_of_documents(document_name="PublicationType")
    def ingest_publication_types(
        self,
        documents: List[Dict]
    ) -> List[int]:

        uids = []
        publication_types = []
        for document in documents:
            doc = document["PublicationType"]

            uids.append(doc["UI"])
            publication_types.append(doc["PublicationType"])

        publication_type_obj_ids = self.dal.biodi_publication_types(
            uids=uids,
            publication_types=publication_types
        )

        return publication_type_obj_ids

    @log_ingestion_of_document(document_name="Article")
    def ingest_article(
        self,
        journal_id: int,
        document: Dict,
    ) -> int:

        doc_article = document["Article"]
        doc_journal = doc_article["Journal"]
        doc_journal_issue = doc_journal["JournalIssue"]["JournalIssue"]

        publication_year = (
            doc_article["ArticleDate"]["Year"] or
            doc_journal_issue["PubDate"]["Year"]
        )

        publication_month = (
            doc_article["ArticleDate"]["Month"] or
            doc_journal_issue["PubDate"]["Month"]
        )

        publication_day = (
            doc_article["ArticleDate"]["Day"] or
            doc_journal_issue["PubDate"]["Day"]
        )

        date_published = (
            doc_article["ArticleDate"]["Date"] or
            doc_journal_issue["PubDate"]["Date"]
        )

        if "Pagination" in doc_article:
            medlinepgn = doc_article["Pagination"].get("MedlinePgn")
        else:
            medlinepgn = None

        article_obj = Article()
        article_obj.publication_year = publication_year
        article_obj.publication_month = publication_month
        article_obj.publication_day = publication_day
        article_obj.date_published = date_published
        article_obj.publication_model = ArticlePubModel.get_member(
            value=self._convert_enum_value(document["PubModel"]),
        )
        article_obj.journal_id = journal_id
        article_obj.journal_volume = doc_journal_issue.get("Volume")
        article_obj.journal_issue = doc_journal_issue.get("Issue")
        article_obj.title = doc_article["ArticleTitle"]
        article_obj.pagination = medlinepgn
        article_obj.language = doc_article.get("Language")
        article_obj.title_vernacular = doc_article.get("VernacularTitle")

        article_id = self.dal.iodi_article(
            publication_year=article_obj.publication_year,
            publication_month=article_obj.publication_month,
            publication_day=article_obj.publication_day,
            date_published=article_obj.date_published,
            publication_model=article_obj.publication_model,
            journal_id=article_obj.journal_id,
            journal_volume=article_obj.journal_volume,
            journal_issue=article_obj.journal_issue,
            title=article_obj.title,
            pagination=article_obj.pagination,
            language=article_obj.language,
            title_vernacular=article_obj.title_vernacular,
            md5=article_obj.md5
        )

        return article_id

    def retrieve_descriptors(
        self,
        documents: List[Dict]
    ) -> List[int]:

        descriptor_obj_ids = []
        for document in documents:
            ui = document["UI"]
            descriptor = self.dal.get_by_attr(
                orm_class=Descriptor,
                attr_name="ui",
                attr_value=ui,
            )  # type: Descriptor

            if descriptor:
                descriptor_obj_ids.append(descriptor.descriptor_id)

        return descriptor_obj_ids

    def retrieve_qualifiers(
        self,
        documents: List[Dict]
    ) -> List[int]:

        qualifier_obj_ids = []
        for document in documents:
            ui = document["QualifierName"]["UI"]
            qualifier = self.dal.get_by_attr(
                orm_class=Qualifier,
                attr_name="ui",
                attr_value=ui,
            )  # type: Qualifier

            if qualifier:
                qualifier_obj_ids.append(qualifier.qualifier_id)

        return qualifier_obj_ids

    @log_ingestion_of_documents(document_name="Keyword")
    def ingest_keywords(
        self,
        documents: Dict,
    ) -> List[int]:

        keywords = []
        md5s = []

        for document in documents:

            keyword = PmKeyword()
            keyword.keyword = document["Keyword"]["Keyword"]

            keywords.append(keyword.keyword)
            md5s.append(keyword.md5)

        keyword_obj_ids = self.dal.biodi_keywords(
            keywords=keywords,
            md5s=md5s
        )

        return keyword_obj_ids

    @log_ingestion_of_document(document_name="MedlineCitation")
    def ingest_citation(
        self,
        article_id: int,
        journal_info_id: int,
        document: Dict
    ) -> int:

        pmid = int(document["PMID"]["PMID"])
        citation_id = self.dal.iodi_citation(
            pmid=pmid,
            date_created=document["DateCreated"]["Date"],
            date_completion=document["DateCompleted"]["Date"],
            date_revision=document["DateRevised"]["Date"],
            article_id=article_id,
            journal_info_id=journal_info_id,
            num_references=document.get("NumberOfReferences")
        )

        return citation_id

    @log_ingestion_of_documents(document_name="MeshHeading")
    def ingest_mesh_headings(
        self,
        citation_id: int,
        documents: List[Dict]
    ):

        documents_descriptors = []
        documents_qualifiers = []
        for document in documents:
            data = document["MeshHeading"]
            document_descriptor = data.get("DescriptorName")
            if document_descriptor:
                documents_descriptors.append(document_descriptor)
            for document_qualifier in data["QualifierNames"]:
                documents_qualifiers.append(document_qualifier)

        _descriptor_ids = self.retrieve_descriptors(
            documents=documents_descriptors
        )

        if not _descriptor_ids:
            return None

        if documents_qualifiers:
            _qualifier_ids = self.retrieve_qualifiers(
                documents=documents_qualifiers
            )
        else:
            _qualifier_ids = []

        descriptor_ids = []
        are_descriptors_major = []
        qualifier_ids = []
        are_qualifiers_major = []
        idx_qualifier = 0
        for idx_descriptor, document in enumerate(documents):

            if not _descriptor_ids[idx_descriptor]:
                continue

            data = document["MeshHeading"]
            document_descriptor = data.get("DescriptorName")

            if not data["QualifierNames"]:
                descriptor_ids.append(_descriptor_ids[idx_descriptor])
                are_descriptors_major.append(
                    document_descriptor["IsMajorTopic"]
                )
                qualifier_ids.append(None)
                are_qualifiers_major.append(None)
                continue

            for document_qualifier in data["QualifierNames"]:
                doc = document_qualifier["QualifierName"]
                descriptor_ids.append(_descriptor_ids[idx_descriptor])
                are_descriptors_major.append(
                    document_descriptor["IsMajorTopic"]
                )
                qualifier_ids.append(_qualifier_ids[idx_qualifier])
                idx_qualifier += 1
                are_qualifiers_major.append(doc["IsMajorTopic"])

        self.dal.biodi_citation_descriptors_qualifiers(
            citation_id=citation_id,
            descriptor_ids=descriptor_ids,
            are_descriptors_major=are_descriptors_major,
            qualifier_ids=qualifier_ids,
            are_qualifiers_major=are_qualifiers_major
        )

    @log_ingestion_of_documents(document_name="DataBank")
    def ingest_databanks(
        self,
        article_id: int,
        documents: List[Dict]
    ):

        # Iterate over the documents, add the `Databank` records and retrieve
        # their IDs.
        databanks = []
        databank_md5s = []
        for document in documents:
            databank_obj = Databank()
            databank_obj.databank = document["DataBank"]["DataBankName"]

            databanks.append(databank_obj.databank)
            databank_md5s.append(databank_obj.md5)

        databank_ids = self.dal.biodi_databanks(
            databanks=databanks,
            md5s=databank_md5s
        )

        for databank_id, document in zip(databank_ids, documents):
            data = document["DataBank"]
            _docs = data["AccessionNumberList"]["AccessionNumbers"]

            accession_numbers = []
            accession_number_md5s = []
            for _doc in _docs:
                accession_number_obj = AccessionNumber()
                _num = _doc["AccessionNumber"]["AccessionNumber"]
                accession_number_obj.accession_number = _num

                accession_numbers.append(accession_number_obj.accession_number)
                accession_number_md5s.append(accession_number_obj.md5)

            accession_number_ids = self.dal.biodi_accession_numbers(
                accession_numbers=accession_numbers,
                md5s=accession_number_md5s
            )

            self.dal.biodi_article_databank_accession_numbers(
                article_id=article_id,
                databank_id=databank_id,
                accession_number_ids=accession_number_ids
            )

    @log_ingestion_of_documents(document_name="Author")
    def ingest_authors(
        self,
        documents: List[Dict]
    ) -> List[int]:

        author_identifiers = []
        author_identifier_sources = []
        names_first = []
        names_last = []
        names_initials = []
        names_suffix = []
        emails = []
        md5s = []
        for entry in documents:
            # Skip invalid author documents.
            if not entry["Author"]["IsValid"]:
                continue

            data = entry["Author"]["Author"]

            author_obj = Author()
            author_obj.author_identifier = data["Identifier"]["Identifier"]
            author_obj.author_identifier_source = data["Identifier"]["Source"]
            author_obj.name_first = data["ForeName"]
            author_obj.name_last = data["LastName"]
            author_obj.name_initials = data["Initials"]
            author_obj.name_initials = data["Initials"]
            author_obj.name_suffix = data["Suffix"]
            author_obj.email = data["Email"]

            author_identifiers.append(author_obj.author_identifier)
            author_identifier_sources.append(
                author_obj.author_identifier_source
            )
            names_first.append(author_obj.name_first)
            names_last.append(author_obj.name_last)
            names_initials.append(author_obj.name_initials)
            names_suffix.append(author_obj.name_suffix)
            emails.append(author_obj.email)
            md5s.append(author_obj.md5)

        author_obj_ids = self.dal.biodi_authors(
            author_identifiers=author_identifiers,
            author_identifier_sources=author_identifier_sources,
            names_first=names_first,
            names_last=names_last,
            names_initials=names_initials,
            names_suffix=names_suffix,
            emails=emails,
            md5s=md5s,
        )

        return author_obj_ids

    @log_ingestion_of_document(document_name="AffiliationInfo")
    def ingest_author_affiliations(
        self,
        document: Dict,
    ) -> List[int]:

        affiliation_identifiers = []
        affiliation_identifier_sources = []
        affiliations = []
        affiliation_canonical_ids = []
        md5s = []

        doc_ident = document["Identifier"]
        for entry in document["Affiliations"]:
            affiliation = Affiliation()
            affiliation.affiliation_identifier = doc_ident["Identifier"]
            affiliation.affiliation_identifier_source = doc_ident["Source"]
            affiliation.affiliation = entry["Affiliation"]

            affiliation_identifiers.append(affiliation.affiliation_identifier)
            affiliation_identifier_sources.append(
                affiliation.affiliation_identifier_source
            )
            affiliations.append(affiliation.affiliation)
            affiliation_canonical_ids.append(None)
            md5s.append(affiliation.md5)

        affiliation_obj_ids = self.dal.biodi_affiliations(
            affiliation_identifiers=affiliation_identifiers,
            affiliation_identifier_sources=affiliation_identifier_sources,
            affiliations=affiliations,
            affiliation_canonical_ids=affiliation_canonical_ids,
            md5s=md5s
        )

        return affiliation_obj_ids

    @log_ingestion_of_document(document_name="Author")
    def ingest_article_author_affiliations(
        self,
        article_id,
        author_ids: List[int],
        documents: List[Dict]
    ):

        _author_ids = []
        _affiliation_ids = []
        _ordinances = []
        _affiliation_canonical_ids = []
        for ordinance, (author_id, document) in enumerate(
            zip(author_ids, documents)
        ):
            doc = document["Author"]["Author"]

            # Get the `AffiliationInfo` document and (if it exists) add the
            # affiliations for this author.
            document_affiliation_info = doc.get("AffiliationInfo")
            if document_affiliation_info:
                affiliation_ids = self.ingest_author_affiliations(
                    document=document_affiliation_info
                )
            else:
                affiliation_ids = [None]

            for _affiliation_id in affiliation_ids:
                _author_ids.append(author_id)
                _affiliation_ids.append(_affiliation_id)
                _ordinances.append(ordinance + 1)
                _affiliation_canonical_ids.append(None)

        self.dal.biodi_article_author_affiliations(
            article_id=article_id,
            author_ids=_author_ids,
            affiliation_ids=_affiliation_ids,
            affiliation_canonical_ids=_affiliation_canonical_ids,
            ordinances=_ordinances,
        )

    @log_ingestion_of_documents(document_name="Grant")
    def ingest_grants(
        self,
        documents: Dict,
    ) -> List[int]:

        uids = []
        acronyms = []
        agencies = []
        countries = []
        md5s = []
        for document in documents:
            doc = document["Grant"]

            grant_obj = Grant()
            grant_obj.uid = doc["GrantID"]
            grant_obj.acronym = doc["Acronym"]
            grant_obj.agency = doc["Agency"]
            grant_obj.country = doc["Country"]

            uids.append(grant_obj.uid)
            acronyms.append(grant_obj.acronym)
            agencies.append(grant_obj.agency)
            countries.append(grant_obj.country)
            md5s.append(grant_obj.md5)

        grant_ids = self.dal.biodi_grants(
            uids=uids,
            acronyms=acronyms,
            agencies=agencies,
            countries=countries,
            md5s=md5s,
        )

        return grant_ids

    @log_ingestion_of_document(document_name="PubmedArticle")
    def ingest(
        self,
        document: Dict
    ):
        # Retrieve shortcuts into the document.
        pubmed_article = document
        medline_citation = pubmed_article["MedlineCitation"]
        pubmed_data = pubmed_article["PubmedData"]
        article = medline_citation["Article"]
        journal = article["Article"]["Journal"]
        # Get the `AbstractText` documents (if available).
        if article["Article"].get("Abstract"):
            abstract_text_documents = article["Article"]["Abstract"].get(
                "AbstractTexts"
            )
        else:
            abstract_text_documents = None
        # Get the `AuthorList` document and the `Author` documents (if
        # available).
        author_list = article["Article"].get("AuthorList")
        if author_list:
            author_documents = author_list.get("Authors")
        else:
            author_documents = None
        # Get the `ChemicalList` document and the `Chemical`
        # documents (if available).
        chemical_list = medline_citation["ChemicalList"]
        chemical_documents = chemical_list.get("Chemicals")
        # Get the `PublicationTypeList` document and the `PublicationType`
        # documents (if available).
        publication_type_list = article["Article"]["PublicationTypeList"]
        publication_type_documents = publication_type_list.get(
            "PublicationTypes"
        )
        # Get the `GrantList` document and the `Grant` documents (if available).
        grant_list = article["Article"].get("GrantList")
        if grant_list:
            grant_documents = grant_list.get("Grants")
        else:
            grant_documents = None
        # Get the `KeywordList` document and the `Keywords` documents (if
        # available).
        keyword_list = medline_citation["KeywordList"]
        keyword_documents = keyword_list.get("Keywords")
        # Get the `ArticleIdList` document and the `ArticleIds` documents (if
        # available).
        article_id_list = pubmed_data["ArticleIdList"]
        article_id_documents = article_id_list.get("ArticleIds")
        # Get the `MeshHeadingList` document and the `MeshHeadings` documents
        # (if available).
        mesh_heading_list = medline_citation["MeshHeadingList"]
        mesh_heading_documents = mesh_heading_list.get("MeshHeadings")
        # Get the `DataBankList` document and the `DataBanks` documents
        # (if available).
        databank_list = article["Article"].get("DataBankList")
        if databank_list:
            databank_documents = databank_list.get("DataBanks")
        else:
            databank_documents = None

        # Skip documents where the `MedlineCitation` version of the `PMID` is
        # not `1` to ensure unique records.
        if medline_citation["PMID"]["Version"] != "1":
            return None

        # Ingest the `MedlineJournalInfo` document.
        journal_info_id = self.ingest_journal_info(
            document=medline_citation["MedlineJournalInfo"]
        )

        # Ingest the `Journal` document.
        journal_id = self.ingest_journal(document=journal)

        # Find and ingest the `Article` document.
        article_id = self.ingest_article(
            journal_id=journal_id,
            document=article
        )

        # Ingest the `MedlineCitation` document.
        citation_id = self.ingest_citation(
            article_id=article_id,
            journal_info_id=journal_info_id,
            document=medline_citation
        )

        # Ingest the `AbstractText` documents.
        if abstract_text_documents:
            abstract_text_ids = self.ingest_abstract_texts(
                documents=abstract_text_documents
            )

            self.dal.biodi_article_abstract_texts(
                article_id=article_id,
                abstract_text_ids=abstract_text_ids,
                ordinances=list(range(1, len(abstract_text_documents) + 1))
            )

        # Ingest `Chemical` documents.
        if chemical_documents:
            chemical_ids = self.retrieve_chemicals(documents=chemical_documents)

            if chemical_ids:
                self.dal.biodi_citation_chemicals(
                    citation_id=citation_id,
                    chemical_ids=chemical_ids
                )

        # Ingest `Author` documents.
        if author_documents:
            author_ids = self.ingest_authors(documents=author_documents)

            self.ingest_article_author_affiliations(
                article_id=article_id,
                author_ids=author_ids,
                documents=author_documents
            )

        # Ingest `PublicationType` documents.
        if publication_type_documents:
            publication_type_ids = self.ingest_publication_types(
                documents=publication_type_documents,
            )

            self.dal.biodi_article_publication_types(
                article_id=article_id,
                publication_type_ids=publication_type_ids,
            )

        # Ingest `Keyword` documents.
        if keyword_documents:
            keyword_ids = self.ingest_keywords(documents=keyword_documents)

            self.dal.biodi_citation_keywords(
                citation_id=citation_id,
                keyword_ids=keyword_ids
            )

        # Ingest `Grant` documents.
        if grant_documents:
            grant_ids = self.ingest_grants(documents=grant_documents)

            self.dal.biodi_article_grants(
                article_id=article_id,
                grant_ids=grant_ids
            )

        if article_id_documents:
            self.ingest_article_ids(
                citation_id=citation_id,
                documents=article_id_documents
            )

        if mesh_heading_documents:
            self.ingest_mesh_headings(
                citation_id=citation_id,
                documents=mesh_heading_documents
            )

        if databank_documents:
            self.ingest_databanks(
                article_id=article_id,
                documents=databank_documents
            )

        return citation_id
