$$
G(s) = \frac{1}{s(Js+b)}
$$

어떤 입력을 넣으면 출력이 어떻게 나오는가?
ex)각도 2배 -> 소리 2배

$$
G(s)=\frac{출력(s)}{입력(s)}​
$$

하지만 현실 세계에서는 즉시 변하지 않는다. 관성 때문에 천천히 속도가 붙었다가 목표에 도달.
이 **시간에 따라 반응 하는 성질**은 상수로는 부족 하고 **전달 함수 $s$ 에 대한 식 으로 커진다.**

## 라플라스 변환

뉴턴 법칙 의 토크 법칙을 예로 들면,

$$
\underbrace{V}_{\text{내가 넣는 것}} \;=\; \underbrace{J\ddot{\theta}}_{\text{관성 돌리기}} \;+\; \underbrace{b\dot{\theta}}_{\text{마찰 이기기}}
$$
으로 볼 수 있다.
이때 미분을 적분해 주어야 답을 얻을 수 있기 때문에 번거로운데 라플라스 변환을 이용 하면 식을 쉽게 변형 할 수 있다.
$$
V = J\ddot{\theta} + b\dot{\theta}
\;\;\xrightarrow{\text{라플라스}}\;\;
V(s) = (Js^2 + bs)\,\theta(s)
$$

그후 우리는 $출력/입력$  꼴의 **전달 함수** 를 원하기 때문에

입력 : $전압 V$ 
출력 : $각도 \theta$
를 이용 하여 전달 함수 $G(s)$ 를 아래의 식으로 표현 할 수 있다.

$$
V(s) = (Js^2 + bs)\,\theta(s)
$$
$$
\frac{\theta(s)}{V(s)} = \frac{\theta(s)}{(Js^2 + bs)\theta(s)}
$$
$$
= \frac{1}{Js^2 + bs}
$$
$$
\Rightarrow\quad G(s) = \frac{1}{s(Js+b)}
$$
가 된다.

## 적용

### RC 회로 (전자)

저항 R과 축전기 C. 입력 전압 Vᵢₙ, 출력 전압 V_C:

$$
V_\text{in} = RC\,\dot{V}_C + V_C
\;\xrightarrow{\mathcal{L}}\;
G(s) = \frac{V_C(s)}{V_\text{in}(s)} = \frac{1}{RCs + 1}
$$

### 스프링-질량-댐퍼 (기계, 자동차 서스펜션)

질량 m, 스프링 k, 댐퍼(감쇠) c. 입력 힘 F, 출력 변위 x:

$$
F = m\ddot{x} + c\dot{x} + kx
\;\xrightarrow{\mathcal{L}}\;
G(s) = \frac{x(s)}{F(s)} = \frac{1}{ms^2 + cs + k}
$$

### DC 모터

$$
V = J\ddot{\theta} + b\dot{\theta}
\;\xrightarrow{\mathcal{L}}\;
G(s) = \frac{1}{Js^2 + bs}
$$

**수학적으로 완전히 똑같은 꼴**2차 다항식 분모).

$$
\underbrace{m\ddot{x} + c\dot{x} + kx}_{\text{기계}}
\quad\longleftrightarrow\quad
\underbrace{L\ddot{q} + R\dot{q} + \tfrac{1}{C}q}_{\text{전기(RLC 회로)}}
$$
## 조건


- **선형(Linear)**: θ², sin θ, x·ẋ 같은 **비선형 항이 없어야** 함. 미분/제곱 없이 항들이 곱하기·더하기로만 있어야 라플라스가 곱셈으로 깔끔하게 안 떨어짐.
- **시불변(Time-Invariant)**: 계수 J, b, m, k…가 **시간에 따라 변하지 않는 상수**여야 함.

이 둘을 합쳐 **LTI 시스템**이라 부르고, 전달 함수는 **LTI에만** 성립합니다.

### 어디서 깨지나

대표적으로 **진자(pendulum)**:

$$
\ddot{\theta} + \frac{g}{L}\sin\theta = 0
$$

여기 sin θ가 **비선형**이라 라플라스로 s 곱셈으로 못 바꿉니다. 이럴 땐 보통 "작은 각도에선 sin θ ≈ θ"로 **선형화(linearize)**해서 억지로 LTI로 만든 뒤 전달 함수를 씁니다. 로봇 제어에서 엄청 자주 하는 작업이에요 — 실제 로봇은 대부분 비선형인데, 동작점 근처에서 선형화해서 선형 제어이론을 적용하죠.