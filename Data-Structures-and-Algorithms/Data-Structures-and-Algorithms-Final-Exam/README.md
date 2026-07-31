# English Version

## 1) Problem

Given an unweighted graph (undirected or directed):
1) Count the number of connected components.
2) Find the component(s) with the largest number of vertices.
3) Assume vertex labels are integers; count how many components have an even sum of vertex labels.
4) Among the components whose sum is even, pick the one with the largest even sum; count how many odd-labeled vertices it contains.

## 2) Files

In `Data-Structures-and-Algorithms`:
- `graph_dfs_homework.py`: adjacency list + a separate `dfs()` function + solutions for tasks 1–4
- `main.py`: reads input and prints results for each task

## 3) Input format

- Line 1: `n m`
- Next `m` lines: `u v`

Optional (legacy input): you may still provide an extra line `t` (0/1) after `n m`.
The program will **ignore** it and still process the graph as **undirected**.

Note: the program always processes the graph **as undirected** (it ignores edge directions if your input is directed).

### Undirected example
```
6 3
1 2
2 3
5 6
```

### Directed example
```
6 5
1 2
2 3
4 5
5 4
6 6
```

## 4) How to run (Windows PowerShell)

Open PowerShell in `CTDLVGT/Graph/`:

```powershell
python .\main.py
```

If you cannot type input when using VS Code **Run** (you get `EOFError`), create `input.txt` and run:

```powershell
Get-Content .\input.txt | python .\main.py
```

If you prefer the classic `< input.txt` redirection (CMD style):

```powershell
cmd /c "python .\main.py < input.txt"
```

---

# Vietnamese Version
## 1) Đề bài

Cho 1 đt ko có trọng số ( vô hướng hoặc có hướng)
1, đếm số thành phần liên thông
2, thành phần liên thông nào có số đỉnh nhiều nhất
3, gs tên đỉnh là các số nguyên, hỏi có bn tp liên thông có tổng số đỉnh là chẵn
4, đếm số pt lẻ trong thành phần có tổng chẵn lớn nhất

## 2) File trong thư mục

Trong `Data-Structures-and-Algorithms`:
- `graph_dfs_homework.py`: danh sách kề + hàm `dfs()` riêng + hàm giải 4 bài
- `main.py`: đọc input và in kết quả theo từng bài

## 3) Quy ước input (đơn giản)

Áp dụng cho cả vô hướng và có hướng.

- Dòng 1: `n m`
- `m` dòng tiếp: `u v`

Tùy chọn (input cũ): bạn có thể nhập thêm 1 dòng `t` (0/1) sau `n m`.
Chương trình sẽ **bỏ qua** dòng này và vẫn xử lý đồ thị **như vô hướng**.

Ghi chú: chương trình luôn xử lý đồ thị **như vô hướng** (nếu input là có hướng thì coi như bỏ hướng).

### Ví dụ vô hướng
```
6 3
1 2
2 3
5 6
```

### Ví dụ có hướng
```
6 5
1 2
2 3
4 5
5 4
6 6
```

## 4) Ý nghĩa các bài

- **Bài 1**: Đếm số thành phần liên thông.
- **Bài 2**: Thành phần liên thông có số đỉnh nhiều nhất.
- **Bài 3**: Đếm số thành phần có tổng nhãn đỉnh chẵn.
- **Bài 4**: Chọn thành phần có tổng nhãn chẵn lớn nhất, rồi đếm số đỉnh lẻ trong thành phần đó.

## 5) Cách chạy (Windows PowerShell)

Mở PowerShell tại `CTDLVGT/Graph/`:

```powershell
python .\main.py
```

Nếu bạn bấm **Run** trong VS Code mà không nhập được dữ liệu (bị lỗi `EOFError`), hãy tạo file `input.txt` rồi chạy theo cách redirect bên dưới.

Hoặc chạy bằng file input:

```powershell
Get-Content .\input.txt | python .\main.py
```

Nếu bạn muốn dùng cú pháp `< input.txt` (giống CMD), chạy:

```powershell
cmd /c "python .\main.py < input.txt"
```
