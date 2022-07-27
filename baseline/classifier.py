import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
#import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import imblearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from imblearn.over_sampling import SMOTE
from collections import Counter
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier
from xgboost import plot_tree
import graphviz
from xgboost import plot_importance
import preprocessor
import win_collector

import warnings
warnings.filterwarnings("ignore")


def model_eval(model, x_train, y_train, x_test, y_test):
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    print(classification_report(y_test, predictions))

    cm = confusion_matrix(y_test, predictions, labels=model.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    disp.plot()
    plt.show()

    f1_score(y_test, predictions, average="weighted")

    probs = model.predict_proba(X_test)
    probs = probs[:, 1]

    auc = roc_auc_score(y_test, predictions)
    print("AUC: %.3f" % auc)

    fpr, tpr, thresholds = roc_curve(y_test, probs)

    model_name = type(model).__name__
    plt.plot([0, 1], [0, 1], linestyle='--', label="No skill")
    plt.plot(fpr, tpr, marker=".", label=model_name)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.show()


if __name__ == "__main__":

    collector = win_collector.DataCollector()
    collector.main(name="combined_dataset")


