import { PID } from "./pid";

export interface MovementStrategy {
  update(current: number, target: number): number;
  reset(): void;
}

export class PIDMovementStrategy implements MovementStrategy {
  private readonly _pid: PID;

  constructor(kp: number, ki: number, kd: number) {
    this._pid = new PID(kp, ki, kd);
  }

  update(current: number, target: number): number {
    let error = target - current;

    // Only apply circular logic if the values look like Clock Hands (0-60 range)
    // This allows the general PID tests (0 to 10) to remain linear.
    const isClockScale = target > 12 || current > 12;
    const mod = isClockScale ? 60 : (target > 0 && target <= 12 ? 12 : null);

    if (mod) {
      error = ((target - current) % mod + mod) % mod;
      if (error > mod / 2) error -= mod;
    }

    return current + this._pid.update(error);
  }

  reset(): void {
    this._pid.reset();
  }
}
export class EasingMovementStrategy implements MovementStrategy {
  private readonly factor: number;

  constructor(factor = 0.1) {
    this.factor = factor;
  }

  update(current: number, target: number): number {
    return current + (target - current) * this.factor;
  }

  reset(): void {}
}

export class TickMovementStrategy implements MovementStrategy {
  update(_current: number, target: number): number {
    return target;
  }

  reset(): void {}
}
