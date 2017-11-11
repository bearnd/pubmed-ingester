# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import enum

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types
import sqlalchemy.dialects
import sqlalchemy.dialects.mysql

from .orm_base import Base, OrmBase


class AbstractTextCategory(enum.Enum):
    """Enumeration of the values of the `NlmCategory` attribute under the
    `<AbstractText>` element."""

    background = "Background"
    objective = "Objective"
    methods = "Methods"
    results = "Results"
    conclusions = "Conclusions"
    unassigned = "Unassigned"


class ArticleIdentifierType(enum.Enum):
    """Enumeration of the values of the `IdType` attribute under the
    `<ArticleId>` element."""

    doi = "doi"
    pii = "pii"
    pmcpid = "pmcpid"
    pmpid = "pmpid"
    pmc = "pmc"
    mid = "mid"
    sici = "sici"
    pubmed = "pubmed"
    medline = "medline"
    pmcid = "pmcid"


class ArticlePubModel(enum.Enum):
    """Enumeration of the values of the `PubModel` attribute under the
    `<Article>` element."""

    print = "Print"
    print_electronic = "Print-Electronic"
    electronic = "Electronic"
    electronic_print = "Electronic-Print"
    electronic_ecollection = "Electronic-eCollection"


class JournalIssnType(enum.Enum):
    """Enumeration of the values of the `IssnType` attribute under the
    `<ISSN>` element."""

    print = "Print"
    electronic = "Electronic"
    undetermined = "Undetermined"


