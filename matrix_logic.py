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
