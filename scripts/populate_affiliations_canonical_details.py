# coding=utf-8

import multiprocessing
from typing import List, Dict, Optional, Tuple, Union

import sqlalchemy.orm
from fform.dals_pubmed import DalPubmed
from fform.orm_pubmed import AffiliationCanonical

from pubmed_ingester.config import import_config
from pubmed_ingester.loggers import create_logger
from pubmed_ingester.retrievers import RetrieverGoogleMaps
from pubmed_ingester.retrievers import get_place_details
from pubmed_ingester.utils import chunk_generator


logger = create_logger(logger_name=__name__)


api_keys = [
    "AIzaSyCJ65svcyTj2fEpBgjNhL7_Zk7yhfQxh6Y",
    "AIzaSyBBU2IJcRgMtYnCEgYwoVVTIZ_tR-kKg_g",
    "AIzaSyBhYcbF_PtLpA_BuckzQfd2A6XeWxF3s-Y",
    "AIzaSyDhG5rV9SNu0uQV88lq9QvjXRXI_Mzz3Lo",
]


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


def _get_place_details(google_place_id):
    global retriever
    return get_place_details(
        google_place_id=google_place_id,
        retriever=retriever
    )


def populate():

    with dal.session_scope() as session:

        # Query out `AffiliationCanonical` records without a country, i.e.,
        # records that haven't had their details filled out.
        query = session.query(
            AffiliationCanonical,
        )  # type: sqlalchemy.orm.Query
        query = query.filter(AffiliationCanonical.country.is_(None))

        # Chunk the query results.
        affiliations_chunks = chunk_generator(
            generator=iter(query.yield_per(50)),
            chunk_size=50,
        )
        # Create a process pool.
        pool = multiprocessing.Pool(processes=50)

        for affiliations_chunk in affiliations_chunks:

            affiliations = list(affiliations_chunk)
            google_place_ids = [
                affiliation.google_place_id for affiliation in affiliations
            ]
            responses = pool.map(_get_place_details, google_place_ids)

            for affiliation, response in zip(affiliations, responses):

                if not response:
                    continue

                result = response["result"]

                components = result["address_components"]

                # # Fallback to the country defined in the facility if Google
                # # returns no country.
                country = _get_address_component_name(
                    components, ("country",)
                )
                # country = country if country else facility.country

                dal.iodu_affiliation_canonical(
                    google_place_id=affiliation.google_place_id,
                    name=result["name"],
                    google_url=result["url"],
                    url=result.get("website"),
                    address=result["formatted_address"],
                    phone_number=result.get("international_phone_number"),
                    coordinate_longitude=result["geometry"]["location"]["lng"],
                    coordinate_latitude=result["geometry"]["location"]["lat"],
                    country=country,
                    administrative_area_level_1=_get_address_component_name(
                        components,
                        ("administrative_area_level_1",)
                    ),
                    administrative_area_level_2=_get_address_component_name(
                        components,
                        ("administrative_area_level_2",)
                    ),
                    administrative_area_level_3=_get_address_component_name(
                        components,
                        ("administrative_area_level_3",)
                    ),
                    administrative_area_level_4=_get_address_component_name(
                        components,
                        ("administrative_area_level_4",)
                    ),
                    administrative_area_level_5=_get_address_component_name(
                        components,
                        ("administrative_area_level_5",)
                    ),
                    locality=_get_address_component_name(
                        components, ("locality",)
                    ),
                    sublocality=_get_address_component_name(
                        components,
                        ("sublocality",),
                        (
                            "sublocality_level_1",
                            "sublocality_level_2",
                            "sublocality_level_3",
                            "sublocality_level_4",
                            "sublocality_level_5",
                        )
                    ),
                    sublocality_level_1=_get_address_component_name(
                        components,
                        ("sublocality_level_1",)
                    ),
                    sublocality_level_2=_get_address_component_name(
                        components,
                        ("sublocality_level_2",)
                    ),
                    sublocality_level_3=_get_address_component_name(
                        components,
                        ("sublocality_level_3",)
                    ),
                    sublocality_level_4=_get_address_component_name(
                        components,
                        ("sublocality_level_4",)
                    ),
                    sublocality_level_5=_get_address_component_name(
                        components,
                        ("sublocality_level_5",)
                    ),
                    colloquial_area=_get_address_component_name(
                        components,
                        ("colloquial_area",)
                    ),
                    floor=_get_address_component_name(
                        components,
                        ("floor",)
                    ),
                    room=_get_address_component_name(
                        components,
                        ("room",)
                    ),
                    intersection=_get_address_component_name(
                        components,
                        ("intersection",)
                    ),
                    neighborhood=_get_address_component_name(
                        components,
                        ("neighborhood",)
                    ),
                    post_box=_get_address_component_name(
                        components,
                        ("post_box",)
                    ),
                    postal_code=_get_address_component_name(
                        components,
                        ("postal_code",)
                    ),
                    postal_code_prefix=_get_address_component_name(
                        components,
                        ("postal_code_prefix",)
                    ),
                    postal_code_suffix=_get_address_component_name(
                        components,
                        ("postal_code_suffix",)
                    ),
                    postal_town=_get_address_component_name(
                        components,
                        ("postal_town",)
                    ),
                    premise=_get_address_component_name(
                        components,
                        ("premise",)
                    ),
                    subpremise=_get_address_component_name(
                        components,
                        ("subpremise",)
                    ),
                    route=_get_address_component_name(
                        components,
                        ("route",)
                    ),
                    street_address=_get_address_component_name(
                        components,
                        ("street_address",)
                    ),
                    street_number=_get_address_component_name(
                        components,
                        ("street_number",)
                    ),
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

    retriever = RetrieverGoogleMaps(api_key=api_keys[1])

    while True:
        try:
            populate()
        except:
            pass
