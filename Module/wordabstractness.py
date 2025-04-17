import pandas as pd
from pathlib import Path
from .auxiliary.modeljoiner import join_word2vec_parts
model_path = Path(__file__).resolve().parent.parent / "data" / "word_concreteness.csv"


try:
    df = pd.read_csv(model_path)
except FileNotFoundError:
    print(f"Model file not found at {model_path}")

abstract_words = df[df["Conc.M"] < 2]["Word"].sample(1500, random_state=42).tolist()
concrete_words = df[df["Conc.M"] > 4]["Word"].sample(1500, random_state=42).tolist()

import numpy as np
from sklearn.linear_model import LogisticRegression
from gensim.models import KeyedVectors


model_path = Path(__file__).resolve().parent.parent / "data" / "word2vec_500k.model.vectors.npy"

if not model_path.exists():
    join_word2vec_parts()

model_path = Path(__file__).resolve().parent.parent / "data" / "word2vec_500k.model"
if not model_path.exists():
    raise FileNotFoundError(f"Model file not found at {model_path}")


word2vec_model = KeyedVectors.load(str(model_path))

X_train = []
y_train = []

for word in abstract_words:
    if word in word2vec_model:
        X_train.append(word2vec_model[word])
        y_train.append(1)  

for word in concrete_words:
    if word in word2vec_model:
        X_train.append(word2vec_model[word])
        y_train.append(0)  

from sklearn.model_selection import train_test_split

import numpy as np
X = np.array(X_train)
y = np.array(y_train)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

clf = LogisticRegression()
clf.fit(X_train, y_train)

def is_abstract(word):
    if word in word2vec_model:
        vector = word2vec_model[word].reshape(1, -1)
        return clf.predict(vector)[0] == 1  
    return None  

def text_abstract_ratio(text):
    abstract_count = 0
    total_words = 0
    # text = clean_input_text(text)
    for word in text.split():
        if word in word2vec_model:  
            total_words += 1
            if is_abstract(word):
                abstract_count += 1
    return (abstract_count / total_words * 700) if total_words > 0 else None  


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

def plot_logistic_regression_decision_boundary():
    """
    Visualizes the logistic regression decision boundary using PCA.
    Uses the trained model (clf) and dataset (X_train, y_train).
    """
    global clf, X_train, y_train  
    
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_train)

    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=y_train, palette={0: "blue", 1: "red"}, alpha=0.5)

    
    x_min, x_max = X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1
    y_min, y_max = X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
    
    
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    Z = clf.predict(pca.inverse_transform(grid_points))  
    Z = Z.reshape(xx.shape)

    
    plt.contourf(xx, yy, Z, alpha=0.2, cmap="coolwarm")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.title("Logistic Regression Decision Boundary (PCA-reduced)")
    plt.legend(["Concrete (Blue)", "Abstract (Red)"])
    plt.show()
