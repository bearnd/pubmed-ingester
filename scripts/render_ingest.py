# coding=utf-8

import os

path = "/mnt/Downloads/_DUMP/download_station/Pubmed/2019/baseline"
fname_config = "/etc/pubmed-ingester/pubmed-ingester-prod.json"
fname_script = "ingest_pubmed.sh"

# Collect subdirectories skipping files alongside them.
subdirs = [os.path.join(path, d) for d in os.listdir(path) if "." not in d]

# Collect all XML files from the various subdirectories.
fnames = []
for fname in os.listdir(path):
    if fname.endswith(".xml.gz"):
        fnames.append(os.path.join(path, fname))

tmpl = ("python -m pubmed_ingester.pubmed_ingester {fname_xml} "
        "--config-file='{fname_config}'")

# Write out the ingestion template file.
with open(fname_script, "w") as fout:
    for fname in fnames:
        line = tmpl.format(fname_xml=fname, fname_config=fname_config)
        fout.write(line)
        fout.write("\n")
        fout.flush()
