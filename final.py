# -*- coding: utf-8 -*-


from sklearn.model_selection import train_test_split
import numpy as np # Matrix and vector computation package
from sklearn.preprocessing import LabelBinarizer

from tqdm import tqdm
import sys

import itertools
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

sig = lambda t: 1 / (1 + np.exp(-t))


def extract_features(images):
	values = []
	for i in range(len(images)):
		values.append(extract_custom_feature(images[i]))
	return values


def extract_custom_feature(image):
	value = 0
	for i in range(len(image)):
		value += image[i].argmax()
	return value/80.


def load_data():
	from sklearn.datasets import load_digits
	digits = load_digits()
	return digits.images, digits.data, digits.target , digits.target_names


def auto(X_train,T_train,X_test,T_test):
	from sklearn.neural_network import MLPClassifier
	clf = MLPClassifier(solver="lbfgs",
	                    alpha=1e-5,
	                    hidden_layer_sizes=(5, 7),
	                    random_state=1)
	
	clf.fit(X_train, T_train)
	T_pred = clf.predict(X_test)
	cnf_matrix = confusion_matrix(T_test, T_pred)
	plt.matshow(cnf_matrix)
	plt.title('Confusion matrix')
	plt.colorbar()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.show()


def manual_train(max_epoch,eta,X_train,T_train):
	
	weigth_type = 0
	# 0 random
	# 1 zero
	
	print "[+] Epoch: " + str(max_epoch)
	print "[+] Eta:   " + str(eta)
	
	if weigth_type == 0:
		layer1_w = np.random.rand(66,5)
		layer2_w = np.random.rand(5, 7)
		layer3_w = np.random.rand(7,10)
	else:
		layer1_w = np.zeros((66, 5))
		layer2_w = np.zeros((5, 7))
		layer3_w = np.zeros((7, 10))
	
	print "[+] Train phase started"
	
	for epoch in tqdm(range(max_epoch)):
		for i,j in zip(X_train,T_train):
			i = i[np.newaxis]
			
			layer1_o = sig(np.dot(i, layer1_w))
			layer2_o = sig(np.dot(layer1_o, layer2_w))
			result = sig(np.dot(layer2_o, layer3_w))
			
			layer_3_delta = ((-(j - result)) * ((1 - result) * result))
			layer_2_delta = layer_3_delta.dot(layer3_w.T) * ((1 - layer2_o) * layer2_o)
			layer_1_delta = layer_2_delta.dot(layer2_w.T) * ((1 - layer1_o) * layer1_o)

			layer3_w -= eta * (layer_3_delta * layer2_o.T)
			layer2_w -= eta * (layer_2_delta * layer1_o.T)
			layer1_w -= eta * (layer_1_delta * i.T)
	
	print "[+] " + str(max_epoch) + " epochs completed"
	
	return layer1_w, layer2_w, layer3_w


def manual_test(X_test,T_test,layer1_w,layer2_w,layer3_w):
	print "[+] Train phase started"
	
	results = []
	
	for i in X_test:
		layer1_o = sig(np.dot(i, layer1_w))
		layer2_o = sig(np.dot(layer1_o, layer2_w))
		result = sig(np.dot(layer2_o, layer3_w))
		results.append(result)
	
	T_pred = []
	for i in results:
		T_pred.append(i.argmax())
	
	acc = 0
	for i,j in zip(results,T_test):
		if i.argmax() == j:
			acc += 1
	
	
	
	print "[+] Accuracy " + str(float(acc) / float(len(results)))
		
	print "[+] Test phase completed"
	
	if show_confusion_matrix == 1:
		cnf_matrix = confusion_matrix(T_test, T_pred)
		plt.matshow(cnf_matrix)
		plt.title('Confusion matrix')
		plt.colorbar()
		plt.ylabel('True label')
		plt.xlabel('Predicted label')
		plt.show()
	
	return acc


def manual(max_epoch,eta,X_train,T_train,X_test,T_test):
	
	layer1_w, layer2_w, layer3_w = manual_train(max_epoch,eta,X_train,T_train)
	acc = manual_test(X_test,T_test,layer1_w,layer2_w,layer3_w)
	return acc

normalization_factor = 16.

# sklearn kütüphanesinden resimler, resimlerin özellikleri alınıyor
images, data, target, names= load_data()

# veri factore göre normalize ediliyor
data = data / normalization_factor

# resimlerden özellik çıkarılıyor
values = extract_features(images)

#bizim çıkardığımız özellik dataya ekleniyor
data = np.column_stack([data,values])

#bias dataya ekleniyor
data = np.column_stack([data,[1/normalization_factor for i in range(len(data))]])

# train ve test seti ayrılıyor
X_train, X_test, T_train, T_test = train_test_split(data, target, test_size=0.5)

# hazır fonksiyonla yapılan işlem
#auto(X_train,T_train,X_test,T_test)

#confusion matrixleri göstermek için 1 yapılması gerek
show_confusion_matrix = 0

#odevdeki soruları seçmek için 1. soru için 1 | 2. soru için 2 | normal çalıştırma için 3
question = 1

if question == 1:
	# kendi yazdığımız fonksyionlarla yapılan öğrenme işlemi
	# ödevde istenen birinci kısım
	# ekrana yazılan sayı başarı yaklaşık %10
	accuracies = []
	max_epoch = 6000
	eta = 0.5
	for i in range(1000,max_epoch,200):
		acc = manual(i,eta,X_train,T_train,X_test,T_test)
		accuracies.append(acc)
		print "-----------------------------------"
	print accuracies
elif question == 2:
	# ödevde istenen ikinci kısım
	accuracies = []
	max_epoch = 300
	eta = 0.1
	steps = np.linspace(eta, 1, 10)
	for i in steps:
		acc = manual(max_epoch,i,X_train,T_train,X_test,T_test)
		accuracies.append(acc)
		print "-----------------------------------"
	print accuracies
else:
	eta = 0.5
	max_epoch = 1000
	acc = manual(max_epoch, eta, X_train, T_train, X_test, T_test)