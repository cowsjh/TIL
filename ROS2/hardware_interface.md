**컨트롤러가 하드웨어를 몰라도 되게** 하드웨어 마다 다른 부분을 `SystemInterface` 를 통해 전부 번역 하고, **컨트롤러는 표준 슬롯(state/commands) 만 보게 하는** 전략

> **NOTE — 컨트롤러가 수많은 하드웨어 의 차이들을 몰라도 명령을 내릴 수 있게 통역 해주는 계층**


## 필요한 이유

컨트롤러로 로봇이 움직이는 큰 두 단계는 

1. 컨트롤러: 어떻게 움직일지 계산
2. 하드웨어: 현재 상태 에 적용

로 이루어져 있다.
하지만 2번은 하드웨어마다 방법이 완전히 다르기 때문에 이를 통역 해 주지 않는 다면 컨트롤러가 명령을 내릴 수 없다.

그래서 ros2_control은 둘 사이에 체계(interface)를 하나 만든다.
컨트롤러와 하드웨어는 그 체계를 사이에 두고 서로 소통 하는데 그 체계가 `hardware_interface` 이고 하드웨어 쪽 통역사가 C++의 `SystemInterface` 플러그인이다.

## state / command

데이터가 오가는데 interface는 두종류가 존재 한다. 항상 주체가 되는 **컨트롤러** 를 기준으로 짜여져 있다.

| 종류                    | 방향               | SO-101에서          |
| --------------------- | ---------------- | ----------------- |
| **state_interface**   | 하드웨어 → 컨트롤러 (읽기) | 서보 현재 위치를 rad로 보고 |
| **command_interface** | 컨트롤러 → 하드웨어 (쓰기) | 컨트롤러가 원하는 rad 명령  |

state·command 각각이 하드웨어와 컨트롤러 사이에서 [같은 메모리를 공유한다.](./ros2_control_interface_memory.md)
### 컴포넌트 타입

하드웨어도 크게 3가지로 분류한다.
- System - 읽기, 쓰기 다 하는 다관절 로봇 
	- *so-101이  system 이고 URDF에* `type="system"` 라고 명시됨
- Actuator - 쓰기 위주 단일 모터
- Sensor - 읽기만 (IMU, 등 센서)

### read / write 루프

`controller_manager` 는 고정 주기로 사이클을 계속 돈다. 콜백 큐에 쌓아두고 나중에 처리하는 이벤트 구동이 아니라, 주기로 맞춘 순차 루프 이다. - **동기, 단일 스레드**

```
read()  →  서보 raw 위치 읽어 state_interface에 채움
   ↓
컨트롤러 update()  →  목표와 비교해 command_interface에 새 명령 씀
   ↓
write() →  command_interface 값을 raw로 바꿔 서보로 전송
   ↓  (반복)
```

## controller_manager

ros2 에서 **기본으로 컴파일이 되어있는 프로그램**.
`pluginlib` [을 이용](./pluginlib.md)해 아래의 방법으로 하드웨어의 멤버와 함수에 접근한다.

1. 기계어를 메모리에 불러오기
	- `colcon build` 시 클래스는 `..._hardware.so` 라는 공유 라이브러리 파일로 나온다. OS 에는 실행 중에 이런 `.so` 를 통째로 메모리에 얹는 기능이 있다.
2. 그 메모리 안에서 원하는 클래스를 골라 객체를 만든다.
	- `.so` 안에서 어느 함수가 객체를 만드는 함수인지 알아낸다.

### 클래스 상속 + 다형성(polymorphism)

`controller_manager`는 현재 하드웨어 클래스는 몰라도, **부모인 `SystemInterface`는 알고있다.** 

```cpp
SystemInterface* h = <공장에서 받아온 객체>;   // 부모 타입 포인터로만 잡음
h->read();    // 실제로는 SO101의 read()가 불림
```

포인터 타입은 부모`SystemInterface`지만, 실제 객체는 **자식은 커스텀 클래스**라 `read()`를 부르면 C++이 vtable를 보고 자식의 `read()`로 알아서 연결해준다.

