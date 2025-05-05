# modules/cleaner.py
import pandas as pd

def detect_missing(df: pd.DataFrame) -> dict:
    """
    返回各列缺失值统计。
    """
    return df.isnull().sum().to_dict()

def drop_missing(df, axis='rows'):
    """
    删除含缺失值的行或列。
    axis: 'rows' 或 'columns'
    """
    if axis == 'columns':
        return df.dropna(axis=1)
    return df.dropna(axis=0)

def fill_missing(df, method='mean', columns=None):
    """
    填充缺失值。
    method: 'mean' | 'median' | 'zero' | 'ffill' | 'bfill'
    columns: list, 要填充的列；None 表示全表
    """
    cols = columns if columns else df.columns
    df2 = df.copy()
    for col in cols:
        if method == 'mean' and pd.api.types.is_numeric_dtype(df2[col]):
            df2[col].fillna(df2[col].mean(), inplace=True)
        elif method == 'median' and pd.api.types.is_numeric_dtype(df2[col]):
            df2[col].fillna(df2[col].median(), inplace=True)
        elif method == 'zero':
            df2[col].fillna(0, inplace=True)
        elif method in ('ffill', 'bfill'):
            df2[col].fillna(method=method, inplace=True)
        else:
            # 对非数值列可做前向填充
            df2[col].fillna(method='ffill', inplace=True)
    return df2

def detect_outliers_zscore(df, columns=None, threshold=3.0):
    """
    基于 Z-score 检测异常值，返回布尔掩码。
    columns: 要检测的列列表；None 默认所有数值列
    """
    import numpy as np
    from scipy import stats

    cols = columns if columns else df.select_dtypes(include='number').columns
    mask = pd.Series(False, index=df.index)
    for col in cols:
        col_zscore = np.abs(stats.zscore(df[col].dropna()))
        # 只对非 NaN 部分打标
        mask[col_zscore.index] |= (col_zscore > threshold)
    return mask

def drop_outliers(df, columns=None, threshold=3.0):
    """
    删除异常值所在行。
    """
    mask = detect_outliers_zscore(df, columns, threshold)
    return df.loc[~mask]
