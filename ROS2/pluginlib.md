## 풀려는 문제

이미 컴파일된 남의 [프로그램](./hardware_interface.md)(`controller_manager` 등)이, 그때 존재하지도 않던 내 클래스의 객체를 **문자열 이름 하나**(`so101_hardware/SO101SystemHardware`)로 생성하는 것. 일반 C++은 `#include`+링크로 빌드 시점에 대상을 확정하므로 불가능.

## 두 축 — 동적 로드 + 공통 부모

- **동적 로드**: 클래스는 빌드 시 `.so`(shared object)로 나오고, OS의 `dlopen`으로 실행 중에 메모리에 얹는다. `dl` = dynamic loading.
- **공통 부모 + 다형성**: 모든 플러그인이 같은 부모(`hardware_interface::SystemInterface`)를 상속하도록 강제. `controller_manager`는 부모 타입 포인터로만 잡고 `h->read()`를 호출 → **vtable이 실제 자식 구현으로 연결**. 알맹이를 몰라도 부모 얼굴만 알면 됨.

## `PLUGINLIB_EXPORT_CLASS` — 이름을 알 수 있는 공장 심기

C++ name mangling 탓에 `.so` 안 함수를 `dlsym`으로 찾을 심볼명을 예측할 수 없다. 이 매크로가 **약속된 심볼의 factory 함수**를 자동 생성해 `.so`에 심는다 → pluginlib가 그걸 호출해 `new` 대신 객체를 만들어 부모 포인터로 반환.

```cpp
#include <pluginlib/class_list_macros.hpp>
PLUGINLIB_EXPORT_CLASS(so101_hardware::SO101SystemHardware,
                       hardware_interface::SystemInterface)
```

## 전화번호부 — plugin description xml

문자열 → 어느 `.so`·어느 클래스인지 매핑하는 등록부. `package.xml`의 `<export>`에 걸어 ament 색인에 올려야 pluginlib가 발견.

```xml
<library path="so101_hardware">
  <class name="so101_hardware/SO101SystemHardware"
         type="so101_hardware::SO101SystemHardware"
         base_class_type="hardware_interface::SystemInterface"/>
</library>
```

## 전체 흐름

```
URDF <plugin> 문자열
 → plugin.xml 조회(어느 .so·클래스)
 → dlopen(.so) → PLUGINLIB_EXPORT_CLASS factory 호출
 → SystemInterface* 반환 → on_init()/read()/write() (vtable로 실제 구현 연결)
```

## 세 곳 문자열 일치가 철칙인 이유

URDF `<plugin>`(조회 키) · plugin.xml `name=` · C++ `namespace::class`+매크로 — 전부 이 조회의 키라서 하나만 어긋나도 "그런 이름 없음"으로 로드 실패. 로직 이전에 이 배선 일치가 첫 관문.

## 적용 범위

ros2_control 하드웨어 컴포넌트 전용이 아니라 **ROS2 플러그인 생태계 전반**(컨트롤러, 센서, RViz 플러그인, Nav2 behavior/planner)이 동일 메커니즘.

---

출처: https://docs.ros.org/en/humble/p/pluginlib/
