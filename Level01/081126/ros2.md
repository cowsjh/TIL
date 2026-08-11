### loose coupling

- 발행자는 구독자가 몇인지 모른다
- 각 노드는 독립 적이다.
- 언어, 위치 무관하다.

간섭이 적은 만큼 어느 한 노드가 죽어도 영향이 적다.

### callback
- 순차 실행 방식이 아니라 event-driven 방식이다.
- 미리 등록해논 함수를 callback 한다.

| 콜백 종류 | 실행 시점 | 예시 |
|---|---|---|
| 구독 콜백 | 구독 중인 토픽에 메시지 도착 | `/scan` 도착 시 장애물 계산 |
| 타이머 콜백 | 정해진 주기마다 | 20ms마다 제어 명령 발행 |
| 서비스 콜백 | 다른 노드의 요청 수신 시 (11강) | — |
## tf2
로봇은 이동할때마다 자신의 base 좌표를 다시 계산 해야 하는데, ROS2 에서는 tf2 로 URDF 를 참조하여 좌표변환을 자동화한다.

tf2 는 3가지의 좌표 프레임을 계산한다. 월드, 객체, 타겟.
[Introducing tf2 — ROS 2 Documentation: Foxy documentation](https://docs.ros.org/en/foxy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html)
터틀 심의 예제를 보면 객체가 타겟을 따라간다. broadcaster 에서 객체의 좌표값을 받고 두 객체의 좌표 차이를 계산하여 따라가게 하는것이다.
![[Pasted image 20260811213316.png]]

3개의 좌표는 아래와 같은 방식으로 연결 된다.
![[Pasted image 20260811213611.png]]



### DDS: Data Distribution Service
데이터 분산 서비스의 줄임말

- 여러 컴퓨터를 자동으로 찾아 서로 연결, 통신 시켜주는 계층
- 특정 주기나 IP를 설정 하여 불필요한 간섭을 막을 수 있음.
- 여러 로봇을 컴퓨터 한대로 제어 가능

![[Pasted image 20260811215718.png]]
