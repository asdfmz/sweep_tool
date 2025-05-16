import sympy as sp

def parse_matrix(form_data, rows, cols):
    data = []
    for i in range(rows):
        row = []
        for j in range(cols):
            value = form_data.get(f"cell_{i}_{j}", "0")
            row.append(sp.sympify(value))  # 数式や分数対応
        data.append(row)
    return sp.Matrix(data)

def compute_rref(matrix):
    rref, _ = matrix.rref()
    return rref