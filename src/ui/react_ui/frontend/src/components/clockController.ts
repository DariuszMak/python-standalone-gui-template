import { calculateHandAngles, getShortestInterval, type ClockHands } from "./clockHelpers";
import { PIDMovementStrategy, type MovementStrategy } from "./strategies";

export class ClockController {
  _clockHands: ClockHands = { second: 0, minute: 0, hour: 0 };

  private _startTime: Date;
  private readonly _strategies: [MovementStrategy, MovementStrategy, MovementStrategy];

  constructor(startTime: Date = new Date(0)) {
    this._startTime = startTime;
    this._strategies = [
      new PIDMovementStrategy(0.15, 0.005, 0.005),
      new PIDMovementStrategy(0.08, 0.004, 0.004),
      new PIDMovementStrategy(0.08, 0.002, 0.002),
    ];
  }


  update(now: Date): void {
    const elapsedSeconds = (now.getTime() - this._startTime.getTime()) / 1000;
    const target = calculateHandAngles(this._startTime, elapsedSeconds);
    const [ss, sm, sh] = this._strategies;

    // We apply the PID to the "shortest delta" 
    // This prevents the hands from spinning backwards at the 12 o'clock jump
    this._clockHands = {
      second: this._clockHands.second + ss.update(getShortestInterval(this._clockHands.second, target.second, 60)),
      minute: this._clockHands.minute + sm.update(getShortestInterval(this._clockHands.minute, target.minute, 60)),
      hour: this._clockHands.hour + sh.update(getShortestInterval(this._clockHands.hour, target.hour, 12)),
    };

  reset(newStartTime: Date = new Date(0)): void {
    this._startTime = newStartTime;
    this._clockHands = { second: 0, minute: 0, hour: 0 };
    for (const strategy of this._strategies) {
      strategy.reset();
    }
  }
}
