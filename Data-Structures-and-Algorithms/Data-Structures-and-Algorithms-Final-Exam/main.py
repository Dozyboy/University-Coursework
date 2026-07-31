import sys

from graph_dfs_homework import get_components, solve_homework


def _readline_or_exit(message_when_no_input):
    try:
        return input()
    except EOFError:
        print(message_when_no_input)
        sys.exit(1)


def main():
    # [VI] Input đơn giản:
    #      Dòng 1: n m
    #      (Tùy chọn input cũ) Dòng 2: t (0/1) -> sẽ bị bỏ qua
    #      m dòng tiếp: u v
    # [EN] Simple input:
    #      Line 1: n m
    #      (Optional legacy input) Line 2: t (0/1) -> will be ignored
    #      Next m lines: u v

    interactive = sys.stdin.isatty()

    if interactive:
        print("[VI] Nhap theo format / [EN] Input format:")
        print("[VI] Dong 1: n m  / [EN] Line 1: n m")
        print("[VI] m dong tiep: u v  / [EN] Next m lines: u v")
        print("[VI] (Tuy chon input cu: co the co them 1 dong 't' (0/1) sau dong 1; chuong trinh se bo qua)")
        print("[EN] (Optional legacy input: you may add a single line 't' (0/1) after line 1; it will be ignored)")
        print()

    line1 = _readline_or_exit(
        "[VI] Khong co du lieu dau vao. Hay nhap input trong Terminal hoac dung: python .\\main.py < input.txt\n"
        "[EN] No input provided. Type input in the Terminal or use: python .\\main.py < input.txt"
    )
    n, m = map(int, line1.split())

    # [VI] Gộp chung: luôn xử lý đồ thị như vô hướng.
    #      Để tương thích input cũ: nếu dòng tiếp theo chỉ có 1 số 0/1 thì coi như 't' cũ và bỏ qua.
    # [EN] Unified: always process the graph as undirected.
    #      Backward compatibility: if the next line is a single 0/1, treat it as legacy 't' and ignore it.
    edges = []

    line2 = _readline_or_exit(
        "[VI] Thieu du lieu canh. Hay nhap m dong canh 'u v' sau dong 'n m'.\n"
        "[EN] Missing edges. Please enter m edge lines 'u v' after the 'n m' line."
    )
    parts = line2.split()
    if len(parts) == 1 and parts[0] in ("0", "1"):
        # [VI] Day la dong t cu -> bo qua
        # [EN] Legacy 't' line -> ignore
        pass
    else:
        # [VI] Day la canh dau tien
        # [EN] This is the first edge
        if len(parts) != 2:
            raise ValueError("[VI] Moi canh phai co dung 2 so: u v\n[EN] Each edge must have exactly 2 integers: u v")
        u, v = map(int, parts)
        edges.append((u, v))

    while len(edges) < m:
        line = _readline_or_exit(
            "[VI] Thieu canh 'u v'. Hay kiem tra so dong canh trong input.\n"
            "[EN] Missing an edge line 'u v'. Please check the number of edge lines in your input."
        )
        u, v = map(int, line.split())
        edges.append((u, v))

    components = get_components(n, edges)
    ans = solve_homework(components)

    print("[VI] DO THI (XU LY NHU VO HUONG) / [EN] GRAPH (PROCESSED AS UNDIRECTED)")
    print(f"n={n}, m={m}")
    print()

    print("[VI] BAI 1: Dem so thanh phan lien thong / [EN] TASK 1: Count connected components")
    print(ans["bai_1"])
    print()

    print("[VI] BAI 2: TP lien thong co so dinh nhieu nhat / [EN] TASK 2: Component(s) with the most vertices")
    print("[VI] Kich thuoc lon nhat / [EN] Max size:", ans["bai_2_max_size"])
    print("[VI] Cac thanh phan (ds dinh) / [EN] Component(s) (vertex lists):")
    for comp in ans["bai_2_components"]:
        print(" ", sorted(comp))
    print()

    print(
        "[VI] BAI 3: Co bao nhieu TP co tong nhan dinh chan / [EN] TASK 3: How many components have an even sum of labels"
    )
    print(ans["bai_3"])
    print()

    print(
        "[VI] BAI 4: Dem so dinh le trong TP co tong chan lon nhat / "
        "[EN] TASK 4: Count odd vertices in the even-sum component with the largest sum"
    )
    if ans["bai_4_sum_max"] is None:
        print("[VI] Khong co TP nao co tong nhan dinh chan.\n[EN] No component has an even sum of labels.")
        print(0)
    else:
        print("[VI] Tong chan lon nhat / [EN] Largest even sum:", ans["bai_4_sum_max"])
        print("[VI] So dinh le trong TP do / [EN] Odd vertices in that component:", ans["bai_4_odd_count"])
        print("[VI] TP do (ds dinh) / [EN] That component (vertex list):", sorted(ans["bai_4_component"]))


if __name__ == "__main__":
    main()
