## 공유 방식 — 값 복사가 아니라 주소 공유

[command/state interface](./hardware_interface.md)는 데이터를 주고받지 않는다. 하드웨어 컴포넌트가 가진 **딱 한 벌의 숫자 칸**을 컨트롤러도 같이 가리키게 `double*`(= double 값 하나의 주소)를 넘기는 방식. 같은 메모리 셀을 둘이 함께 본다. ("double 포인터" = `double**`가 아니라 pointer-to-double.)

## 토픽 대신 포인터인 이유

read→update→write 루프는 한 프로세스(`controller_manager`) 안에서 100~1000Hz로 도는 실시간 루프. 토픽은 복사+직렬화+큐잉으로 지연이 붙는다. 컨트롤러와 하드웨어를 같은 프로세스에 넣고 **주소만 공유하면 복사 0회** — 실시간성 확보.

## 데이터 저장소 = 하드웨어 멤버 벡터

```cpp
std::vector<double> hw_states_;    // 서보에서 읽은 현재 위치(rad)
std::vector<double> hw_commands_;  // 컨트롤러가 원하는 목표 위치(rad)
```

이 벡터가 유일한 실데이터. export 함수는 복사가 아니라 **이 칸들의 주소를 배부**한다.

```cpp
std::vector<StateInterface> export_state_interfaces() {
  std::vector<StateInterface> ifaces;
  for (i ...) ifaces.emplace_back(
      StateInterface(joints[i].name, "position", &hw_states_[i])); // 값 아닌 주소
  return ifaces;
}
```

`StateInterface(이름, 종류, double* 주소)`는 주소만 품는다. command도 대칭으로 `&hw_commands_[i]`.

## 값이 흐르는 경로 (셀 하나 기준)

```
read()   : 서보 raw → raw2rad → hw_states_[0] 에 씀
컨트롤러 : state 포인터로 *(&hw_states_[0]) 읽음 → 계산 → command 포인터로 hw_commands_[0] 씀
write()  : hw_commands_[0] 읽어 rad2raw+clamp → 서보 전송
```

컨트롤러 `get_value()`는 자기 포인터를 역참조할 뿐 → read()가 방금 쓴 셀을 같은 자리에서 읽는다. **"전달" 행위 자체가 없다** — 처음부터 같은 셀을 본다.

## 두 가지 함의

- **순서가 정합성이다 (락 없음)**: `controller_manager`가 read→update→write를 한 스레드에서 순서대로 돌려 동시 접근이 없으므로 mutex 불필요 → 빠름. 반대로 **다른 스레드에서 `hw_states_`를 만지면 이 안전장치가 깨진다**(시리얼 read를 별도 스레드로 뺄 때 주의).
- **포인터 수명**: 컨트롤러가 잡은 주소는 컴포넌트 객체가 사는 동안만 유효. `hw_states_` 크기는 `on_init`에서 관절 수만큼 확정하고 **이후 resize·재할당 금지**(재할당 시 주소가 바뀌어 dangling).

## 버전 주의

위는 **Humble** 기준 raw `double*` 공유. Jazzy~ 이후는 스레드 안전성 위해 핸들을 더 감싼 구조로 변경됨.

---

출처: https://control.ros.org/humble/doc/getting_started/getting_started.html
