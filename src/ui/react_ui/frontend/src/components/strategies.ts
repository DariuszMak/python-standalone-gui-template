import { PID } from "./pid";

export interface MovementStrategy {
  update(current: number, target: number): number;
  reset(): void;
}

// .\components\strategies.ts

export class PIDMovementStrategy implements MovementStrategy {
  private readonly _pid: PID;

  constructor(kp: number, ki: number, kd: number) {
    this._pid = new PID(kp, ki, kd);
  }

  update(current: number, target: number): number {
    // 1. Determine if we are tracking 60 (sec/min) or 12 (hours)
    const mod = target <= 12.1 && current <= 12.1 ? 12 : 60;

    // 2. Calculate the shortest error on a circle
    let error = (target - current) % mod;
    if (error > mod / 2) error -= mod;
    if (error < -mod / 2) error += mod;

    // 3. Return the new position
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
