# coding=utf-8

import argparse
import binascii
import csv
from typing import List, Dict

from shapely import wkb
import sqlalchemy.orm
from fform.dals_pubmed import DalPubmed
from fform.orm_pubmed import Affiliation
from fform.orm_pubmed import AffiliationCanonical

from pubmed_ingester.config import import_config
from pubmed_ingester.loggers import create_logger
from pubmed_ingester.utils import chunk_generator


logger = create_logger(logger_name=__name__)


def read_affiliations(filename_affiliations_csv):

    msg = "Reading `affiliations` CSV file '{}'"
    msg_fmt = msg.format(filename_affiliations_csv)
    logger.info(msg_fmt)

    affiliations = {}
    with open(filename_affiliations_csv) as finp:
        reader = csv.DictReader(
            finp,
            fieldnames=[
                "affiliation_id",
                "affiliation_identifier",
                "affiliation_identifier_source",
                "affiliation",
                "md5",
                "affiliation_canonical_id",
            ],
            delimiter="|",
        )
        for entry in reader:
            md5 = entry["md5"].replace("\\x", "")
            affiliations[md5] = entry

    return affiliations


def read_affiliations_canonical(filename_affiliations_canonical_csv):

    msg = "Reading `affiliations_canonical` CSV file '{}'"
    msg_fmt = msg.format(filename_affiliations_canonical_csv)
    logger.info(msg_fmt)

    affiliations_canonical = {}
    with open(filename_affiliations_canonical_csv) as finp:
        reader = csv.DictReader(
            finp,
            fieldnames=[
                "affiliation_canonical_id",
                "google_place_id",
                "name",
                "google_url",
                "url",
                "address",
                "phone_number",
                "coordinates",
                "country",
                "administrative_area_level_1",
                "administrative_area_level_2",
                "administrative_area_level_3",
                "administrative_area_level_4",
                "administrative_area_level_5",
                "locality",
                "sublocality",
                "sublocality_level_1",
                "sublocality_level_2",
                "sublocality_level_3",
                "sublocality_level_4",
                "sublocality_level_5",
                "colloquial_area",
                "floor",
                "room",
                "intersection",
                "neighborhood",
                "post_box",
                "postal_code",
                "postal_code_prefix",
                "postal_code_suffix",
                "postal_town",
                "premise",
                "subpremise",
                "route",
                "street_address",
                "street_number",
            ],
            delimiter="|",
        )
        for entry in reader:
            affiliations_canonical[entry["affiliation_canonical_id"]] = entry

    return affiliations_canonical


def ingest_affiliation_canonical_old(affiliation_canonical_old):

    msg = "Ingesting canonical affiliation with Google Place ID '{}'"
    msg_fmt = msg.format(affiliation_canonical_old["google_place_id"])
    logger.info(msg_fmt)

    coordinates_str_hex = affiliation_canonical_old["coordinates"]
    if coordinates_str_hex:
        coordinates_str_bin = binascii.unhexlify(coordinates_str_hex)
        point = wkb.loads(coordinates_str_bin)
        coordinate_longitude = point.x
        coordinate_latitude = point.y
    else:
        coordinate_longitude = None
        coordinate_latitude = None

    affiliation_canonical_id = dal.iodu_affiliation_canonical(
        google_place_id=affiliation_canonical_old["google_place_id"],
        name=affiliation_canonical_old["name"],
        google_url=affiliation_canonical_old["name"],
        url=affiliation_canonical_old["url"],
        address=affiliation_canonical_old["address"],
        phone_number=affiliation_canonical_old["phone_number"],
        coordinate_longitude=coordinate_longitude,
        coordinate_latitude=coordinate_latitude,
        country=affiliation_canonical_old["country"],
        administrative_area_level_1=
        affiliation_canonical_old["administrative_area_level_1"],
        administrative_area_level_2=
        affiliation_canonical_old["administrative_area_level_2"],
        administrative_area_level_3=
        affiliation_canonical_old["administrative_area_level_3"],
        administrative_area_level_4=
        affiliation_canonical_old["administrative_area_level_4"],
        administrative_area_level_5=
        affiliation_canonical_old["administrative_area_level_5"],
        locality=affiliation_canonical_old["locality"],
        sublocality=affiliation_canonical_old["sublocality"],
        sublocality_level_1=affiliation_canonical_old["sublocality_level_1"],
        sublocality_level_2=affiliation_canonical_old["sublocality_level_2"],
        sublocality_level_3=affiliation_canonical_old["sublocality_level_3"],
        sublocality_level_4=affiliation_canonical_old["sublocality_level_4"],
        sublocality_level_5=affiliation_canonical_old["sublocality_level_5"],
        colloquial_area=affiliation_canonical_old["colloquial_area"],
        floor=affiliation_canonical_old["floor"],
        room=affiliation_canonical_old["room"],
        intersection=affiliation_canonical_old["intersection"],
        neighborhood=affiliation_canonical_old["neighborhood"],
        post_box=affiliation_canonical_old["post_box"],
        postal_code=affiliation_canonical_old["postal_code"],
        postal_code_prefix=affiliation_canonical_old["postal_code_prefix"],
        postal_code_suffix=affiliation_canonical_old["postal_code_suffix"],
        postal_town=affiliation_canonical_old["postal_town"],
        premise=affiliation_canonical_old["premise"],
        subpremise=affiliation_canonical_old["subpremise"],
        route=affiliation_canonical_old["route"],
        street_address=affiliation_canonical_old["street_address"],
        street_number=affiliation_canonical_old["street_number"],
    )

    return affiliation_canonical_id


