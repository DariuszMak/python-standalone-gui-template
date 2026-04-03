/**
 * ClockController — mirrors src/ui/shared/controller/clock_controller.py
 *
 * Stores a start-time anchor and computes UNBOUNDED cumulative hand targets
 * on every update(), so the PID strategies never see a wrap discontinuity.
 */

import { calculateHandAngles, type ClockHands } from "./clockHelpers";
import { PIDMovementStrategy, type MovementStrategy } from "./strategies";

export class ClockController {
  /** Current smoothed hand positions (unbounded display units). */
  _clockHands: ClockHands = { second: 0, minute: 0, hour: 0 };

  private _startTime: Date;
  private readonly _strategies: [MovementStrategy, MovementStrategy, MovementStrategy];

  constructor(startTime: Date = new Date(0)) {
    this._startTime = startTime;
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
    const elapsedSeconds = (now.getTime() - this._startTime.getTime()) / 1000;
    const target = calculateHandAngles(this._startTime, elapsedSeconds);
    const [ss, sm, sh] = this._strategies;

    this._clockHands = {
      second: ss.update(this._clockHands.second, target.second),
      minute: sm.update(this._clockHands.minute, target.minute),
      hour: sh.update(this._clockHands.hour, target.hour),
    };
  }

  /**
   * Reset to a new start anchor and zero all hand positions and PID state.
   * Mirrors ClockController.reset() in clock_controller.py
   */
  reset(newStartTime: Date = new Date(0)): void {
    this._startTime = newStartTime;
    this._clockHands = { second: 0, minute: 0, hour: 0 };
    for (const strategy of this._strategies) {
      strategy.reset();
    }
  }
}
