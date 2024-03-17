from grant_doc_data1 import npi_classifier, npi_reader, distances_classifier, string_distance_features

df1 = npi_reader.read()
nc = npi_classifier.NPIClassifier('data')

df2 = string_distance_features.read()
dc = distances_classifier.distancesClassifier('data')

nc.train()
nc.save()