class AbstractText(Base, OrmBase):
    """Table of `<AbstractText>` element records."""

    # set table name
    __tablename__ = "abstract_texts"

    # Autoincrementing primary key ID.
    abstract_text_id = sqlalchemy.Column(
        name="abstract_text_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Abstract text label (referring to the `Label` attribute under the
    # `<AbstractText>` element).
    label = sqlalchemy.Column(
        name="label",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Abstract text category (referring to the `NlmCategory` attribute of the
    # `<AbstractText>` element).
    category = sqlalchemy.Column(
        name="category",
        type_=sqlalchemy.types.Enum(AbstractTextCategory),
        nullable=True,
        default=AbstractTextCategory.unassigned,
        index=True
    )

    # Abstract text (value of the `<AbstractText>` element).
    text = sqlalchemy.Column(
        name="text",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class AccessionNumber(Base, OrmBase):
    """Table of `<AccessionNumber>` element records."""

    # set table name
    __tablename__ = "accession_numbers"

    # Autoincrementing primary key ID.
    accession_number_id = sqlalchemy.Column(
        name="accession_number_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Accession number value (referring to the `<AccessionNumber>` element).
    accession_number = sqlalchemy.Column(
        name="accession_number",
        type_=sqlalchemy.types.Unicode(),
        unique=True,
        nullable=False,
        index=True,
    )


class Affiliation(Base, OrmBase):
    """Table of `<Affliliation>` element records."""

    # set table name
    __tablename__ = "affiliations"

    # Autoincrementing primary key ID.
    affiliation_id = sqlalchemy.Column(
        name="affiliation_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Affiliation name (referring to the `<Affliliation>` element).
    affiliation = sqlalchemy.Column(
        name="affiliation",
        type_=sqlalchemy.types.Unicode(),
    )

    # Relationship to a list of `Author` records.
    authors = sqlalchemy.orm.relationship(
        argument="Author",
        secondary="ArticleAuthorAffiliation",
        back_populates="affiliations",
    )

    # Relationship to a list of `Author` records.
    articles = sqlalchemy.orm.relationship(
        argument="Article",
        secondary="ArticleAuthorAffiliation",
        back_populates="affiliations",
    )


class Article(Base, OrmBase):
    """Table of `<Article>` element records."""

    # set table name
    __tablename__ = "articles"

    # Autoincrementing primary key ID.
    article_id = sqlalchemy.Column(
        name="article_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Publication year (referring to the `<Year>` element).
    pub_year = sqlalchemy.Column(
        name="pub_year",
        type_=sqlalchemy.types.SmallInteger(),
        nullable=False,
        index=True,
    )

    # Publication month (referring to the `<Month>` element).
    pub_month = sqlalchemy.Column(
        name="pub_month",
        type_=sqlalchemy.types.SmallInteger(),
        nullable=True,
    )

    # Publication day (referring to the `<Day>` element).
    pub_day = sqlalchemy.Column(
        name="pub_day",
        type_=sqlalchemy.types.SmallInteger(),
        nullable=True,
    )

    # Publication date (referring to either the `<ArticleDate>` element).
    dt_published = sqlalchemy.Column(
        name="dt_published",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Article publication model (referring to the `PubModel` attribute of the
    # `<Article>` element).
    pub_model = sqlalchemy.Column(
        name="pub_model",
        type_=sqlalchemy.types.Enum(ArticlePubModel),
        nullable=True,
        default=None,
    )

    # Foreign key to the journal this article was published under.
    journal_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("journals.journal_id"),
        name="journal_id",
    )

    # Journal volume under which the article was published (referring to the
    # `<Volume>` element).
    journal_volume = sqlalchemy.Column(
        name="journal_volume",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Journal issue under which the article was published (referring to the
    # `<Issue>` element).
    journal_issue = sqlalchemy.Column(
        name="journal_issue",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Article title (referring to the `<ArticleTitle>` element).
    title = sqlalchemy.Column(
        name="title",
        type_=sqlalchemy.types.Unicode(),
        nullable=True
    )

    # Article pagination (referring to the `<Pagination>` element).
    pagination = sqlalchemy.Column(
        name="pagination",
        type_=sqlalchemy.types.Unicode(),
        nullable=True
    )

    # Article language (referring to the `<Language>` element).
    language = sqlalchemy.Column(
        name="language",
        type_=sqlalchemy.types.Unicode(length=3),
        nullable=True
    )

    # Article vernacular title (referring to the `<VernacularTitle>` element).
    title_vernacular = sqlalchemy.Column(
        name="title_vernacular",
        type_=sqlalchemy.types.Unicode(),
        nullable=True
    )

    # Relationship to a `Journal` record.
    journal = sqlalchemy.orm.relationship("Journal")

    abstract_texts = sqlalchemy.orm.relationship(
        argument="AbstractText",
        secondary="ArticleAbstractText",
    )

    # Relationship to a list of `Author` records.
    authors = sqlalchemy.orm.relationship(
        argument="Author",
        secondary="ArticleAuthorAffiliation",
        back_populates="articles",
    )

    # Relationship to a list of `ArticleDatabankAccessionNumber` records.
    databank_accession_numbers = sqlalchemy.orm.relationship(
        argument="ArticleDatabankAccessionNumber",
        back_populates="article"
    )

    # Relationship to a list of `Grant` records.
    grants = sqlalchemy.orm.relationship(
        argument="Grant",
        secondary="ArticleGrant",
        back_populates="articles"
    )

    # Relationship to a list of `PublicationType` records.
    publication_types = sqlalchemy.orm.relationship(
        argument="PublicationType",
        secondary="ArticlePublicationType",
        back_populates="articles"
    )

    # Relationship to a list of `Author` records.
    affiliations = sqlalchemy.orm.relationship(
        argument="Affiliation",
        secondary="ArticleAuthorAffiliation",
        back_populates="articles",
    )


class ArticleAbstractText(Base, OrmBase):
    """Associative table between `Article` and `AbstractText` records."""

    # set table name
    __tablename__ = "article_abstract_texts"

    # Autoincrementing primary key ID.
    article_abstract_text_id = sqlalchemy.Column(
        name="article_abstract_text_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the article ID.
    article_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("articles.article_id"),
        name="article_id",
    )

    # Foreign key to the author ID.
    abstract_text_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("abstract_texts.abstract_text_id"),
        name="abstract_text_id",
    )

    # Ordinance of the abstract text in the abstract.
    ordinance = sqlalchemy.Column(
        name="ordinance",
        type_=sqlalchemy.types.SmallInteger(),
        nullable=False,
    )


class ArticleAuthorAffiliation(Base, OrmBase):
    """Associative table between `Article`, `Author`, and `Affiliation`
     records."""

    # set table name
    __tablename__ = "article_author_affiliations"

    # Autoincrementing primary key ID.
    article_author_affiliation_id = sqlalchemy.Column(
        name="article_author_affiliation_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the article ID.
    article_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("articles.article_id"),
        name="article_id",
    )

    # Foreign key to the author ID.
    author_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("authors.author_id"),
        name="author_id",
    )

    # Foreign key to the author ID.
    affiliation_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("affiliations.affiliation_id"),
        name="affiliation_id",
    )

    # Ordinance of the author in the article.
    ordinance = sqlalchemy.Column(
        name="ordinance",
        type_=sqlalchemy.types.SmallInteger(),
        nullable=False,
    )


class ArticleDatabankAccessionNumber(Base, OrmBase):
    """Associative table between `Article`, `Databank` and `AccessionNumber`
    records."""

    # set table name
    __tablename__ = "article_databank_accession_numbers"

    # Autoincrementing primary key ID.
    article_databank_accession_number_id = sqlalchemy.Column(
        name="article_databank_accession_number_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the article ID.
    article_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("articles.article_id"),
        name="article_id",
    )

    # Foreign key to the databank ID.
    databank_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("databanks.databank_id"),
        name="databank_id",
    )

    # Foreign key to the accession number ID.
    accession_number_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("accession_numbers.accession_number_id"),
        name="accession_number_id",
    )

    article = sqlalchemy.orm.relationship(
        argument="Article",
        back_populates="databank_accession_numbers"
    )


class ArticleGrant(Base, OrmBase):
    """Associative table between `Article` and `Grant` records."""

    # set table name
    __tablename__ = "article_grants"

    # Autoincrementing primary key ID.
    article_grant_id = sqlalchemy.Column(
        name="article_grant_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the article ID.
    article_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("articles.article_id"),
        name="article_id",
    )

    # Foreign key to the grant ID.
    grant_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("grants.grant_id"),
        name="grant_id",
    )


class CitationChemical(Base, OrmBase):
    """Associative table between `Citation` and `Chemical` records."""

    # set table name
    __tablename__ = "citation_chemicals"

    # Autoincrementing primary key ID.
    citation_chemical_id = sqlalchemy.Column(
        name="citation_chemical_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the citation ID.
    citation_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("citations.citation_id"),
        name="citation_id",
    )

    # Foreign key to the chemical ID.
    chemical_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("chemicals.chemical_id"),
        name="chemical_id",
    )


class CitationDescriptorQualifier(Base, OrmBase):
    """Associative table between `Citation`, `Descriptor` and `Qualifier`
    records."""

    # set table name
    __tablename__ = "citation_descriptors_qualifiers"

    # Autoincrementing primary key ID.
    citation_descriptor_qualifier_id = sqlalchemy.Column(
        name="citation_descriptor_qualifier_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the citation ID.
    citation_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("citations.citation_id"),
        name="citation_id",
    )

    # Foreign key to the descriptor ID.
    descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("descriptors.descriptor_id"),
        name="descriptor_id",
    )

    # Whether the descriptor is major or not (referring to the `MajorTopicYN`
    # attribute of the `<DescriptorName>` element).
    is_descriptor_major = sqlalchemy.Column(
        name="is_descriptor_major",
        type_=sqlalchemy.types.Boolean(),
        nullable=False
    )

    # Foreign key to the qualifier ID and part of the composite primary key.
    qualifier_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("qualifiers.qualifier_id"),
        name="qualifier_id",
        primary_key=True,
    )

    # Whether the qualifier is major or not (referring to the `MajorTopicYN`
    # attribute of the `<QualifierName>` element).
    is_qualifier_major = sqlalchemy.Column(
        name="is_qualifier_major",
        type_=sqlalchemy.types.Boolean(),
        nullable=False
    )


class CitationIdentifier(Base, OrmBase):
    """Associative table between `Citation` and `Identifier` records."""

    # set table name
    __tablename__ = "citation_identifiers"

    # Autoincrementing primary key ID.
    citation_identifier_id = sqlalchemy.Column(
        name="citation_identifier_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the citation ID.
    citation_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("citations.citation_id"),
        name="citation_id",
    )

    # Identifier type (referring to the `IdType` attribute of the `<ArticleId>`
    # element).
    identifier_type = sqlalchemy.Column(
        name="identifier_type",
        type_=sqlalchemy.types.Enum(ArticleIdentifierType),
        nullable=False,
        index=True,
    )

    # Identifier (referring to the value of the `<ArticleId>` element).
    identifier = sqlalchemy.Column(
        name="identifier",
        type_=sqlalchemy.types.Unicode(),
    )

    # Relationship to an `Citation` records.
    citation = sqlalchemy.orm.relationship(
        argument="Citation",
        back_populates="identifiers",
    )


class CitationKeyword(Base, OrmBase):
    """Associative table between `Citation` and `Keyword` records."""

    # set table name
    __tablename__ = "citation_keywords"

    # Autoincrementing primary key ID.
    citation_keyword_id = sqlalchemy.Column(
        name="citation_keyword_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the citation ID.
    citation_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("citations.citation_id"),
        name="citation_id",
    )

    # Foreign key to the keyword ID.
    keyword_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("keywords.keyword_id"),
        name="keyword_id",
    )


class ArticlePublicationType(Base, OrmBase):
    """Associative table between `Article` and `PublicationType` records."""

    # set table name
    __tablename__ = "article_publication_types"

    # Autoincrementing primary key ID.
    article_publication_type_id = sqlalchemy.Column(
        name="article_publication_type_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the article ID.
    article_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("articles.article_id"),
        name="article_id",
    )

    # Foreign key to the publication type ID.
    publication_type_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("publication_types.publication_type_id"),
        name="publication_type_id",
    )


