
## 정의

$$\sigma(x) = \frac{1}{1+e^{-x}}$$

예: $x=0 \Rightarrow \sigma(0)=0.5$. $x\to+\infty \Rightarrow e^{-x}\to0 \Rightarrow \sigma(x)\to1$.
$x\to-\infty \Rightarrow e^{-x}\to\infty \Rightarrow \sigma(x)\to0$. 즉 **입력을 무엇을 넣든
0과 1 사이로 눌러 담는 함수** — 분모의 $e^{-x}$가 지수함수이므로
[[지수법칙 Laws of Exponents]]가 그대로 적용된다.

## 왜 이름이 "시그모이드"인가

그리스 문자 시그마($\sigma$, sigma)의 옛 형태를 뜻하는 *sigmoeides*("S자 모양의")에서
왔다 — 그래프가 완만한 S자 곡선이기 때문. 아래로 볼록하다가 위로 볼록하게
바뀌는 변곡점이 $x=0$에 있다.

## 왜 ML에서 쓰는가

출력이 항상 $(0,1)$ 사이라서 **"확률"처럼 해석**할 수 있다.

- **로지스틱 회귀**: 선형식 $w^Tx+b$의 결과를 시그모이드에 통과시켜 "클래스 1일
  확률"로 변환. `가능도 likelihood.md`에서 다루는 우도 개념과 이어짐.
- **신경망 활성함수**: 뉴런의 출력을 0~1로 제한. 다만 입력이 크거나 작을 때
  기울기가 0에 가까워지는 vanishing gradient 문제 때문에 은닉층에서는
  ReLU 계열이 더 흔히 쓰이고, 시그모이드는 주로 출력층(이진 분류)에 남아있다.

## 미분이 자기 자신으로 표현되는 성질

$$\sigma'(x) = \sigma(x)\bigl(1-\sigma(x)\bigr)$$

$e^x$의 미분이 자기 자신이 되는 성질([[로그법칙 Laws of Logarithms]] 참고)이
분모에 들어있기 때문에, 시그모이드도 도함수를 함수 자기 자신만으로 다시 쓸 수
있다 — 역전파(backpropagation) 계산이 간단해지는 이유.

## 연결

- 곡선 형태 자체는 그래픽스의 S자 커브(smoothstep)와 같은 계열 —
  [[쉐이핑 함수 Shaping Functions]] (0~1 구간을 다듬는다는 용도가 같음, 다만
  시그모이드는 정의역이 전체 실수라 입력을 0~1로 "눌러 담는" 데 특화)
