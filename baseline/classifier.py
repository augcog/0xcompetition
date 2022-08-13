import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import win_collector
import win_preprocessor

import warnings
warnings.filterwarnings("ignore")


def model_eval(model, x_train, y_train, x_test, y_test):
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)
    return accuracy


if __name__ == "__main__":

    # pulling transaction data from database
    # collector = win_collector.DataCollector()
    # collector.main(name="combined_dataset")

    # load in csv into a pandas dataframe
    data = pd.read_csv('../CSV_files/combined_dataset.csv')
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
    print("Accuracy: %.2f%%" % (100.0 * model_eval(xgb_clf, X_train, y_train, X_test, y_test)))

