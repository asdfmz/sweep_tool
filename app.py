from flask import Flask, render_template, request
from sympy import Matrix
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        try:
            rows = []
            for i in range(3):
                row_str = request.form[f"row{i}"]
                row = [eval(x) for x in row_str.split(",")]
                rows.append(row)
            mat = Matrix(rows)
            rref_mat, _ = mat.rref()
            result = str(rref_mat)
        except Exception as e:
            result = f"エラー：{e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)