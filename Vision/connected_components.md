[이진 마스크](./binary_mask.md)는 "속하는가"만 답하고 "몇 개인가"는 답 못한다. 흰 픽셀을 서로 붙어있는 덩어리로 묶는 연산이 연결 성분 레이블링(connected component labeling)이다.

이웃 판정 기준은 둘 중 하나:

- **4-연결**: 상하좌우만 이웃
- **8-연결**: 대각선까지 이웃

`cv2.connectedComponents`가 마스크(지시함수, 값 0/1)를 레이블맵(덩어리마다 고유 번호)으로 바꾼다. "어디 있는가"에서 "몇 개, 어느 것인가"로 가는 다음 계단 — 마스크 하나에 물체가 여럿 섞여 있을 때 각각을 따로 다루려면 이 단계가 필요하다.

## 원리 — 2-pass + Union-Find

한 번의 스캔(raster scan, 왼쪽→오른쪽 위→아래)만으로는 안 된다. U자 모양 예시:

```
1 0 1
1 0 1
1 1 1
```

왼쪽 위부터 스캔하며 "이미 본 이웃(왼쪽·위)에 라벨 있으면 그걸 쓰고, 없으면 새 번호"로 채우면:

```
1 0 2
1 0 2
1 1 ?   ← 왼쪽=1, 위=2. 둘 다 이웃인데 라벨이 다르다
```

마지막 칸에서 충돌 발생 — 왼쪽 기둥과 오른쪽 기둥이 실은 바닥에서 이어진 한 덩어리인데, 스캔 순서상 아직 그 사실을 모른 채 각자 다른 임시 번호(1, 2)를 받은 것. 이게 1-pass로 안 되는 이유.

**1차 스캔**: 임시 라벨을 매기되, 충돌이 생기면 "1번과 2번은 사실 같다"를 **동치 테이블(equivalence table)** 에 적어둔다(`union(1, 2)`).
**2차 스캔**: 테이블을 따라 각 임시 라벨을 대표 라벨로 바꿔 쓴다(`find(2) → 1`).

동치 테이블의 실제 구현이 **Union-Find(Disjoint Set)** 자료구조다:

```python
parent = list(range(n))          # 처음엔 각자가 자기 대표

def find(x):                     # x가 속한 그룹의 대표를 찾는다
    while parent[x] != x:
        x = parent[x]
    return x

def union(a, b):                 # 두 그룹을 하나로 합친다
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb
```

`find`가 트리를 타고 올라가 뿌리(대표 라벨)를 반환하고, `union`이 두 트리를 하나로 붙인다. 2차 스캔에서 임시 라벨마다 `find()`를 불러 최종 번호로 바꾸면 끝.

대안으로 flood-fill(BFS/DFS로 이웃을 전부 따라가며 한 번에 라벨링)도 있다 — 개념은 더 직관적이지만 재귀 깊이·큐 관리 비용 때문에, 실무 라이브러리(OpenCV·scikit-image)는 스캔 한 줄씩 순차 접근이 가능한 2-pass 방식을 표준으로 쓴다.

---

출처: [Connected Components Labeling for Binary Images](https://www.researchgate.net/publication/336044568_CONNECTED_COMPONENT_LABELING_FOR_BINARY_IMAGES)
