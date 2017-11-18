# -*- coding: utf-8 -*-

from sqlalchemy.dialects.postgresql import insert

import datetime
from typing import List

from .loggers import create_logger
from .dal_base import DalBase
from .dal_base import with_session_scope
from .orm import Chemical
from .orm import Author
from .orm import Affiliation
from .orm import Keyword
from .orm import Descriptor
from .orm import Qualifier
from .orm import PublicationType
from .orm import Journal
from .orm import JournalInfo
from .orm import Grant
from .orm import Databank
from .orm import AccessionNumber
from .orm import ArticleAbstractText
from .orm import ArticleAuthorAffiliation
from .orm import ArticleDatabankAccessionNumber
from .orm import ArticleGrant
from .orm import CitationChemical
from .orm import CitationDescriptorQualifier
from .orm import CitationIdentifier
from .orm import CitationKeyword
from .orm import ArticleIdentifierType
from .orm import ArticlePublicationType
from .orm import AbstractText
from .orm import AbstractTextCategory
from .orm import ArticlePubModel
from .orm import Article
from .orm import Citation
from .utils import lists_equal_length


class DalPubmed(DalBase):
    def __init__(
        self,
        sql_username,
        sql_password,
        sql_host,
        sql_port,
        sql_db,
        *args,
        **kwargs
    ):

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

        super(DalPubmed, self).__init__(
            sql_username=sql_username,
            sql_password=sql_password,
            sql_host=sql_host,
            sql_port=sql_port,
            sql_db=sql_db,
            *args,
            **kwargs
        )

    @with_session_scope()
    def bget_chemicals(
        self,
        uids: List[str],
        session=None
    ) -> List[Chemical]:

        query = session.query(Chemical)
        query = query.filter(Chemical.uid.in_(uids))

        chemical_objs = query.all()

        return chemical_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_chemicals(
        self,
        nums_registries: List[str],
        uids: List[str],
        chemicals: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            Chemical,
            values=list(
                {
                    "num_registry": num_registry,
                    "uid": uid,
                    "chemical": chemical,
                } for num_registry, uid, chemical in zip(
                    nums_registries,
                    uids,
                    chemicals
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        chemical_objs = self.bget_chemicals(uids=uids, session=session)

        chemical_obj_ids = []
        for uid in uids:
            for chemical_obj in chemical_objs:
                if uid == chemical_obj.uid:
                    chemical_obj_ids.append(chemical_obj.chemical_id)

        return chemical_obj_ids

    @with_session_scope()
    def bget_descriptors(
        self,
        uids: List[str],
        session=None
    ) -> List[Descriptor]:

        query = session.query(Descriptor)
        query = query.filter(Descriptor.uid.in_(uids))

        descriptor_objs = query.all()

        return descriptor_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_descriptors(
        self,
        uids: List[str],
        descriptors: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            Descriptor,
            values=list(
                {
                    "uid": uid,
                    "descriptor": descriptor,
                } for uid, descriptor in zip(
                    uids,
                    descriptors
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        descriptor_objs = self.bget_descriptors(uids=uids, session=session)

        descriptor_obj_ids = []
        for uid in uids:
            for descriptor_obj in descriptor_objs:
                if uid == descriptor_obj.uid:
                    descriptor_obj_ids.append(descriptor_obj.descriptor_id)

        return descriptor_obj_ids

    @with_session_scope()
    def bget_qualifiers(
        self,
        uids: List[str],
        session=None
    ) -> List[Qualifier]:

        query = session.query(Qualifier)
        query = query.filter(Qualifier.uid.in_(uids))

        qualifier_objs = query.all()

        return qualifier_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_qualifiers(
        self,
        uids: List[str],
        qualifiers: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            Qualifier,
            values=list(
                {
                    "uid": uid,
                    "qualifier": qualifier,
                } for uid, qualifier in zip(
                    uids,
                    qualifiers
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        qualifier_objs = self.bget_qualifiers(uids=uids, session=session)

        qualifier_obj_ids = []
        for uid in uids:
            for qualifier_obj in qualifier_objs:
                if uid == qualifier_obj.uid:
                    qualifier_obj_ids.append(qualifier_obj.qualifier_id)

        return qualifier_obj_ids

    @with_session_scope()
    def bget_keywords(self, md5s, session=None) -> List[Keyword]:

        query = session.query(Keyword)
        query = query.filter(Keyword.md5.in_(md5s))

        keyword_objs = query.all()

        return keyword_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_keywords(
        self,
        keywords: List[str],
        md5s: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            Keyword,
            values=list(
                {
                    "keyword": keyword,
                    "md5": md5,
                } for keyword, md5 in zip(
                    keywords,
                    md5s
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        keyword_objs = self.bget_keywords(md5s=md5s, session=session)

        keyword_obj_ids = []
        for md5 in md5s:
            for keyword_obj in keyword_objs:
                if md5 == keyword_obj.md5:
                    keyword_obj_ids.append(keyword_obj.keyword_id)

        return keyword_obj_ids

    @with_session_scope()
    def bget_publication_types(
        self,
        uids: List[str],
        session=None
    ) -> List[PublicationType]:

        query = session.query(PublicationType)
        query = query.filter(PublicationType.uid.in_(uids))

        publication_type_objs = query.all()

        return publication_type_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_publication_types(
        self,
        uids: List[str],
        publication_types: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            PublicationType,
            values=list(
                {
                    "uid": uid,
                    "publication_type": publication_type,
                } for uid, publication_type in zip(
                    uids,
                    publication_types
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        publication_type_objs = self.bget_publication_types(
            uids=uids,
            session=session
        )

        publication_type_obj_ids = []
        for uid in uids:
            for publication_type_obj in publication_type_objs:
                if uid == publication_type_obj.uid:
                    publication_type_obj_ids.append(
                        publication_type_obj.publication_type
                    )

        return publication_type_obj_ids

    @with_session_scope()
    def bget_authors(
        self,
        md5s: List[str],
        session=None
    ) -> List[Author]:

        query = session.query(Author)
        query = query.filter(Author.md5.in_(md5s))

        author_objs = query.all()

        return author_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_authors(
        self,
        author_identifiers: List[str],
        author_identifier_sources: List[str],
        names_first: List[str],
        names_last: List[str],
        names_initials: List[str],
        names_suffix: List[str],
        md5s: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            Author,
            values=list(
                {
                    "author_identifier": author_identifier,
                    "author_identifier_source": author_identifier_source,
                    "name_first": name_first,
                    "name_last": name_last,
                    "name_initials": name_initials,
                    "name_suffix": name_suffix,
                    "md5": md5,
                } for (
                    author_identifier,
                    author_identifier_source,
                    name_first,
                    name_last,
                    name_initials,
                    name_suffix,
                    md5,
                ) in zip(
                    author_identifiers,
                    author_identifier_sources,
                    names_first,
                    names_last,
                    names_initials,
                    names_suffix,
                    md5s
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        author_objs = self.bget_authors(md5s=md5s, session=session)

        author_obj_ids = []
        for md5 in md5s:
            for author_obj in author_objs:
                if md5 == author_obj.md5:
                    author_obj_ids.append(author_obj.author_id)

        return author_obj_ids

    @with_session_scope()
    def bget_affiliations(
        self,
        md5s: List[str],
        session=None
    ) -> List[Affiliation]:

        query = session.query(Affiliation)
        query = query.filter(Affiliation.md5.in_(md5s))

        affiliation_objs = query.all()

        return affiliation_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_affiliations(
        self,
        affiliation_identifiers: List[str],
        affiliation_identifier_sources: List[str],
        md5s: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            Affiliation,
            values=list(
                {
                    "affiliation_identifier": affiliation_identifier,
                    "affiliation_identifier_source":
                        affiliation_identifier_source,
                    "md5": md5,
                } for (
                    affiliation_identifier,
                    affiliation_identifier_source,
                    md5,
                ) in zip(
                    affiliation_identifiers,
                    affiliation_identifier_sources,
                    md5s
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        affiliation_objs = self.bget_affiliations(md5s=md5s, session=session)

        affiliation_obj_ids = []
        for md5 in md5s:
            for affiliation_obj in affiliation_objs:
                if md5 == affiliation_obj.md5:
                    affiliation_obj_ids.append(affiliation_obj.affiliation_id)

        return affiliation_obj_ids

    @with_session_scope()
    def bget_journal_infos(
        self,
        nlmids: List[str],
        session=None
    ) -> List[JournalInfo]:

        query = session.query(JournalInfo)
        query = query.filter(JournalInfo.nlmid.in_(nlmids))

        journal_info_objs = query.all()

        return journal_info_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_journal_infos(
        self,
        nlmids: List[str],
        issns: List[str],
        countries: List[str],
        abbreviations: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            JournalInfo,
            values=list(
                {
                    "nlmid": nlmid,
                    "issn": issn,
                    "country": country,
                    "abbreviation": abbreviation,
                } for (
                    nlmid,
                    issn,
                    country,
                    abbreviation,
                ) in zip(
                    nlmids,
                    issns,
                    countries,
                    abbreviations,
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        journal_info_objs = self.bget_journal_infos(
            nlmids=nlmids,
            session=session
        )

        journal_info_obj_ids = []
        for nlmid in nlmids:
            for journal_info_obj in journal_info_objs:
                if nlmid == journal_info_obj.nlmid:
                    journal_info_obj_ids.append(
                        journal_info_obj.journal_info_id
                    )

        return journal_info_obj_ids

    @with_session_scope()
    def bget_journals(
        self,
        md5s: List[str],
        session=None
    ) -> List[Journal]:

        query = session.query(Journal)
        query = query.filter(Journal.md5.in_(md5s))

        journal_objs = query.all()

        return journal_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_journals(
        self,
        issns: List[str],
        issn_types: List[str],
        titles: List[str],
        abbreviations: List[str],
        md5s: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            Journal,
            values=list(
                {
                    "issn": nlmid,
                    "issn_type": issn,
                    "title": title,
                    "abbreviation": abbreviation,
                    "md5s": md5,
                } for (
                    nlmid,
                    issn,
                    title,
                    abbreviation,
                    md5,
                ) in zip(
                    issns,
                    issn_types,
                    titles,
                    abbreviations,
                    md5s,
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        journal_objs = self.bget_journals(md5s=md5s, session=session)

        journal_obj_ids = []
        for md5 in md5s:
            for journal_obj in journal_objs:
                if md5 == journal_obj.md5:
                    journal_obj_ids.append(journal_obj.journal_id)

        return journal_obj_ids

    @with_session_scope()
    def bget_grants(
        self,
        uids: List[str],
        session=None
    ) -> List[Grant]:

        query = session.query(Grant)
        query = query.filter(Grant.uid.in_(uids))

        grant_objs = query.all()

        return grant_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_grants(
        self,
        uids: List[str],
        acronyms: List[str],
        agencies: List[str],
        countries: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            Grant,
            values=list(
                {
                    "uid": uid,
                    "acronym": acronym,
                    "agency": agency,
                    "country": country,
                } for (
                    uid,
                    acronym,
                    agency,
                    country,
                ) in zip(
                    uids,
                    acronyms,
                    agencies,
                    countries,
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        grant_objs = self.bget_grants(uids=uids, session=session)

        grant_obj_ids = []
        for uid in uids:
            for grant_obj in grant_objs:
                if uid == grant_obj.uid:
                    grant_obj_ids.append(grant_obj.grant_id)

        return grant_obj_ids

    @with_session_scope()
    def bget_databanks(
        self,
        md5s: List[str],
        session=None
    ) -> List[Databank]:

        query = session.query(Databank)
        query = query.filter(Databank.md5.in_(md5s))

        databank_objs = query.all()

        return databank_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_databanks(
        self,
        databanks: List[str],
        md5s: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            Databank,
            values=list(
                {
                    "databank": databank,
                    "md5": md5,
                } for databank, md5 in zip(
                    databanks,
                    md5s
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        databank_objs = self.bget_databanks(md5s=md5s, session=session)

        databank_obj_ids = []
        for md5 in md5s:
            for databank_obj in databank_objs:
                if md5 == databank_obj.md5:
                    databank_obj_ids.append(databank_obj.databank_id)

        return databank_obj_ids

    @with_session_scope()
    def bget_accession_numbers(
        self,
        md5s: List[str],
        session=None
    ) -> List[AccessionNumber]:

        query = session.query(AccessionNumber)
        query = query.filter(AccessionNumber.md5.in_(md5s))

        accession_number_objs = query.all()

        return accession_number_objs

    @lists_equal_length
    @with_session_scope()
    def biodi_accession_numbers(
        self,
        accession_numbers: List[str],
        md5s: List[str],
        session=None
    ) -> List[int]:

        statement = insert(
            Databank,
            values=list(
                {
                    "accession_number": accession_number,
                    "md5": md5,
                } for accession_number, md5 in zip(
                    accession_numbers,
                    md5s
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

        accession_number_objs = self.bget_accession_numbers(
            md5s=md5s,
            session=session
        )

        accession_number_obj_ids = []
        for md5 in md5s:
            for accession_number_obj in accession_number_objs:
                if md5 == accession_number_obj.md5:
                    accession_number_obj_ids.append(
                        accession_number_obj.accession_number_id
                    )

        return accession_number_obj_ids

    @lists_equal_length
    @with_session_scope()
    def biodi_article_abstract_texts(
        self,
        article_id: int,
        abstract_text_ids: List[int],
        session=None
    ) -> None:

        statement = insert(
            ArticleAbstractText,
            values=list(
                {
                    "article_id": article_id,
                    "abstract_text_id": abstract_text_id,
                } for abstract_text_id in zip(abstract_text_ids)
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

    @lists_equal_length
    @with_session_scope()
    def biodi_article_author_affiliations(
        self,
        article_id: int,
        author_id: int,
        affiliation_ids: List[int],
        ordinances: List[int],
        session=None,
    ) -> None:

        statement = insert(
            ArticleAuthorAffiliation,
            values=list(
                {
                    "article_id": article_id,
                    "author_id": author_id,
                    "affiliation_id": affiliation_id,
                    "ordinance": ordinance,
                } for affiliation_id, ordinance in zip(
                    affiliation_ids,
                    ordinances
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

    @lists_equal_length
    @with_session_scope()
    def biodi_article_databank_accession_numbers(
        self,
        article_id: int,
        databank_id: int,
        accession_number_ids: List[int],
        session=None,
    ) -> None:

        statement = insert(
            ArticleDatabankAccessionNumber,
            values=list(
                {
                    "article_id": article_id,
                    "databank_id": databank_id,
                    "accession_number_id": accession_number_id,
                } for accession_number_id in zip(
                    accession_number_ids
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

    @lists_equal_length
    @with_session_scope()
    def biodi_article_grants(
        self,
        article_id: int,
        grant_ids: List[int],
        session=None,
    ) -> None:

        statement = insert(
            ArticleGrant,
            values=list(
                {
                    "article_id": article_id,
                    "grant_id": grant_id,
                } for grant_id in zip(
                    grant_ids
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

    @lists_equal_length
    @with_session_scope()
    def biodi_citation_chemicals(
        self,
        citation_id: int,
        chemical_ids: List[int],
        session=None,
    ) -> None:

        statement = insert(
            CitationChemical,
            values=list(
                {
                    "citation_id": citation_id,
                    "chemical_id": chemical_id,
                } for chemical_id in zip(
                    chemical_ids
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

    @lists_equal_length
    @with_session_scope()
    def biodi_citation_descriptors_qualifiers(
        self,
        citation_id: int,
        descriptor_ids: List[int],
        are_descriptors_major: List[bool],
        qualifier_ids: List[int],
        are_qualifiers_major: List[bool],
        session=None,
    ) -> None:

        statement = insert(
            CitationDescriptorQualifier,
            values=list(
                {
                    "citation_id": citation_id,
                    "descriptor_id": descriptor_id,
                    "is_descriptor_major": is_descriptor_major,
                    "qualifier_id": qualifier_id,
                    "is_qualifier_major": is_qualifier_major,
                } for (
                    descriptor_id,
                    is_descriptor_major,
                    qualifier_id,
                    is_qualifier_major,
                ) in zip(
                    descriptor_ids,
                    are_descriptors_major,
                    qualifier_ids,
                    are_qualifiers_major,
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

    @lists_equal_length
    @with_session_scope()
    def biodi_citation_identifiers(
        self,
        citation_id: int,
        identifier_types: List[ArticleIdentifierType],
        identifiers: List[str],
        session=None,
    ) -> None:

        statement = insert(
            CitationIdentifier,
            values=list(
                {
                    "citation_id": citation_id,
                    "identifier_type": identifier_type,
                    "identifier": identifier,
                } for (
                    identifier_type,
                    identifier
                ) in zip(
                    identifier_types,
                    identifiers
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

    @lists_equal_length
    @with_session_scope()
    def biodi_citation_keywords(
        self,
        citation_id: int,
        keyword_ids: List[int],
        session=None,
    ) -> None:

        statement = insert(
            CitationKeyword,
            values=list(
                {
                    "citation_id": citation_id,
                    "keyword_id": keyword_id,
                } for keyword_id in zip(
                    keyword_ids
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

    @lists_equal_length
    @with_session_scope()
    def biodi_article_publication_types(
        self,
        article_id: int,
        publication_type_ids: List[int],
        session=None,
    ) -> None:

        statement = insert(
            ArticlePublicationType,
            values=list(
                {
                    "article_id": article_id,
                    "publication_type_id": publication_type_id,
                } for publication_type_id in zip(
                    publication_type_ids
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

    @lists_equal_length
    @with_session_scope()
    def biodi_abstract_texts(
        self,
        labels: str,
        categories: List[AbstractTextCategory],
        texts: List[str],
        session=None,
    ) -> None:

        statement = insert(
            AbstractText,
            values=list(
                {
                    "label": label,
                    "category": category,
                    "text": text,
                } for label, category, text in zip(
                    labels,
                    categories,
                    texts
                )
            )
        ).on_conflict_do_nothing()

        session.execute(statement)

    @with_session_scope()
    def add_article(
        self,
        publication_year: int,
        publication_month: int,
        publication_day: int,
        date_published: datetime.date,
        publication_model: ArticlePubModel,
        journal_id: int,
        journal_volume: str,
        journal_issue: str,
        title: str,
        pagination: str,
        language: str,
        title_vernacular: str,
        session=None,
    ) -> int:

        article_obj = Article()
        article_obj.publication_year = publication_year
        article_obj.publication_month = publication_month
        article_obj.publication_day = publication_day
        article_obj.date_published = date_published
        article_obj.publication_model = publication_model
        article_obj.journal_id = journal_id
        article_obj.journal_volume = journal_volume
        article_obj.journal_issue = journal_issue
        article_obj.title = title
        article_obj.pagination = pagination
        article_obj.language = language
        article_obj.title_vernacular = title_vernacular

        session.add(article_obj)

        return article_obj.article_id

    @with_session_scope()
    def add_citation(
        self,
        pmid: int,
        date_created: datetime.date,
        date_completion: datetime.date,
        date_revision: datetime.date,
        article_id: int,
        journal_info_id: int,
        num_references: int,
        session=None
    ) -> int:
        citation_obj = Citation()
        citation_obj.pmid = pmid
        citation_obj.date_created = date_created
        citation_obj.date_completion = date_completion
        citation_obj.date_revision = date_revision
        citation_obj.article_id = article_id
        citation_obj.journal_info_id = journal_info_id
        citation_obj.num_references = num_references

        session.add(citation_obj)

        return citation_obj.citation_id
