#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the module
from __future__ import print_function
import aerospike
from sklearn.externals import joblib

aerospike_namespace = 'test'
aerospike_set = 'setup_objects'

# Configure the client
config = {
  'hosts': [
    ('localhost', 3000)
  ]
}

# Joblib serializer for Aerospike
def joblib_serializer(val):
  return joblib.dump(val)

# Python objects load
objects_to_write = {}

with open('lr_model','rb') as f:
   objects_to_write["lr_model"] = joblib.load(f)

with open('count_vectorizer','rb') as f:
   objects_to_write["count_vectorizer"] = joblib.load(f)

with open('tfidf_transformer','rb') as f:
   objects_to_write["tfidf_transformer"] = joblib.load(f)
   
# Aerospike serializer for the matrices
aerospike.set_serializer(joblib_serializer)

# Create a client and connect it to the cluster
try:
  client = aerospike.client(config).connect()
except:
  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)

# Records are addressable via a tuple of (namespace, set, key)
# for k, v in objects_to_write.iteritems():
for k, v in objects_to_write.items():
  key = (aerospike_namespace, aerospike_set, k)
  try:
    client.put(key, {
      'object_id': k,
      'value': v
    })
  except Exception as e:
    import sys
    print("error: {0}".format(e), file=sys.stderr)

# Close the connection to the Aerospike cluster
client.close()
