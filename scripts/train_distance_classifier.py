from grant_doc_data1 import npi_classifier, npi_reader, distances, distances_classifier

df1 = npi_reader.read()
nc = npi_classifier.NPIClassifier('data')

df2 = distances.read()
dc = distances_classifier.distancesClassifier('data')

nc.train()
nc.save()