# coding=utf-8

from pubmed_ingester.config import import_config
from pubmed_ingester.loggers import create_logger

from fform.dals_pubmed import DalPubmed
from fform.orm_pubmed import Affiliation
from fform.orm_pubmed import ArticleAuthorAffiliation

logger = create_logger(logger_name=__name__)


def populate():

    with dal.session_scope() as session:

        query = session.query(ArticleAuthorAffiliation)
        for aaf in query.yield_per(10):
            msg_fmt = "Processing ArticleAuthorAffiliation {}".format(aaf)
            logger.info(msg_fmt)

            if not aaf.affiliation_id:
                continue

            # Retrieve the linked `Affiliation` record object.
            aff = dal.get(
                Affiliation,
                pk=aaf.affiliation_id
            )  # type: Affiliation

            # Skip the entry if `affiliation_canonical_id` is not defined.
            if not aff.affiliation_canonical_id:
                continue

            # Update the `ArticleAuthorAffiliation` record with the
            # `affiliation_canonical_id`.
            dal.update_attr_value(
                orm_class=ArticleAuthorAffiliation,
                pk=aaf.article_author_affiliation_id,
                attr_name="affiliation_canonical_id",
                attr_value=aff.affiliation_canonical_id
            )


if __name__ == '__main__':

    cfg = import_config("/etc/pubmed-ingester/pubmed-ingester-dev.json")

    # Create a new PubMed DAL.
    dal = DalPubmed(
        sql_username="somada141",
        sql_password="BcOGAdy6kHnk0tIcLyYLRcfB8ZiqT6PiSn8mHjc6",
        sql_host="192.168.0.12",
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    populate()
