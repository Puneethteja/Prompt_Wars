import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.metrics import confusion_matrix
import joblib



df = pd.read_csv(
    "Prompt_Wars\dataset.csv",
    encoding="utf-8"
)
X = df["prompt"]

y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,
   random_state=1

)
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

vectorizer = TfidfVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

model = LogisticRegression()
model.fit(
    X_train_vectorized,
    y_train
)

predictions = model.predict(
    X_test_vectorized
)



print(
    "Accuracy:",
    accuracy_score(y_test, predictions)
)

print(
    "Precision:",
    precision_score(y_test, predictions)
)

print(
    "Recall:",
    recall_score(y_test, predictions)
)

print(
    "F1 Score:",
    f1_score(y_test, predictions)
)

print(
    confusion_matrix(
        y_test,
        predictions
    )
)

joblib.dump(
    model,
    "detector.pkl"
)

joblib.dump(
    vectorizer,
    "vectorizer.pkl"
)