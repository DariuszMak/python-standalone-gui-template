/**
 * ClockController — mirrors src/ui/shared/controller/clock_controller.py
 *
 * Owns the three PID movement strategies and the current ClockHands state.
 * Consumers call update() each frame and read _clockHands for rendering.
 */

import { calculateHandAngles, type ClockHands } from "./clockHelpers";
import { PIDMovementStrategy, type MovementStrategy } from "./strategies";

export class ClockController {
  /** Current smoothed hand positions (display units). */
  _clockHands: ClockHands = { second: 0, minute: 0, hour: 0 };

  private readonly _strategies: [MovementStrategy, MovementStrategy, MovementStrategy];

  constructor() {
    this._strategies = [
      new PIDMovementStrategy(0.15, 0.005, 0.005), // second
      new PIDMovementStrategy(0.08, 0.004, 0.004), // minute
      new PIDMovementStrategy(0.08, 0.002, 0.002), // hour
    ];
  }

  /**
   * Advance hand positions toward the target angles for `now`.
   * Mirrors ClockController.update() in clock_controller.py
   */
  update(now: Date): void {
    const target = calculateHandAngles(now);
    const [ss, sm, sh] = this._strategies;

    this._clockHands = {
      second: ss.update(this._clockHands.second, target.second),
      minute: sm.update(this._clockHands.minute, target.minute),
      hour: sh.update(this._clockHands.hour, target.hour),
    };
  }

  /**
   * Reset hand positions and PID state.
   * Mirrors ClockController.reset() in clock_controller.py
   */
  reset(): void {
    this._clockHands = { second: 0, minute: 0, hour: 0 };
    for (const strategy of this._strategies) {
      strategy.reset();
    }
  }
}
