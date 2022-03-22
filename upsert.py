#!/usr/bin/env python3

from democonstants import CBCLUSTER, CBUSER, CBPASSWORD
import sys
import couchbase.subdocument as SD
from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator
from datetime import timedelta

pa = PasswordAuthenticator(CBUSER, CBPASSWORD)
cluster = Cluster('couchbases://' + CBCLUSTER + '?ssl=no_verify', ClusterOptions(pa))
bucket = cluster.bucket('travel-sample')
collection = bucket.default_collection()

try:
  document = dict(
    country="Iceland", callsign="ICEAIR", iata="FI", icao="ICE",
    id=123, name="Icelandair", type="airline"
  )
  result = collection.upsert(
    'airline_123',
    document,
    expiry=timedelta(minutes=1)
  )
  print("UPSERT SUCCESS")
  print("cas result:", result.cas)
except:
  print("exception:", sys.exc_info())

try:
  result = collection.lookup_in('airline_123', [SD.get('name')])
  name = result.content_as[str](0) # "United Kingdom"
  print("name:", name)

except:
  print("exception:", sys.exc_info()[0])
