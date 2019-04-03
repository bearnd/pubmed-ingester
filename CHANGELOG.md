## Changelog

### v0.6.1

- Fixed bug in the `parse_grant` method where null values actually had a string value of `NULL` causing errors with the DB field as the acronym is supposed to have a maximum length of 2.

### v0.6.0

Issue No. 202:

- Added the other schemata in the PG configuration to allow for the entire ORM to be reflected in the DB.
- Updated the `Makefile` to use `unittest` instead of `pytest`.
- Added Pubmed article assets for unit-testing.
- Added new integration tests against the newly added assets.
- Ported the parser unit-tests from pytest to unittest.
- Fixed issue in the different method of the `IngesterDocumentPubmedArticle` class as outdated method of enumeration-member retrieval were being used.
- Renamed the `ingest_chemicals` method of the `IngesterDocumentPubmedArticle` to `retrieve_chemicals` as the MeSH descriptors representing chemicals are no longer stored but rather retrieved from the `mesh.descriptors` table. This method is now used to retrieve the PK IDs and use those in the `biodi_citation_chemicals` method.
- Updated the `ingest_author_affiliations` and `ingest_article_author_affiliations` methods of the `IngesterDocumentPubmedArticle` class to store NULL values under the `affiliation_canonical_id` columns.
- Renamed the `ingest_descriptors` and `ingest_qualifiers` methods of the `IngesterDocumentPubmedArticle` to `retrieve_descriptors` and `retrieve_qualifiers` as the MeSH descriptors and qualifiers are no longer stored but rather retrieved from the `mesh.descriptors` table. These methods are now used to retrieve the PK IDs and use those in the `ingest_mesh_headings` method.
- Added a script to render an ingestion script for the baseline files.

### v0.5.1

- Updated the `IngesterDocumentPubmedArticle` class to convert enumeration values to their PostgreSQL-compatible format prior to retrieving the enum member.

### v0.5.0

- Added a script to copy canonical affiliation IDs to the `article_author_affiliations` table.

### v0.4.0

- Moved the `find_affiliation_google_place` function to the `utils.py` module.
- Added a new `get_place_details` function to the `retrievers.py` module.
- Added a new script to populate the canonical affiliation details.

### v0.3.0

- Refactored Ansible role to match the roles used in other projects, i.e., using Ansible Vault, provisioning PostgreSQL schemata and extensions.
- Ported code to work with `fightfor-orm` instead of defining its own ORM and Alembic revision system.
- Added basic unit-tests.
- Added code to retrieve and populate canonical affiliations.

### v0.2.1

- Removed the obsolete alembic migration for the old initial schema.
- Added a script to ingest a single Pubmed XML file.

### v0.2.0

- Removed the service template from the Ansible role as it will not be used right now.
- Updated the Ansible role and enabled installation of a PostgreSQL server for both development and production.
- `parser_utils.py`: Added two new functions `clean_affiliation_email` and `extract_affiliation_email` to remove any email addresses from affiliations and extract email addresses from affiliations respectively.
- `orm.py`: Updated the `Author` class and added an `email` field that may store the author email should it be included in the affiliation. The email was also included in the author MD5.
- `dals.py`: Updated the `biodi_authors` method to include author emails.
- `parsers.py`: Updated the `parse_affiliation_info` method to remove any email addresses from the affiliation itself.
- `parsers.py`: Added a new `extract_affiliation_info_emails` method to the `ParserXmlPubmedArticle` class to extract email addresses from author affiliations and updated the `parse_author` method to store that affiliation in the author document.
- `ingesters.py`: Updated the `ingest_authors` method of the `IngesterDocumentPubmedArticle` class to ingest author email addresses.
- Recreated the initial alembic schema.
- Added a new script to perform the ingestion of the Pubmed baseline files on the target server.
- Added a new script to perform a profiling of the ingestion of a Pubmed XML file.

### v0.1.1

- Added a production `requirements.txt`.

### v0.1.0

- Initial release.
