#!/usr/bin/env python3

from democonstants import CBCLUSTER, CBUSER, CBPASSWORD
import sys
import couchbase.subdocument as SD

from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator

pa = PasswordAuthenticator(CBUSER, CBPASSWORD)
cluster = Cluster('couchbases://' + CBCLUSTER + '?ssl=no_verify', ClusterOptions(pa))
bucket = cluster.bucket('travel-sample')
collection = bucket.default_collection()

try:
  result = collection.lookup_in('airline_10', [SD.get('country')])
  country = result.content_as[str](0)
  print("Sub-doc before:")
  print("country:", country)

except:
  print("exception:", sys.exc_info()[0])

try:
  collection.mutate_in("airline_10", [SD.upsert("country", "United States")])

except:
  print("exception:", sys.exc_info()[0])

try:
  result = collection.lookup_in('airline_10', [SD.get('country')])
  country = result.content_as[str](0)
  print("Sub-doc after:")
  print("country:", country)

except:
  print("exception:", sys.exc_info()[0])
