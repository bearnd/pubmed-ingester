# coding=utf-8

import multiprocessing
from typing import List, Dict, Optional, Tuple, Union

import sqlalchemy.orm
from fform.dals_pubmed import DalPubmed
from fform.orm_pubmed import Affiliation

from pubmed_ingester.config import import_config
from pubmed_ingester.loggers import create_logger
from pubmed_ingester.retrievers import RetrieverGoogleMaps
from pubmed_ingester.utils import find_affiliation_google_place
from pubmed_ingester.utils import chunk_generator


logger = create_logger(logger_name=__name__)


def _get_address_component_name(
    address_components: List[Dict],
    include_types: Tuple[str],
    exclude_types: Optional[Tuple[str, ...]] = (),
) -> Union[str, None]:

    component = None
    for _component in address_components:
        s01 = set(_component["types"])
        s02 = set(include_types)
        s03 = set(exclude_types)

        # If the component `types` don't contain all `include_types` then
        # skip the component.
        if not s01.issuperset(s02):
            continue

        # If the componment `types` include any of the `exclude_types` then
        # skip the component.
        if s01.intersection(s03):
            continue

        component = _component
        break

    if component:
        return component["long_name"]

    return None


def find_place(affiliation: Affiliation):
    global retriever
    return find_affiliation_google_place(retriever, affiliation)


def populate():

    with dal.session_scope() as session:
        query = session.query(Affiliation)  # type: sqlalchemy.orm.Query
        query = query.filter(Affiliation.affiliation_canonical_id.is_(None))

        affiliations_chunks = chunk_generator(
            generator=iter(query.yield_per(50)),
            chunk_size=50,
        )
        pool = multiprocessing.Pool(processes=50)
        for affiliations_chunk in affiliations_chunks:

            affiliations = list(affiliations_chunk)
            responses = pool.map(find_place, affiliations)

            for affiliation, response in zip(affiliations, responses):

                if not response:
                    continue

                # Retrieving Google Place ID from the first candidate.
                place_id = response["candidates"][0]["place_id"]

                affiliation_canonical_id = dal.iodu_affiliation_canonical(
                    google_place_id=place_id,
                    name=None,
                    google_url=None,
                    url=None,
                    address=None,
                    phone_number=None,
                    coordinate_longitude=None,
                    coordinate_latitude=None,
                    country=None,
                    administrative_area_level_1=None,
                    administrative_area_level_2=None,
                    administrative_area_level_3=None,
                    administrative_area_level_4=None,
                    administrative_area_level_5=None,
                    locality=None,
                    sublocality=None,
                    sublocality_level_1=None,
                    sublocality_level_2=None,
                    sublocality_level_3=None,
                    sublocality_level_4=None,
                    sublocality_level_5=None,
                    colloquial_area=None,
                    floor=None,
                    room=None,
                    intersection=None,
                    neighborhood=None,
                    post_box=None,
                    postal_code=None,
                    postal_code_prefix=None,
                    postal_code_suffix=None,
                    postal_town=None,
                    premise=None,
                    subpremise=None,
                    route=None,
                    street_address=None,
                    street_number=None,
                )

                dal.update_attr_value(
                    orm_class=Affiliation,
                    pk=affiliation.affiliation_id,
                    attr_name="affiliation_canonical_id",
                    attr_value=affiliation_canonical_id,
                )


if __name__ == '__main__':
    cfg = import_config("/etc/pubmed-ingester/pubmed-ingester-dev.json")

    dal = DalPubmed(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host="192.168.0.12",
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    retriever = RetrieverGoogleMaps(api_key=cfg.google_maps_api_key)

    populate()
