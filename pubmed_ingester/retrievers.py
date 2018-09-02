# coding=utf-8

from typing import Optional, List, Dict

import requests

from pubmed_ingester.loggers import create_logger


class RetrieverGoogleMaps(object):

    api_url_default_place_search = ("https://maps.googleapis.com/maps/api/"
                                    "place/findplacefromtext/json")

    api_url_default_place_details = ("https://maps.googleapis.com/maps/api/"
                                     "place/details/json")

    fields_defaults_place_search = [
        "place_id",
    ]

    fields_defaults_place_details = [
        "geometry/location",
        "formatted_address",
        "address_component",
        "name",
        "url",
        "formatted_phone_number",
        "international_phone_number",
        "website",
    ]

    def __init__(
        self,
        api_key: str,
        **kwargs
    ):
        """Constructor and initialization.

        Args:
            api_key (str): The Google Places API key.
        """

        # Internalize arguments.
        self.api_key = api_key

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

    def search_place(
        self,
        query: str,
        base_url: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> Dict:

        # Fallback to the default URL if none is defined.
        base_url = base_url if base_url else self.api_url_default_place_search

        # Fallback to the default fields if none are defined.
        fields = fields if fields else self.fields_defaults_place_search

        # Perform the request.
        response = requests.get(
            url=base_url,
            params={
                "key": self.api_key,
                "inputtype": "textquery",
                "input": query,
                "language": "en",
                "fields": ",".join(fields),
            }
        )

        result = None
        if response.ok:
            result = response.json()

        return result

    def get_place_details(
        self,
        google_place_id: str,
        base_url: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ):

        # Fallback to the default URL if none is defined.
        base_url = base_url if base_url else self.api_url_default_place_details

        # Fallback to the default fields if none are defined.
        fields = fields if fields else self.fields_defaults_place_details

        # Perform the request.
        response = requests.get(
            url=base_url,
            params={
                "key": self.api_key,
                "place_id": google_place_id,
                "language": "en",
                "fields": ",".join(fields),
            }
        )

        result = None
        if response.ok:
            result = response.json()

        return result
