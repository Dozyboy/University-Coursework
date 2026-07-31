"""[VI] Đỉnh được đánh số từ 1..n.
[EN] Vertices are labeled from 1..n.

[VI] Với đồ thị có hướng: để giữ bài ở mức DFS cơ bản, ta xét "liên thông yếu"
    (bỏ hướng các cạnh) rồi tìm thành phần liên thông như đồ thị vô hướng.
[EN] For a directed graph: to keep the DFS solution basic, we use "weak connectivity"
    (ignore edge directions) and then find connected components like an undirected graph.
"""


def build_adj(n, edges, directed=False):
    """[VI] Tạo danh sách kề.
    [EN] Build an adjacency list.

    [VI] directed=False  -> vô hướng
        directed=True   -> có hướng (nhưng khi làm liên thông yếu, ta vẫn thêm 2 chiều)
    [EN] directed=False  -> undirected
        directed=True   -> directed (but for weak connectivity we still add both directions)
    """

    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        # [VI] Gộp chung: mặc định xử lý như vô hướng (bỏ hướng cạnh)
        # [EN] Unified: process as undirected by default (ignore edge direction)
        adj[v].append(u)
    return adj


def dfs(start, adj, visited):
    """[VI] DFS (dùng stack) trả về danh sách các đỉnh trong 1 thành phần.
    [EN] DFS (stack-based) returns the list of vertices in one component.
    """

    stack = [start]
    visited[start] = True
    comp = []

    while stack:
        u = stack.pop()
        comp.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)

    return comp


def get_components(n, edges, directed=False):
    """[VI] Lấy các thành phần liên thông.
    [EN] Get connected components.

    [VI] - Vô hướng: DFS trực tiếp
        - Có hướng: liên thông yếu -> bỏ hướng cạnh (thêm cả 2 chiều) rồi DFS
    [EN] - Undirected: run DFS directly
        - Directed: weak connectivity -> ignore directions (add both directions), then DFS
    """

    # [VI] Gộp chung: luôn tính thành phần liên thông như đồ thị vô hướng
    #      (nếu input là có hướng thì cũng coi như bỏ hướng)
    # [EN] Unified: always compute components as in an undirected graph
    #      (if the input is directed, we still ignore directions)
    adj = build_adj(n, edges, directed=False)

    visited = [False] * (n + 1)
    components = []
    for v in range(1, n + 1):
        if not visited[v]:
            components.append(dfs(v, adj, visited))
    return components


def solve_homework(components):
    """[VI] Trả về kết quả 4 bài (dùng đúng DFS ở trên).
    [EN] Return results for the 4 tasks (using the DFS above).
    """

    # [VI] Bài 1: số thành phần liên thông
    # [EN] Task 1: number of connected components
    bai_1 = len(components)

    # [VI] Bài 2: thành phần có số đỉnh nhiều nhất
    # [EN] Task 2: component(s) with the largest number of vertices
    max_size = 0
    for comp in components:
        if len(comp) > max_size:
            max_size = len(comp)
    bai_2_components = [comp for comp in components if len(comp) == max_size]

    # [VI] Bài 3: đếm số TP có tổng nhãn đỉnh chẵn
    # [EN] Task 3: count components whose sum of vertex labels is even
    bai_3 = 0
    even_sum_components = []
    for comp in components:
        s = sum(comp)
        if s % 2 == 0:
            bai_3 += 1
            even_sum_components.append(comp)

    # [VI] Bài 4: trong các TP có tổng chẵn, lấy TP có tổng lớn nhất, đếm số đỉnh lẻ
    # [EN] Task 4: among even-sum components, pick the one with the largest sum and count odd vertices
    if not even_sum_components:
        bai_4_sum_max = None
        bai_4_odd_count = 0
        bai_4_comp = []
    else:
        bai_4_comp = even_sum_components[0]
        bai_4_sum_max = sum(bai_4_comp)
        for comp in even_sum_components[1:]:
            s = sum(comp)
            if s > bai_4_sum_max:
                bai_4_sum_max = s
                bai_4_comp = comp

        bai_4_odd_count = 0
        for x in bai_4_comp:
            if x % 2 != 0:
                bai_4_odd_count += 1

    return {
        "bai_1": bai_1,
        "bai_2_max_size": max_size,
        "bai_2_components": bai_2_components,
        "bai_3": bai_3,
        "bai_4_sum_max": bai_4_sum_max,
        "bai_4_odd_count": bai_4_odd_count,
        "bai_4_component": bai_4_comp,
    }


# [VI] Dữ liệu mẫu (input cũ có dòng `t`):
# [EN] Sample input (legacy with `t` line):
# 8 5
# 0
# 1 2
# 2 3
# 4 5
# 6 7
# 7 8

# [VI] Dữ liệu mẫu (input cũ có dòng `t`):
# [EN] Sample input (legacy with `t` line):
# 8 6
# 1
# 1 2
# 2 3
# 4 5
# 5 4
# 6 7
# 8 8
