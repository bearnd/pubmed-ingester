# -*- coding: utf-8 -*-

import re
import datetime

from pubmed_ingester.loggers import create_logger


logger = create_logger(logger_name=__name__)

month_abbreviations = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}

regex_orcid = re.compile("(\d{4}-?\d{4}-?\d{4}-?\d{4})")
regex_year = re.compile("(\d{4})")


def parse_date_element(date_element):

    result = {
        "Year": None,
        "Month": None,
        "Day": None,
        "Date": None
    }

    if date_element is None:
        return result

    year_element = date_element.find("Year")
    month_element = date_element.find("Month")
    day_element = date_element.find("Day")

    # Extract the year (if the element exists).
    if year_element is not None:
        # Extract the text out of the element.
        year_element_text = year_element.text
        # Lowercase and strip any whitespace from the string.
        year_element_text = year_element_text.lower().strip()
        # If the string is a digit then convert it to an integer.
        if year_element_text.isdigit():
            result["Year"] = year_element_text

    # Extract the month (if the element exists).
    if month_element is not None:
        # Extract the text out of the element.
        month_element_text = month_element.text
        # Lowercase and strip any whitespace from the string.
        month_element_text = month_element_text.lower().strip()
        # If the string is a digit then convert it to an integer.
        if month_element_text.isdigit():
            result["Month"] = month_element_text
        # If the string contains a recognized month abbreviation get the digit
        # from the `month_abbreviations` dictionary.
        elif month_element_text.lower() in month_abbreviations:
            result["Month"] = month_abbreviations[month_element_text.lower()]

    if day_element is not None:
        # Extract the text out of the element.
        day_element_text = day_element.text
        # Lowercase and strip any whitespace from the string.
        day_element_text = day_element_text.lower().strip()
        # If the string is a digit then convert it to an integer.
        if day_element_text.isdigit():
            result["Day"] = day_element_text

    if result["Year"] and result["Month"] and result["Day"]:
        try:
            result["Date"] = datetime.date(
                year=int(result["Year"]),
                month=int(result["Month"]),
                day=int(result["Day"])
            )
        except ValueError:
            msg = "Date components {} cannot be combined into a date"
            msg_fmt = msg.format(result)
            logger.error(msg_fmt)

    return result


def extract_year_from_medlinedate(pubdate_element):

    if pubdate_element is None:
        return None

    medlinedate_element = pubdate_element.find("MedlineDate")

    if medlinedate_element is None:
        return None

    medline_date_text = medlinedate_element.text

    match = regex_year.search(medline_date_text)

    if match is None:
        return None

    year_max = -1
    for group in match.groups():
        if year_max < int(group):
            year_max = int(group)

    return year_max


def convert_yn_boolean(yn_boolean_raw):
    if yn_boolean_raw == "Y":
        return True
    elif yn_boolean_raw == "N":
        return False
    else:
        return None


def clean_orcid_identifier(orcid_identifier_raw):

    orcid_identifier_clean = None

    if orcid_identifier_raw is None:
        return orcid_identifier_clean

    match = regex_orcid.search(orcid_identifier_raw)

    if match is None:
        return orcid_identifier_clean

    orcid_identifier_text = match.group(0)

    if "-" not in orcid_identifier_text:
        chunks = [
            orcid_identifier_text[i:i + 4]
            for i in range(0, len(orcid_identifier_text), 4)
        ]
        orcid_identifier_clean = "-".join(chunks)
    else:
        orcid_identifier_clean = orcid_identifier_text

    return orcid_identifier_clean
