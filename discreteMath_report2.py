# relation_equivalence_kor.py
# 작성자: (빌렉자르갈 / 20213008)

from typing import List

A = [1, 2, 3, 4, 5]

# 1. 관계행렬 입력
def read_matrix(n: int = 5) -> List[List[int]]:
    R = []
    print(f"{n}×{n} 관계행렬을 입력하세요 (각 행은 공백으로 구분된 0 또는 1 다섯 개):")
    for i in range(n):
        row = input(f"{i+1}행: ").strip().split()
        if len(row) != n:
            raise ValueError(f"각 행에는 반드시 {n}개의 숫자가 있어야 합니다.")
        R.append([int(x) for x in row])
    return R

# 2. 관계의 성질 판별
def is_reflexive(R: List[List[int]]) -> bool:
    return all(R[i][i] == 1 for i in range(len(R)))

def is_symmetric(R: List[List[int]]) -> bool:
    n = len(R)
    for i in range(n):
        for j in range(n):
            if R[i][j] != R[j][i]:
                return False
    return True

def is_transitive(R: List[List[int]]) -> bool:
    n = len(R)
    for i in range(n):
        for j in range(n):
            if R[i][j]:
                for k in range(n):
                    if R[j][k] and not R[i][k]:
                        return False
    return True

# 3. 폐포 계산
def reflexive_closure(R: List[List[int]]) -> List[List[int]]:
    n = len(R)
    C = [row[:] for row in R]
    for i in range(n):
        C[i][i] = 1
    return C

def symmetric_closure(R: List[List[int]]) -> List[List[int]]:
    n = len(R)
    C = [row[:] for row in R]
    for i in range(n):
        for j in range(n):
            if R[i][j] == 1 or R[j][i] == 1:
                C[i][j] = 1
                C[j][i] = 1
    return C

def transitive_closure(R: List[List[int]]) -> List[List[int]]:
    n = len(R)
    C = [row[:] for row in R]
    for k in range(n):
        for i in range(n):
            if C[i][k]:
                for j in range(n):
                    if C[k][j]:
                        C[i][j] = 1
    return C

# 4. 보조 함수
def matrix_to_str(R: List[List[int]]) -> str:
    return "\n".join(" ".join(str(x) for x in row) for row in R)

def check_equivalence(R: List[List[int]]):
    r = is_reflexive(R)
    s = is_symmetric(R)
    t = is_transitive(R)
    return r, s, t, (r and s and t)

def equivalence_classes(R: List[List[int]]) -> List[List[int]]:
    n = len(R)
    visited = [False] * n
    classes = []
    for i in range(n):
        if not visited[i]:
            comp = []
            stack = [i]
            visited[i] = True
            while stack:
                u = stack.pop()
                comp.append(u + 1)
                for v in range(n):
                    if R[u][v] == 1 and R[v][u] == 1 and not visited[v]:
                        visited[v] = True
                        stack.append(v)
            classes.append(sorted(comp))
    classes.sort(key=lambda x: x[0])
    return classes

# 5. 출력 함수
def print_relation_report(R: List[List[int]], title: str):
    print("=" * 50)
    print(f"▶ {title}")
    print("-" * 50)
    print(matrix_to_str(R))
    print("-" * 50)
    r, s, t, eq = check_equivalence(R)
    print(f"반사적?   {'예' if r else '아니오'}")
    print(f"대칭적?   {'예' if s else '아니오'}")
    print(f"추이적?   {'예' if t else '아니오'}")
    print(f"⇒ 동치 관계인가?  {'예' if eq else '아니오'}")
    if eq:
        print("동치류:")
        for cls in equivalence_classes(R):
            print(f"   [{', '.join(map(str, cls))}]")
    print()

# 6. 메인 실행부
def main():
    R = read_matrix(5)
    print_relation_report(R, "입력된 관계 R")

    r, s, t, eq = check_equivalence(R)

    if not r:
        RC = reflexive_closure(R)
        print_relation_report(RC, "반사적 폐포(Reflexive Closure)")
    else:
        RC = R

    if not s:
        SC = symmetric_closure(R)
        print_relation_report(SC, "대칭적 폐포(Symmetric Closure)")
    else:
        SC = R

    if not t:
        TC = transitive_closure(R)
        print_relation_report(TC, "추이적 폐포(Transitive Closure)")
    else:
        TC = R

    # 모든 폐포를 적용한 최종 동치폐포
    R_equiv = transitive_closure(symmetric_closure(reflexive_closure(R)))
    print_relation_report(R_equiv, "최종 동치폐포 (Equivalence Closure = T(S(R_reflexive)))")

# 7. 실행 시작
if __name__ == "__main__":
    main()
