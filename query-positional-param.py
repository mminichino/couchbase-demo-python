#!/usr/bin/env python3

from democonstants import CBCLUSTER, CBUSER, CBPASSWORD
import sys

from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator

pa = PasswordAuthenticator(CBUSER, CBPASSWORD)

cluster = Cluster('couchbases://' + CBCLUSTER + '?ssl=no_verify', ClusterOptions(pa))
bucket = cluster.bucket('travel-sample')

query = """
  SELECT h.name, h.city, h.state
  FROM `travel-sample` h
  WHERE h.type = $1
    AND h.city = $2 LIMIT 5
"""

try:
  result = cluster.query(query, 'hotel', 'Malibu')

  for row in result:
    # each row is an instance of the query call
    name = row['name']
    city = row['city']
    print("hotel: {} in {}".format(name, city))

except:
  print("exception:", sys.exc_info()[0])
