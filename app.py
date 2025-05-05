from flask import Flask, render_template, request, flash, redirect, url_for
from modules.uploader import save_and_load
from modules.cleaner import detect_missing, drop_missing, fill_missing
import pandas as pd
from modules.analyzer import run_kmeans, run_regression

# 全局 DataFrame 存储
GLOBAL_DF = None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'your-secret-key'  # 用于 flash 消息


@app.route('/', methods=['GET'])
def index():
    # 首页展示上传表单或预览
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    global GLOBAL_DF
    f = request.files.get('datafile')
    if not f or f.filename == '':
        flash("未选择文件，请重新上传")
        return redirect(url_for('index'))

    try:
        df = save_and_load(f, app.config['UPLOAD_FOLDER'])
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))

    # 存储到全局以供后续清洗使用
    GLOBAL_DF = df
    # 渲染前10行为 HTML 表格
    # 在app.py中修改表格生成代码
    table_html = df.head(10).to_html(
        classes='table table-striped table-bordered table-responsive',
        index=False,
        border=0,
        justify='left'
    )
    return render_template('index.html', table_html=table_html)


@app.route('/clean', methods=['GET', 'POST'])
def clean():
    global GLOBAL_DF
    # 未上传则跳回首页
    if GLOBAL_DF is None:
        flash("请先上传数据")
        return redirect(url_for('index'))

    # 统计缺失情况
    stats = detect_missing(GLOBAL_DF)
    cleaned_df = None
    table_html = None

    if request.method == 'POST':
        action = request.form.get('action')           # 'dropna' 或 'fillna'
        # 处理缺失值
        if action == 'dropna':
            axis = request.form.get('axis', 'rows')
            cleaned_df = drop_missing(GLOBAL_DF, axis='columns' if axis == 'columns' else 'rows')
        else:
            method = request.form.get('method', 'mean')
            cols = request.form.getlist('columns') or None
            cleaned_df = fill_missing(GLOBAL_DF, method=method, columns=cols)

        # 更新全局 DataFrame
        GLOBAL_DF = cleaned_df
        table_html = cleaned_df.head(10).to_html(classes='table table-striped', index=False)

    return render_template(
        'clean.html',
        stats=stats,
        columns=GLOBAL_DF.columns.tolist(),
        preview_html=table_html
    )



@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    global GLOBAL_DF
    if GLOBAL_DF is None:
        flash("请先上传并清洗数据")
        return redirect(url_for('index'))

    columns = list(GLOBAL_DF.select_dtypes(include='number').columns)
    result = None

    if request.method == 'POST':
        algo = request.form['algorithm']
        if algo == 'kmeans':
            n_clusters = int(request.form.get('n_clusters', 3))
            features = request.form.getlist('features')
            result = run_kmeans(GLOBAL_DF, features, n_clusters)
        elif algo == 'regression':
            target = request.form['target']
            features = request.form.getlist('features')
            result = run_regression(GLOBAL_DF, features, target)

    return render_template(
        'analyze.html',
        columns=columns,
        result=result
    )



if __name__ == '__main__':
    app.run(debug=True)
