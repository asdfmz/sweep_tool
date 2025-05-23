import sympy as sp
import config

def _adjust_index(i: int) -> int:
    """
    ユーザー入力に応じて index を変換（1-indexed → 0-indexed など）
    """
    return i - 1 if config.ONE_INDEXED else i

def _display_index(i: int) -> int:
    """
    ログ表示用のインデックスを変換（0-indexed → 1-indexed など）
    """
    return i + 1 if config.ONE_INDEXED else i

def apply_transformation(matrix: sp.Matrix, op: str, target: int, factor=None, other=None):
    """
    指定された基本変形を行列に適用する。
    Parameters:
        matrix (sp.Matrix): 現在の行列
        op (str): 操作の種類（"scale", "add", "swap"）
        target (int): 対象行番号（UI上の番号）
        factor: 定数倍や加算に使う係数（sympy型）
        other (int): 相手行番号（UI上の番号）
    Returns:
        matrix (sp.Matrix): 変形後の行列
        log (str): 履歴用の文字列
    """
    # index調整
    target_adj = _adjust_index(target)
    target_disp = _display_index(target_adj)
    if other is not None:
        other_adj = _adjust_index(other)
        other_disp = _display_index(other_adj)

    if op == "scale":
        matrix.row_op(target_adj, lambda x, _: factor * x)
        return matrix, f"R{target_disp} ← {factor} × R{target_disp}"

    elif op == "add":
        matrix.row_op(target_adj, lambda x, j: x + factor * matrix[other_adj, j])
        return matrix, f"R{target_disp} ← R{target_disp} + {factor} × R{other_disp}"

    elif op == "swap":
        matrix.row_swap(target_adj, other_adj)
        return matrix, f"R{target_disp} ⇄ R{other_disp}"

    else:
        raise ValueError(f"Unsupported operation: {op}")

def gaussian_elimination_steps(matrix):
    """
    掃き出し法を1ステップずつ実行し、
    [(matrix1, query1), (matrix2, query2), ...] の形で返す
    """
    steps = []
    m = matrix.copy()

    rows, cols = m.rows, m.cols
    pivot_row = 0

    for col in range(cols):
        if pivot_row >= rows:
            break

        # ピボットが0だったら下から探してswap
        if m[pivot_row, col] == 0:
            for r in range(pivot_row + 1, rows):
                if m[r, col] != 0:
                    m.row_swap(pivot_row, r)
                    steps.append((m.copy(), {"o": "w", "t": pivot_row + 1, "r": r + 1}))
                    break
            else:
                continue  # この列はスキップ

        # ピボットを1にする
        factor = m[pivot_row, col]
        if factor != 1:
            m.row_op(pivot_row, lambda x, _: x / factor)
            steps.append((m.copy(), {"o": "s", "t": pivot_row + 1, "f": str(1 / factor)}))

        # 他の行を消去
        for r in range(rows):
            if r != pivot_row and m[r, col] != 0:
                f = m[r, col]
                m.row_op(r, lambda x, j: x - f * m[pivot_row, j])
                steps.append((m.copy(), {"o": "a", "t": r + 1, "r": pivot_row + 1, "f": str(-f)}))

        pivot_row += 1

    return steps
