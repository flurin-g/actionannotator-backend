from typing import List

from pymongo import MongoClient
from bson.objectid import ObjectId

test_data = [{'speaker': 'me018', 'text': "That's why we have the forms, uh, even if there are no digits."},
             {'speaker': 'me013', 'text': "O_K, yeah, I didn't"},
             {'speaker': 'me018', 'text': "So I guess we're - we're done."},
             {'speaker': 'me013', 'text': "Yeah, yeah, I'll do my credit card number"}]

DB_NAME = 'acn_ann_db'

client = MongoClient()
db = client[DB_NAME]
icsi_db = db.icsi


def insert_into_icsi(data: List[dict]) -> List[ObjectId]:
    new_result = icsi_db.insert_many(data)
    return new_result.inserted_ids


if __name__ == '__main__':
    res = insert_into_icsi(test_data)

    print(f"One tutorial: {res}")
