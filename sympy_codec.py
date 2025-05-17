# sympy_codec.py

import sympy as sp
from typing import List

def matrix_to_string_list(matrix: sp.Matrix) -> List[List[str]]:
    """
    SymPyの行列を list[list[str]] に変換（セッション保存用）
    """
    return [[str(cell) for cell in row] for row in matrix.tolist()]

def string_list_to_matrix(string_list: List[List[str]]) -> sp.Matrix:
    """
    list[list[str]] を SymPyの行列に復元
    """
    return sp.Matrix([[sp.sympify(cell) for cell in row] for row in string_list])

if __name__ == "__main__":
    m = sp.Matrix([[1, 1/3], [sp.sqrt(2), sp.I + 2]])
    print("元の行列：", m)

    data = matrix_to_string_list(m)
    print("保存用データ：", data)

    recovered = string_list_to_matrix(data)
    print("復元行列：", recovered)