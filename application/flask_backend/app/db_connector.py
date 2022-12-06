from pymongo import MongoClient
import pymongo


def db_connection(url):
    client = pymongo.MongoClient(url)
    return client
