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
import win_preprocessor

import warnings
warnings.filterwarnings("ignore")


def model_eval(model, x_train, y_train, x_test, y_test):
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))


if __name__ == "__main__":

    # pulling transaction data from database
    collector = win_collector.DataCollector()
    collector.main(name="combined_dataset")

    # load in csv into a pandas dataframe
    data = pd.read_csv('./combined_dataset')
    preprocessor = win_preprocessor.Preprocessor(data)
    preprocessor.remove_features()

    y = data.iloc[:, 0]
    X = data.iloc[:, 1:]

    # split data into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # oversampling
    x_train_sm, y_train_sm = SMOTE().fit_resample(X_train, y_train)

    # initialization of XGBoost classifier
    xgb_clf = XGBClassifier(use_label_encoder=False, eval_metric="error")

    # train and evaluate
    model_eval(xgb_clf, x_train_sm, y_train_sm, X_test, y_test)

