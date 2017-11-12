# -*- coding: utf-8 -*-

import re
import datetime


month_abbreviations = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

regex_orcid = re.compile("(\d{4}-?\d{4}-?\d{4}-?\d{4})")


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
        elif month_element_text in month_abbreviations:
            result["Month"] = month_abbreviations[month_element_text]

    if day_element is not None:
        # Extract the text out of the element.
        day_element_text = day_element.text
        # Lowercase and strip any whitespace from the string.
        day_element_text = day_element_text.lower().strip()
        # If the string is a digit then convert it to an integer.
        if day_element_text.isdigit():
            result["Day"] = day_element_text

    if result["Year"] and result["Month"] and result["Day"]:
        result["Date"] = datetime.date(
            year=int(result["year"]),
            month=int(result["month"]),
            day=int(result["day"])
        )

    return result


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
