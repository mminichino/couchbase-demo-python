#!/usr/bin/env python3

from democonstants import CBCLUSTER, CBUSER, CBPASSWORD
import sys
import json

from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator

pa = PasswordAuthenticator(CBUSER, CBPASSWORD)
cluster = Cluster('couchbases://' + CBCLUSTER + '?ssl=no_verify', ClusterOptions(pa))

bucket = cluster.bucket('travel-sample')
collection = bucket.default_collection()

try:
  result = collection.get('airline_10')
  print(json.dumps(result.content, indent=2))

except:
  print("exception:", sys.exc_info()[0])
