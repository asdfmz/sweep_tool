from flask import Flask, render_template, request, redirect, session, url_for
import sympy as sp
from sympy_codec import matrix_to_string_list, string_list_to_matrix
from matrix_logic import apply_transformation 
import config
import os


app = Flask(__name__)
app.secret_key = "session-secret-key"

# ------------------------------
# 1. 行列サイズ選択
# ------------------------------
@app.route("/", methods=["GET", "POST"])
def select_size():
    if request.method == "POST":
        rows = int(request.form["rows"])
        cols = int(request.form["cols"])
        return redirect(url_for("input_matrix", rows=rows, cols=cols))
    
    settings = {
        "min_rows": config.MIN_ROWS, 
        "max_rows": config.MAX_ROWS, 
        "min_cols": config.MIN_COLS, 
        "max_cols": config.MAX_COLS, 
    }
    return render_template("select_size.html", **settings)

# ------------------------------
# 2. 行列入力フォーム表示
# ------------------------------
@app.route("/input_matrix")
def input_matrix():
    rows = int(request.args.get("rows", 0))
    cols = int(request.args.get("cols", 0))

    if rows <= 0 or cols <= 0:
        return "行数・列数が不正です", 400

    return render_template("input_matrix.html", rows=rows, cols=cols)

# ------------------------------
# 3. 初期行列 & セッション保存
# ------------------------------
@app.route("/init_matrix", methods=["POST"])
def init_matrix():
    rows = int(request.form["rows"])
    cols = int(request.form["cols"])

    matrix_str = []
    for i in range(rows):
        row = []
        for j in range(cols):
            value = request.form.get(f"cell_{i}_{j}", "0")
            if value.strip() == "":
                value = "0"
            row.append(str(sp.sympify(value)))
        matrix_str.append(row)

    session["matrix_state"] = {
        "initial": matrix_str,
        "current": matrix_str,
        "history": []
    }
    return redirect(url_for("interactive_view"))

# ------------------------------
# 4. 基本変形実行ページ（GET/POST）
# ------------------------------
@app.route("/interactive", methods=["GET", "POST"])
def interactive_view():
    if "matrix_state" not in session:
        return redirect(url_for("select_size"))
    
    state = session["matrix_state"]
    matrix = string_list_to_matrix(state["current"])
    history = state["history"]

    if request.method == "POST":
        op = request.form["operation"]
        target = int(request.form["target"])
        factor = request.form.get("factor")
        other = request.form.get("other")

        factor = sp.sympify(factor) if factor else None
        other = int(other) if other else None

        matrix, log = apply_transformation(matrix, op, target, factor, other)
        history.append(log)
        
        session["matrix_state"] = {
            "initial": state["initial"],
            "current": matrix_to_string_list(matrix),
            "history": history
        }
        return redirect(url_for("interactive_view"))
    
    latex_result = sp.latex(matrix)
    return render_template("interactive.html", latex_result=latex_result, history=history, config=config)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)