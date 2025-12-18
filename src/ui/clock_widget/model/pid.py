from __future__ import annotations


class PID:
    def __init__(self, kp: float = 0.0, ki: float = 0.0, kd: float = 0.0) -> None:
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        self.prev_error = 0.0
        self.integral = 0.0

    def update(self, error: float) -> float:
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

    def pid_reset(self) -> None:
        self.prev_error = 0.0
        self.integral = 0.0
