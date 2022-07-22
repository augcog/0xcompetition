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
import collector

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

    dc = collector.DataCollector()
    print(dc.normal_transactions(index=1, address="0x804d39f546c5164af7612c3dca3683150e55bb78", flag=0))
    print(dc.token_transfer_transactions(address="0x804d39f546c5164af7612c3dca3683150e55bb78"))

    data = pd.read_csv("https://raw.githubusercontent.com/Vagif12/Ethereum-Fraud-Detection/master/datasets"
                       "/final_combined_dataset.csv")
    prepro = preprocessor.Preprocessor(data)
    prepro.remove_features()
    data.dropna(inplace=True)

    y = data.iloc[:, 0]
    X = data.iloc[:, 1:]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    print(f'Shape of the training before SMOTE: {X_train.shape, y_train.shape}')

    x_train_sm, y_train_sm = SMOTE().fit_resample(X_train, y_train)
    # print(f'Shape of the training after SMOTE: {x_train_sm.shape, y_train_sm.shape}')

    xgb_clf = XGBClassifier(use_label_encoder=False, eval_metric="error")
    model_eval(xgb_clf, X_train, y_train, X_test, y_test)

