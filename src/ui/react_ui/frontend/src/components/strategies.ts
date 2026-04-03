/**
 * Movement strategies — mirrors src/ui/shared/model/strategies/
 *
 * MovementStrategy      → movement_strategy.py
 * PIDMovementStrategy   → pid_strategy.py
 * EasingMovementStrategy → easing_strategy.py
 * TickMovementStrategy  → tick_strategy.py
 */

import { PID } from "./pid";

export interface MovementStrategy {
  update(current: number, target: number): number;
  reset(): void;
}

/**
 * Mirrors PIDMovementStrategy in pid_strategy.py
 */
export class PIDMovementStrategy implements MovementStrategy {
  private readonly _pid: PID;

  constructor(kp: number, ki: number, kd: number) {
    this._pid = new PID(kp, ki, kd);
  }

  update(current: number, target: number): number {
    const error = target - current;
    return current + this._pid.update(error);
  }

  reset(): void {
    this._pid.reset();
  }
}

/**
 * Mirrors EasingMovementStrategy in easing_strategy.py
 */
export class EasingMovementStrategy implements MovementStrategy {
  private readonly factor: number;

  constructor(factor = 0.1) {
    this.factor = factor;
  }

  update(current: number, target: number): number {
    return current + (target - current) * this.factor;
  }

  reset(): void {
    // stateless — nothing to reset
  }
}

/**
 * Mirrors TickMovementStrategy in tick_strategy.py
 */
export class TickMovementStrategy implements MovementStrategy {
  update(_current: number, target: number): number {
    return target;
  }

  reset(): void {
    // stateless — nothing to reset
  }
}
