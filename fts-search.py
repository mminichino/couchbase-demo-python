#!/usr/bin/env python3

from democonstants import CBCLUSTER, CBUSER, CBPASSWORD
import sys

from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
from couchbase.search import QueryStringQuery, SearchOptions

pa = PasswordAuthenticator(CBUSER, CBPASSWORD)
cluster = Cluster('couchbases://' + CBCLUSTER + '?ssl=no_verify', ClusterOptions(pa))
bucket = cluster.bucket('travel-sample')
collection = bucket.default_collection()

try:
  result = cluster.search_query("travel-fts-index", QueryStringQuery("swanky"), SearchOptions(limit=10))
  for row in result.rows():
      row_result = collection.get(row.id)
      name = row_result.content_as[dict]['name']
      city = row_result.content_as[dict]['city']
      print("Found row: {}: {} in {}".format(row.id, name, city))
  print("Reported total rows:{}".format(result.metadata().metrics.total_rows))
except CouchbaseException as e:
  print("Couchbase Error:"+str(e))
except Exception as ex:
  print("Error:"+str(ex))
except:
  print("exception:", sys.exc_info()[0])
