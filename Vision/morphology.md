모폴로지는 [이진 마스크](./binary_mask.md)를 집합으로 보고 침식·팽창으로 청소하는 연산군이다.

- **침식(erode)**: 흰 영역을 한 겹 깎는다 — 점 노이즈 제거, 물체도 작아짐
- **팽창(dilate)**: 흰 영역을 한 겹 불린다 — 구멍 메움, 물체도 커짐
- **열림(open)** = 침식→팽창: 바깥 점 노이즈 제거, 크기 보존
- **닫힘(close)** = 팽창→침식: 안쪽 구멍 메움, 크기 보존

실무 표준 순서는 **열림 → 닫힘**. 침식으로 없앤 점 노이즈를 팽창이 만회하려면 순서가 이래야 크기가 보존된다.

## 커널 모양 셋

```python
cv2.getStructuringElement(cv2.MORPH_RECT,    (5,5))  # 사각형 — 직선 경계
cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))  # 원형 — 기본값
cv2.getStructuringElement(cv2.MORPH_CROSS,   (5,5))  # 십자 — 얇은 선 보존
```

`iterations` 파라미터로 커널을 키우는 대신 같은 연산을 N번 반복할 수도 있다 — 결과 모양과 계산 비용이 다르다.

커널엔 **anchor(기준점)** 도 있다 — 어느 픽셀 자리에 계산 결과를 쓸지 정하는 점으로, 기본값은 커널 중심(`Point(-1,-1)`이 "중심"을 뜻하는 관례). 침식은 커널이 덮은 영역의 최솟값을, 팽창은 최댓값을 anchor 위치에 쓰는 것으로 정의된다.

## 열림·닫힘 너머

| 연산 | 정의 | 쓰는 곳 |
|---|---|---|
| `MORPH_GRADIENT` | 팽창 − 침식 | 물체 윤곽선만 추출 |
| `MORPH_TOPHAT` | 원본 − 열림 | 배경보다 밝은 작은 돌기 강조 |
| `MORPH_BLACKHAT` | 닫힘 − 원본 | 배경보다 어두운 작은 홈 강조 |

top-hat/black-hat은 그레이스케일 이미지에도 그대로 적용된다 — 조명이 화면 안에서 기울어진 경우(적응형 이진화가 푸는 문제)를 모폴로지로도 풀 수 있다.

## 뿌리는 광산학

수리형태학은 1964년 파리 광산학교(École des Mines)에서 태어났다 — Matheron은 **다공질 매체의 기하와 투과율의 관계**를, Serra는 **철광석 절편의 정량화(밀링 특성 예측용)** 를 각각 의뢰받아 연구하던 중, 그해 12월 Formery와 함께 이 접근을 "mathematical morphology"라 명명했다. 1968년엔 이 연구를 위해 Centre de Morphologie Mathématique가 세워졌다. 출발부터 이미지가 아니라 집합론(민코프스키 합·차)이었고, [이진 마스크](./binary_mask.md)가 집합 신분을 갖는 덕에 반세기 전 광산학 도구가 그대로 얹힌다.

---

출처:
- [Mathematical morphology — Wikipedia](https://en.wikipedia.org/wiki/Mathematical_morphology)
- [The birth of mathematical morphology (Matheron & Serra)](https://www.researchgate.net/publication/228805773_The_birth_of_mathematical_morphology)
- [OpenCV: Eroding and Dilating](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html)