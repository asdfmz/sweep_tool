from flask import session
from sympy_codec import matrix_to_string_list, string_list_to_matrix

def init_session(initial_matrix):
    """初期化：初期行列から履歴リストを作成し、セッションに保存"""
    session["m"] = [
        [initial_matrix],  # matrix_history
        [None],                                   # query_history
        0                                          # current_step
    ]

def get_current_step():
    return session["m"][2]

def get_current_matrix():
    step = get_current_step()
    return string_list_to_matrix(session["m"][0][step])

def get_matrix_history():
    return session["m"][0]

def get_query_history():
    return session["m"][1]

def append_step(matrix, query):
    """
    現在のステップ位置で履歴を切り詰め、次の行列とクエリを履歴に追加
    """
    step = get_current_step()
    matrix_hist = session["m"][0][:step + 1]
    query_hist = session["m"][1][:step + 1]

    matrix_hist.append(matrix_to_string_list(matrix))
    query_hist.append(query)

    session["m"] = [matrix_hist, query_hist, step + 1]

def step_back():
    step = get_current_step()
    if step > 0:
        session["m"] = [session["m"][0], session["m"][1], step - 1]

def step_forward():
    matrix_hist = session["m"][0]
    step = session["m"][2]
    if step + 1 < len(matrix_hist):
        session["m"] = [session["m"][0], session["m"][1], step + 1]

def step_to_start():
    session["m"] = [session["m"][0], session["m"][1], 0]

def step_to_end():
    session["m"] = [session["m"][0], session["m"][1], len(session["m"][0]) - 1]

def generate_log(query):
    """
    queryオブジェクトからログ文字列を生成（短縮構造対応）
    """
    if not query:
        return "初期状態"
    op = query["o"]
    t = query["t"]
    f = query.get("f")
    r = query.get("r")

    if op == "s":
        return f"R{t} ← {f} × R{t}"
    elif op == "a":
        return f"R{t} ← R{t} + {f} × R{r}"
    elif op == "w":
        return f"R{t} ⇄ R{r}"
    else:
        return "不明な操作"
