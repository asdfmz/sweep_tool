from flask import Flask, render_template, request, redirect, session, url_for
import sympy as sp
from sympy_codec import matrix_to_string_list, string_list_to_matrix
from matrix_logic import apply_transformation, gaussian_elimination_steps
import config
import os
import session_handler as sh


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
    
    return render_template("select_size.html", config=config)

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

    sh.init_session(matrix_str)
    return redirect(url_for("interactive_view"))

# ------------------------------
# 4. 基本変形実行ページ（GET/POST）
# ------------------------------
@app.route("/interactive", methods=["GET", "POST"])
def interactive_view():
    if "m" not in session:
        return redirect(url_for("select_size"))

    if request.method == "POST":
        if "back" in request.form:
            sh.step_back()
        elif "forward" in request.form:
            sh.step_forward()
        elif "to_start" in request.form:
            sh.step_to_start()
        elif "to_end" in request.form:
            sh.step_to_end()
        elif "jump_to" in request.form:
            index = int(request.form["jump_to"])
            sh.jump_to_step(index)
        elif "auto_solve" in request.form:
            steps = gaussian_elimination_steps(sh.get_current_matrix())
            for m, q in steps:
                sh.append_step(m, q)
        else:
            op = request.form["operation"]
            target = int(request.form["target"])
            factor = request.form.get("factor")
            other = request.form.get("other")

            factor = sp.sympify(factor) if factor else None
            other = int(other) if other else None

            current_matrix = sh.get_current_matrix()
            new_matrix, _ = apply_transformation(current_matrix, op, target, factor, other)

            query = {"o": op[0], "t": target, "f": str(factor) if factor else None, "r": other}
            sh.append_step(new_matrix, query)

        return redirect(url_for("interactive_view"))

    matrices = [sp.latex(string_list_to_matrix(m)) for m in sh.get_matrix_history()]
    queries = [sh.generate_log_latex(q) for q in sh.get_query_history()]
    current = sh.get_current_step()
    query_len = len(queries)

    matrix = sh.get_matrix_history()[current]
    latex_matrix = sp.latex(string_list_to_matrix(matrix))
    matrix_rows = string_list_to_matrix(matrix).rows

    return render_template("interactive.html",
                           latex_matrix=latex_matrix,
                           current=current,
                           matrix_rows=matrix_rows, config=config,
                           matrices=matrices, queries=queries,
                           query_len=query_len)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)