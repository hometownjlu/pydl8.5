"""
========================================================================
DL8.5 classifier : user specific error function based on transactions ID
========================================================================

"""
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time
from dl85 import DL85Predictor

dataset = np.genfromtxt("../datasets/anneal.txt", delimiter=' ')
X = dataset[:, 1:]
y = dataset[:, 0]
X = X.astype('int32')
y = y.astype('int32')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


print("#####################################################################################\n"
      "#      DL8.5 Predictor used for classification : user specific error function       #\n"
      "#####################################################################################")


# return the error and the majority class
def error(tids, y):
    classes, supports = np.unique(y.take(list(tids)), return_counts=True)
    maxindex = np.argmax(supports)
    return sum(supports) - supports[maxindex], classes[maxindex]


clf = DL85Predictor(max_depth=2, error_function=lambda tids: error(tids, y_train), time_limit=600)
start = time.perf_counter()
print("Model building...")
clf.fit(X_train, y_train)
duration = time.perf_counter() - start
print("Model built. Duration of building =", round(duration, 4))
y_pred = clf.predict(X_test)
print("Confusion Matrix below")
print(confusion_matrix(y_test, y_pred))
print("Accuracy DL8.5 on training set =", round(clf.accuracy_, 4))
print("Accuracy DL8.5 on test set =", round(accuracy_score(y_test, y_pred), 4))