class Author(Base, OrmBase):
    """Table of `<Author>` element records."""

    # set table name
    __tablename__ = "authors"

    # Autoincrementing primary key ID.
    author_id = sqlalchemy.Column(
        name="author_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Author first name (referring to the `<ForeName>` element).
    name_first = sqlalchemy.Column(
        name="name_first",
        type_=sqlalchemy.types.Unicode(),
    )

    # Author last name (referring to the `<LastName>` element).
    name_last = sqlalchemy.Column(
        name="name_last",
        type_=sqlalchemy.types.Unicode(),
    )

    # Author initials (referring to the `<Initials>` element).
    name_initials = sqlalchemy.Column(
        name="name_initials",
        type_=sqlalchemy.types.Unicode(),
    )

    # Author suffix (referring to the `<Suffix>` element).
    name_suffix = sqlalchemy.Column(
        name="name_suffix",
        type_=sqlalchemy.types.Unicode(),
    )

    # Relationship to a list of `Article` records.
    articles = sqlalchemy.orm.relationship(
        argument="Article",
        secondary="ArticleAuthorAffiliation",
        back_populates="authors"
    )

    # Relationship to a list of `Affiliation` records.
    affiliations = sqlalchemy.orm.relationship(
        argument="Affiliation",
        secondary="ArticleAuthorAffiliation",
        back_populates="authors"
    )


class Chemical(Base, OrmBase):
    """Table of `<Chemical>` element records."""

    # set table name
    __tablename__ = "chemicals"

    # Autoincrementing primary key ID.
    chemical_id = sqlalchemy.Column(
        name="chemical_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Chemical registry number (referring to the `<RegistryNumber>` element).
    num_registry = sqlalchemy.Column(
        name="num_registry",
        type_=sqlalchemy.types.Unicode(length=9),
        index=True,
    )

    # Publication type UID (referring to the `UI` attribute of the
    # `<NameOfSubstance>` element).
    uid = sqlalchemy.Column(
        name="uid",
        type_=sqlalchemy.types.Unicode(length=7),
        unique=True,
        index=True,
    )

    # Publication type name (referring to the `<NameOfSubstance>` element).
    name = sqlalchemy.Column(
        name="name",
        type_=sqlalchemy.types.Unicode(),
    )

    # Relationship to a list of `Citation` records.
    articles = sqlalchemy.orm.relationship(
        argument="Citation",
        secondary="CitationChemical",
        back_populates="chemicals"
    )


class Citation(Base, OrmBase):
    """Table of `<MedlineCitation>` element records."""

    # set table name
    __tablename__ = "citations"

    # Autoincrementing primary key ID.
    citation_id = sqlalchemy.Column(
        name="citation_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Citation PMID (referring to the `<PMID>` element).
    pmid = sqlalchemy.Column(
        name="pmid",
        type_=sqlalchemy.types.Integer(),
        unique=True,
        nullable=False,
    )

    # Citation creation date (referring to either the `<DateCreated>` element).
    dt_created = sqlalchemy.Column(
        name="dt_created",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Citation completion date (referring to either the `<DateCompleted>`
    # element).
    dt_completion = sqlalchemy.Column(
        name="dt_completion",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Citation revision date (referring to the `<DateRevised>` element).
    dt_revision = sqlalchemy.Column(
        name="dt_revision",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Foreign key to the article ID.
    article_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("articles.article_id"),
        name="article_id",
    )

    # Foreign key to the journal info ID.
    journal_info_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("journal_infos.journal_info_id"),
        name="journal_info_id",

    )

    # Number of references in citation (referring to the `<NumberofReferences>`
    # element).
    num_references = sqlalchemy.Column(
        name="num_references",
        type_=sqlalchemy.types.SmallInteger(),
        nullable=True,
    )

    # Relationship to an `Article` record.
    article = sqlalchemy.orm.relationship(
        argument="Article",
    )

    # Relationship to a `JournalInfo` record.
    journal_info = sqlalchemy.orm.relationship(
        argument="JournalInfo",
    )

    # Relationship to a list of `Identifier` records.
    identifiers = sqlalchemy.orm.relationship(
        argument="CitationIdentifier",
        back_populates="citation"
    )

    # Relationship to a list of `Chemical` records.
    chemicals = sqlalchemy.orm.relationship(
        argument="Chemical",
        secondary="CitationChemical",
        back_populates="citation"
    )

    # Relationship to a list of `Keyword` records.
    keywords = sqlalchemy.orm.relationship(
        argument="Keyword",
        secondary="CitationKeyword",
        back_populates="citations"
    )


class Databank(Base, OrmBase):
    """Table of `<DataBank>` element records."""

    # set table name
    __tablename__ = "databanks"

    # Autoincrementing primary key ID.
    databank_id = sqlalchemy.Column(
        name="databank_id",
        type_=sqlalchemy.types.SmallInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Unique qualifier name (referring to the `<DataBankName>` element).
    name = sqlalchemy.Column(
        name="name",
        type_=sqlalchemy.types.Unicode(length=20),
        unique=True,
        nullable=False,
        index=True,
    )


class Descriptor(Base, OrmBase):
    """Table of `<DescriptorName>` element records."""

    # set table name
    __tablename__ = "descriptors"

    # Autoincrementing primary key ID.
    descriptor_id = sqlalchemy.Column(
        name="descriptor_id",
        type_=sqlalchemy.types.Integer(),
        primary_key=True,
        autoincrement="auto",
    )

    # Descriptor UID (referring to the `UI` attribute of the `<DescriptorName>`
    # element).
    uid = sqlalchemy.Column(
        name="uid",
        type_=sqlalchemy.types.Unicode(length=7),
        unique=True,
        index=True,
    )

    # Descriptor qualifier name (value of the `<DescriptorName>` element).
    descriptor = sqlalchemy.Column(
        name="descriptor",
        type_=sqlalchemy.types.Unicode(),
        unique=True,
        nullable=False,
        index=True,
    )


class Grant(Base, OrmBase):
    """Table of `<Grant>` element records."""

    # set table name
    __tablename__ = "grants"

    # Autoincrementing primary key ID.
    grant_id = sqlalchemy.Column(
        name="grant_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Pubmed Grant ID (referring to the `<GrantID>` element).
    uid = sqlalchemy.Column(
        name="uid",
        type_=sqlalchemy.types.Unicode(),
        unique=True,
    )

    # Grant acronym (referring to the `<Acronym>` element).
    acronym = sqlalchemy.Column(
        name="acronym",
        type_=sqlalchemy.types.Unicode(length=2),
    )

    # Grant acronym (referring to the `<Agency>` element).
    agency = sqlalchemy.Column(
        name="agency",
        type_=sqlalchemy.types.Unicode(),
    )

    # Country of granting agency (referring to the `<Country>` element).
    country = sqlalchemy.Column(
        name="country",
        type_=sqlalchemy.types.Unicode(),
    )

    # Relationship to a list of `Article` records.
    grants = sqlalchemy.orm.relationship(
        argument="Article",
        secondary="ArticleGrant",
        back_populates="grants"
    )


class Journal(Base, OrmBase):
    """Table of `<Journal>` element records."""

    # set table name
    __tablename__ = "journals"

    # Autoincrementing primary key ID.
    journal_id = sqlalchemy.Column(
        name="journal_id",
        type_=sqlalchemy.types.Integer(),
        primary_key=True,
        autoincrement="auto",
    )

    # Unique journal International Standard Serial Number (ISSN) (referring to
    # the `<ISSN>` element).
    issn = sqlalchemy.Column(
        name="issn",
        type_=sqlalchemy.types.Unicode(length=9),
        unique=True,
        nullable=False,
        index=True,
    )

    # ISSN type (referring to the `IssnType` attribute of the `<ISSN>` element).
    issn_type = sqlalchemy.Column(
        name="issn_type",
        type_=sqlalchemy.types.Enum(JournalIssnType),
        nullable=True,
        default=JournalIssnType.undetermined
    )

    # Full journal title (referring to the `<Title>` element).
    title = sqlalchemy.Column(
        name="title",
        type_=sqlalchemy.types.Unicode(),
    )

    # Journal ISO abbreviation (referring to the `<ISOAbbreviation>` element).
    abbreviation = sqlalchemy.Column(
        name="abbreviation",
        type_=sqlalchemy.types.Unicode(),
    )


class JournalInfo(Base, OrmBase):
    """Table of `<MedlineJournalInfo>` element records."""

    # set table name
    __tablename__ = "journal_infos"

    # Autoincrementing primary key ID.
    journal_info_id = sqlalchemy.Column(
        name="journal_info_id",
        type_=sqlalchemy.types.Integer(),
        primary_key=True,
        autoincrement="auto",
    )

    # Journal unique NLM ID (referring to the `<NlmUniqueID>` element).
    nlmid = sqlalchemy.Column(
        name="nlmid",
        type_=sqlalchemy.types.Unicode(length=9),
        unique=True,
        index=True
    )

    # Link to a journal ISSN (referring to the `<ISSNLinking>` element).
    issn = sqlalchemy.Column(
        name="issn",
        type_=sqlalchemy.types.Unicode(length=9),
    )

    # Country of journal publication (referring to the `<Country>` element).
    country = sqlalchemy.Column(
        name="country",
        type_=sqlalchemy.types.Unicode(),
    )

    # Journal abbreviation (referring to the `<MedlineTA>` element).
    abbreviation = sqlalchemy.Column(
        name="abbreviation",
        type_=sqlalchemy.types.Unicode(),
    )


class Keyword(Base, OrmBase):
    """Table of `<Keyword>` element records."""

    # set table name
    __tablename__ = "keywords"

    # Autoincrementing primary key ID.
    keyword_id = sqlalchemy.Column(
        name="keyword_id",
        type_=sqlalchemy.types.Integer(),
        primary_key=True,
        autoincrement="auto",
    )

    # Keyword name (value of the `<Keyword>` element).
    keyword = sqlalchemy.Column(
        name="keyword",
        type_=sqlalchemy.types.Unicode(),
        unique=True,
        nullable=False,
        index=True,
    )

    # Relationship to a list of `Citation` records.
    citations = sqlalchemy.orm.relationship(
        argument="Citation",
        secondary="CitationKeyword",
        back_populates="keywords",
    )


class PublicationType(Base, OrmBase):
    """Table of `<PublicationType>` element records."""

    # set table name
    __tablename__ = "publication_types"

    # Autoincrementing primary key ID.
    publication_type_id = sqlalchemy.Column(
        name="publication_type_id",
        type_=sqlalchemy.types.SmallInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Publication type UID (referring to the `UI` attribute of the
    # `<PublicationType>` element).
    uid = sqlalchemy.Column(
        name="uid",
        type_=sqlalchemy.types.Unicode(length=7),
        unique=True,
        index=True,
    )

    # Publication type name (referring to the `<PublicationType>` element).
    name = sqlalchemy.Column(
        name="name",
        type_=sqlalchemy.types.Unicode(length=9),
    )

    # Relationship to a list of `Article` records.
    articles = sqlalchemy.orm.relationship(
        argument="Article",
        secondary="ArticlePublicationType",
        back_populates="publication_types"
    )


class Qualifier(Base, OrmBase):
    """Table of `<Qualifier>` element records."""

    # set table name
    __tablename__ = "qualifiers"

    # Autoincrementing primary key ID.
    qualifier_id = sqlalchemy.Column(
        name="qualifier_id",
        type_=sqlalchemy.types.Integer(),
        primary_key=True,
        autoincrement="auto",
    )

    # Qualifier UID (referring to the `UI` attribute of the `<QualifierName>`
    # element).
    uid = sqlalchemy.Column(
        name="uid",
        type_=sqlalchemy.types.Unicode(length=7),
        unique=True,
        index=True,
    )

    # Unique qualifier name (value of the `<QualifierName>` element).
    qualifier = sqlalchemy.Column(
        name="qualifier",
        type_=sqlalchemy.types.Unicode(),
        unique=True,
        nullable=False,
        index=True,
    )
