from grant_doc_data1 import npi_classifier
from grant_doc_data1.distances import distances_classifier, string_distance_features
from grant_doc_data1.npi_data import npi_reader

df1 = npi_reader.read()
nc = npi_classifier.NPIClassifier('data')

df2 = string_distance_features.read()
dc = distances_classifier.distancesClassifier('data')

nc.train()
nc.save()