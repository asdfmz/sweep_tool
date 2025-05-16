from flask import Flask, render_template, request, redirect, url_for
import config
from matrix_logic import parse_matrix, compute_rref  
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def select_size():
    if request.method == "GET":
        settings = {
            "min_rows": config.MIN_ROWS, 
            "max_rows": config.MAX_ROWS, 
            "min_cols": config.MIN_COLS, 
            "max_cols": config.MAX_COLS, 
        }
        return render_template("select_size.html", **settings)    
    elif request.method == "POST":
        r = int(request.form["rows"])
        c = int(request.form["cols"])
        return redirect(url_for("input_matrix", rows=r, cols=c))

@app.route("/input")
def input_matrix():
    # クエリパラメータから行数と列数を取得
    rows = int(request.args.get("rows", 0))
    cols = int(request.args.get("cols", 0))

    # 値が不正だったらエラーメッセージを返す（念のため）
    if rows <= 0 or cols <= 0:
        return "行数・列数が不正です", 400

    return render_template("input_matrix.html", rows=rows, cols=cols)

@app.route("/result", methods=["POST"])
def show_result():
    try:
        rows = int(request.form["rows"])
        cols = int(request.form["cols"])

        # 入力データから行列を構築
        matrix = parse_matrix(request.form, rows, cols)
        result_matrix = compute_rref(matrix)

        return render_template("result.html",
            rows=rows, cols=cols,
            result=str(result_matrix))

    except Exception as e:
        return f"エラーが発生しました: {str(e)}", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)