def find_matching_affiliation_old(
    affiliation_new: Affiliation,
    affiliations_old: Dict[str, Dict[str, str]],
):

    # Get the hexadecimal MD5 of the new affiliation.
    md5_hex = affiliation_new.md5.hex()

    if md5_hex in affiliations_old:
        return affiliations_old[md5_hex]

    for key, affiliation_old in affiliations_old.items():

        if (
            affiliation_new.affiliation_identifier and
            affiliation_new.affiliation_identifier
            != affiliation_old["affiliation_identifier"]
        ):
            continue

        if (
            affiliation_new.affiliation_identifier_source and
            affiliation_new.affiliation_identifier_source
            != affiliation_old["affiliation_identifier_source"]
        ):
            continue

        if affiliation_new.affiliation == affiliation_old["affiliation"]:
            return affiliation_old

    return None


def populate(
    filename_affiliations_csv: str,
    filename_affiliations_canonical_csv: str
):
    # Read the previous `affiliations` table dump CSV.
    affiliations_old = read_affiliations(
        filename_affiliations_csv=filename_affiliations_csv,
    )
    # Read the previous `affiliations_canonical` table dump CSV.
    affiliations_canonical_old = read_affiliations_canonical(
        filename_affiliations_canonical_csv=filename_affiliations_canonical_csv,
    )

    with dal.session_scope() as session:
        # Query out `Affiliations` records without a canonical affiliation ID.
        query = session.query(Affiliation)  # type: sqlalchemy.orm.Query
        query = query.filter(Affiliation.affiliation_canonical_id.is_(None))

        # Chunk the query results.
        affiliations_chunks = chunk_generator(
            generator=iter(query.yield_per(50)),
            chunk_size=50,
        )

        # Iterate over the new affiliations in a chunked-fashion.
        for affiliations_chunk in affiliations_chunks:
            affiliations_new = list(
                affiliations_chunk,
            )  # type: List[Affiliation]

            # Iterate over the new affiliations chunk.
            for affiliation_new in affiliations_new:
                msg = "Processing affiliation with ID '{}'"
                msg_fmt = msg.format(affiliation_new.affiliation_id)
                logger.info(msg_fmt)

                affiliation_old = find_matching_affiliation_old(
                    affiliation_new=affiliation_new,
                    affiliations_old=affiliations_old,
                )

                # Skip new affiliations that aren't represented in
                # `affiliations_old`.
                if not affiliation_old:
                    logger.debug("No match")
                    continue

                # Retrieve the ID of the old canonical affiliation this
                # affiliation should be associated with.
                affiliation_canonical_id_old = affiliation_old[
                    "affiliation_canonical_id"
                ]

                if (
                    affiliation_canonical_id_old not in
                    affiliations_canonical_old
                ):
                    logger.debug("Canonical affiliation ID mismatch")
                    continue

                # Retrieve the data of the associated old canonical affiliation.
                affiliation_canonical_old = affiliations_canonical_old[
                    affiliation_canonical_id_old
                ]

                # (Attempt to) retrieve the newly stored canonical affiliation
                # (possibly in a previous run of this script).
                affiliation_canonical_new = dal.get_by_attr(
                    orm_class=AffiliationCanonical,
                    attr_name="google_place_id",
                    attr_value=affiliation_canonical_old["google_place_id"],
                )  # type: AffiliationCanonical

                # If the canonical affiliation has not been stored anew
                # (possibly in a previous run) of this script then store it.
                # Otherwise retrieve the ID from the retrieved record.
                if not affiliation_canonical_new:
                    affiliation_canonical_id_new = \
                        ingest_affiliation_canonical_old(
                            affiliation_canonical_old=
                            affiliation_canonical_old,
                        )
                else:
                    affiliation_canonical_id_new = \
                        affiliation_canonical_new.affiliation_canonical_id

                # Update the affiliation with the canonical affiliation ID.
                dal.update_attr_value(
                    orm_class=Affiliation,
                    pk=affiliation_new.affiliation_id,
                    attr_name="affiliation_canonical_id",
                    attr_value=affiliation_canonical_id_new,
                )


if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(
        description="Canonical affiliations porting utility.",
    )
    argument_parser.add_argument(
        "--affiliations-dump",
        dest="filename_affiliations_csv",
        help="Dumped CSV of the `affiliations` table.",
        required=True,
    )
    argument_parser.add_argument(
        "--affiliations-canonical-dump",
        dest="filename_affiliations_canonical_csv",
        help="Dumped CSV of the `affiliations_canonical` table.",
        required=True,
    )
    arguments = argument_parser.parse_args()

    cfg = import_config("/etc/pubmed-ingester/pubmed-ingester-dev.json")
    # Create a new DAL.
    dal = DalPubmed(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host="localhost",
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    populate(
        filename_affiliations_csv=arguments.filename_affiliations_csv,
        filename_affiliations_canonical_csv=
        arguments.filename_affiliations_canonical_csv,
    )
