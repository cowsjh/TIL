엔코더와 IMU는 둘 다 로봇 자기 자신의 움직임만 재는 proprioceptive 센서다. 이 둘로만 위치를 구하는 것
-  [odom→base_link](./odom.md) 구간이 바로 이 방식으로 계산되며, proprioceptive 센서만으로는 오차가 무한정 누적된다.
- 바퀴가 미끄러지면 "이만큼 굴렀다"고 세지만 실제로는 그만큼 안 움직였다.
- IMU도 [자이로 적분](./imu_gyro_quaternion.md) 특성상 시간이 지나면 오차가 쌓인다.
