import re
import os
import csv
import json
from pathlib import Path

FILE_NAME_CAND = r"elcand*.csv"
FILE_NAME_PARTY = r"elpaty.csv"
FILE_NAME_REPM = r"elrepm*.csv"

SCHEMA = {
    FILE_NAME_CAND: [
        "province", "county", "area", "city", "village", "number", "name", "partyNo",
        "gender", "birth", "age", "birthPlace", "education", "incumbent", "win", "vice"
    ],
    FILE_NAME_PARTY: ["number", "name"],
    FILE_NAME_REPM: ["partyNo", "rank", "name", "gender", "birth", "age", "birthPlace", "education", "incumbent", "win"]
}

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = f'{FILE_DIR}/../../../data/raw/voteData/'
POLITICS_FILE_PATH = f'{FILE_DIR}/../../../data/organized/2016-politics.json'
print(os.path.abspath(SOURCE_DIR))


def readRawData():
    history_info = {}
    politics_info = {}
    with open(POLITICS_FILE_PATH, "r") as f:
        politics_info = json.load(f)

    for cand_filename in Path(SOURCE_DIR).glob(f'**/{FILE_NAME_CAND}'):
        dir = os.path.dirname(cand_filename)

        print("processing", os.path.abspath(dir))

        party_filename = dir + "/" + FILE_NAME_PARTY
        party_mappings = {}

        with open(party_filename) as pf:
            reader = csv.DictReader(pf, fieldnames=SCHEMA[FILE_NAME_PARTY])
            for row in reader:
                party_mappings[row["number"]] = row["name"]

        repm_files = list(Path(dir).glob(FILE_NAME_REPM))

        if len(repm_files) > 0:
            with open(repm_files[0]) as cf:
                reader = csv.DictReader(cf, fieldnames=SCHEMA[FILE_NAME_REPM])
                for row in reader:
                    row["party"] = party_mappings[re.sub(r"\D", "", row["partyNo"].strip())]  # strip() to prevent some dirty data like "1 "
                    row["electionName"] = "-".join(dir.split("voteData/")[1].split("/"))
                    history_info.setdefault(row['name'], []).append(row)
        else:
            with open(cand_filename) as cf:
                reader = csv.DictReader(cf, fieldnames=SCHEMA[FILE_NAME_CAND])
                for row in reader:
                    row["party"] = party_mappings[re.sub(r"\D", "", row["partyNo"].strip())]  # strip() to prevent some dirty data like "1 "
                    row["electionName"] = "-".join(dir.split("voteData/")[1].split("/"))
                    if row["electionName"].startswith("2016") and row["name"] in politics_info:
                        row["politics"] = politics_info[row["name"]]
                    history_info.setdefault(row['name'], []).append(row)
    return history_info


HISTORY_INFO = readRawData()


def getHistory(name: str):
    return HISTORY_INFO.get(name, [])