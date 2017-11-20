## Changelog

### v0.2.1

- Removed the obsolete alembic migration for the old initial schema.

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
