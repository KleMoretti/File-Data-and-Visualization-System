# modules/analyzer.py

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import silhouette_score, mean_squared_error

def run_kmeans(df: pd.DataFrame, features: list, n_clusters: int = 3):
    """
    在 df[features] 上跑 KMeans 聚类，返回 labels 与轮廓系数。
    """
    X = df[features].dropna()
    km = KMeans(n_clusters=n_clusters, random_state=42)
    labels = km.fit_predict(X)
    score = silhouette_score(X, labels)
    return {
        'labels': labels,
        'centers': km.cluster_centers_,
        'silhouette': round(score, 4)
    }

def run_regression(df: pd.DataFrame, feature_cols: list, target_col: str):
    """
    用线性回归预测 target_col，返回模型系数、截距与 MSE。
    """
    data = df[feature_cols + [target_col]].dropna()
    X = data[feature_cols].values
    y = data[target_col].values
    lr = LinearRegression()
    lr.fit(X, y)
    preds = lr.predict(X)
    mse = mean_squared_error(y, preds)
    return {
        'coef': lr.coef_.tolist(),
        'intercept': lr.intercept_,
        'mse': round(mse, 4)
    }
