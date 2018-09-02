# -*- coding: utf-8 -*-

import urllib.parse
import ftplib


def collect_urls(path):
    ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov")
    ftp.login()

    urls = []
    items = ftp.mlsd(path)
    for item in items:
        filename = item[0]

        if not filename.endswith(".xml.gz"):
            continue

        print(filename)
        urls.append(
            urllib.parse.urljoin(
                "ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/",
                filename
            )
        )

    return urls


if __name__ == '__main__':
    with open("pubmed_urls_baseline.txt", "w") as fout:
        for url in collect_urls(path="pubmed/baseline"):
            fout.write(url + "\n")

    with open("pubmed_urls_updatefiles.txt", "w") as fout:
        for url in collect_urls(path="pubmed/updatefiles"):
            fout.write(url + "\n")
