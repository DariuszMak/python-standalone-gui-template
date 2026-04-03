import { describe, it, expect } from "vitest";

// Import from canonical modules directly (mirrors Python test imports from shared/)
import { PID } from "./pid";
import {
  PIDMovementStrategy,
  EasingMovementStrategy,
  TickMovementStrategy,
} from "./strategies";
import {
  calculateHandAngles,
  clockHandsInRadians,
  polarToCartesian,
  formatTime,
  type ClockHands,
} from "./clockHelpers";
import { ClockController } from "./clockController";

// Also verify that clockUtils re-exports everything (backwards compatibility)
import {
  PID as PIDFromUtils,
  PIDMovementStrategy as PIDStrategyFromUtils,
  calculateHandAngles as calcFromUtils,
  polarToCartesian as polarFromUtils,
  formatTime as formatFromUtils,
  ClockController as ControllerFromUtils,
} from "./clockUtils";

function localDate(h: number, m: number, s: number, ms = 0): Date {
  const now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), now.getDate(), h, m, s, ms);
}

// ---------------------------------------------------------------------------
// PID
// ---------------------------------------------------------------------------
describe("PID", () => {
  it("first update applies kp, ki, kd correctly", () => {
    const pid = new PID(1.0, 0.1, 0.5);
    expect(pid.update(1.0)).toBeCloseTo(1.6);
  });

  it("second update uses accumulated integral and previous error", () => {
    const pid = new PID(1.0, 0.1, 0.5);
    pid.update(1.0);
    const out = pid.update(0.5);
    expect(out).toBeCloseTo(0.4);
  });

  it("reset zeroes internal state", () => {
    const pid = new PID(1.0, 0.1, 0.5);
    pid.update(1.0);
    pid.update(0.5);
    expect(pid._integral).not.toBe(0);
    expect(pid._prevError).not.toBe(0);
    pid.reset();
    expect(pid._integral).toBe(0);
    expect(pid._prevError).toBe(0);
  });

  it("after reset the same input gives the same result as first call", () => {
    const pid = new PID(0.1, 0.1, 0.0);
    const first = pid.update(5.0);
    pid.update(3.0);
    pid.reset();
    expect(pid.update(5.0)).toBeCloseTo(first);
  });

  it("re-exported from clockUtils is the same class", () => {
    expect(new PIDFromUtils(1, 0, 0).update(2)).toBeCloseTo(new PID(1, 0, 0).update(2));
  });
});

// ---------------------------------------------------------------------------
// Movement strategies
// ---------------------------------------------------------------------------
describe("PIDMovementStrategy", () => {
  it("moves current toward target", () => {
    const s = new PIDMovementStrategy(0.1, 0, 0);
    const v1 = s.update(0, 10);
    expect(v1).toBeGreaterThan(0);
    const v2 = s.update(v1, 10);
    expect(v2).toBeGreaterThan(v1);
  });

  it("reset causes same output as first call", () => {
    const s = new PIDMovementStrategy(0.1, 0.1, 0);
    const first = s.update(0, 10);
    s.update(5, 10);
    s.reset();
    expect(s.update(0, 10)).toBeCloseTo(first);
  });

  it("re-exported from clockUtils works identically", () => {
    const a = new PIDMovementStrategy(0.15, 0.005, 0.005);
    const b = new PIDStrategyFromUtils(0.15, 0.005, 0.005);
    expect(a.update(0, 30)).toBeCloseTo(b.update(0, 30));
  });
});

describe("EasingMovementStrategy", () => {
  it("moves fractionally toward target", () => {
    const s = new EasingMovementStrategy(0.2);
    expect(s.update(0, 10)).toBeCloseTo(2.0);
    expect(s.update(5, 15)).toBeCloseTo(7.0);
  });

  it("factor 1.0 snaps directly to target", () => {
    expect(new EasingMovementStrategy(1.0).update(3, 10)).toBeCloseTo(10);
  });

  it("factor 0.0 stays at current", () => {
    expect(new EasingMovementStrategy(0.0).update(3, 10)).toBeCloseTo(3);
  });

  it("reset is a no-op (stateless)", () => {
    const s = new EasingMovementStrategy(0.5);
    s.reset(); // must not throw
    expect(s.update(0, 10)).toBeCloseTo(5);
  });
});

describe("TickMovementStrategy", () => {
  it("snaps immediately to target", () => {
    const s = new TickMovementStrategy();
    expect(s.update(5, 20)).toBeCloseTo(20);
    expect(s.update(-10, -3.5)).toBeCloseTo(-3.5);
  });
});

// ---------------------------------------------------------------------------
// calculateHandAngles
// ---------------------------------------------------------------------------
describe("calculateHandAngles", () => {
  it("midnight gives all zeros", () => {
    const h = calculateHandAngles(localDate(0, 0, 0));
    expect(h.second).toBeCloseTo(0);
    expect(h.minute).toBeCloseTo(0);
    expect(h.hour).toBeCloseTo(0);
  });

  it("noon gives all zeros (12-hour wrap)", () => {
    const h = calculateHandAngles(localDate(12, 0, 0));
    expect(h.second).toBeCloseTo(0);
    expect(h.minute).toBeCloseTo(0);
    expect(h.hour).toBeCloseTo(0);
  });

  it("half past three", () => {
    const h = calculateHandAngles(localDate(3, 30, 0));
    expect(h.second).toBeCloseTo(0);
    expect(h.minute).toBeCloseTo(30);
    expect(h.hour).toBeCloseTo(3.5);
  });

  it("23:59:59 maximum hand positions", () => {
    const dt = localDate(23, 59, 59);
    const h = calculateHandAngles(dt);
    const localH = dt.getHours() % 12;
    const total = localH * 3600 + dt.getMinutes() * 60 + dt.getSeconds();
    expect(h.second).toBeCloseTo(total % 60, 4);
    expect(h.minute).toBeCloseTo((total / 60) % 60, 4);
    expect(h.hour).toBeCloseTo((total / 3600) % 12, 4);
  });

  it("milliseconds contribute to smoothness", () => {
    const dt0 = localDate(0, 0, 30, 0);
    const dt500 = localDate(0, 0, 30, 500);
    expect(calculateHandAngles(dt500).second).toBeGreaterThan(calculateHandAngles(dt0).second);
  });

  it("second hand equals total-seconds mod 60", () => {
    const dt = localDate(1, 2, 3);
    const localH = dt.getHours() % 12;
    const total = localH * 3600 + dt.getMinutes() * 60 + dt.getSeconds();
    expect(calculateHandAngles(dt).second).toBeCloseTo(total % 60);
  });

  it("minute hand equals total-seconds/60 mod 60", () => {
    const dt = localDate(2, 45, 10);
    const localH = dt.getHours() % 12;
    const total = localH * 3600 + dt.getMinutes() * 60 + dt.getSeconds();
    expect(calculateHandAngles(dt).minute).toBeCloseTo((total / 60) % 60, 5);
  });

  it("hour hand equals total-seconds/3600 mod 12", () => {
    const dt = localDate(7, 15, 0);
    const localH = dt.getHours() % 12;
    const total = localH * 3600 + dt.getMinutes() * 60 + dt.getSeconds();
    expect(calculateHandAngles(dt).hour).toBeCloseTo((total / 3600) % 12, 5);
  });

  it("PM hour wraps correctly: 15:30 same as 3:30", () => {
    const am = localDate(3, 30, 0);
    const pm = localDate(15, 30, 0);
    expect(calculateHandAngles(pm).hour).toBeCloseTo(calculateHandAngles(am).hour, 5);
    expect(calculateHandAngles(pm).minute).toBeCloseTo(calculateHandAngles(am).minute, 5);
  });

  it("re-exported from clockUtils produces identical results", () => {
    const dt = localDate(9, 15, 30, 250);
    const a = calculateHandAngles(dt);
    const b = calcFromUtils(dt);
    expect(a.second).toBeCloseTo(b.second);
    expect(a.minute).toBeCloseTo(b.minute);
    expect(a.hour).toBeCloseTo(b.hour);
  });
});

// ---------------------------------------------------------------------------
// clockHandsInRadians
// ---------------------------------------------------------------------------
describe("clockHandsInRadians", () => {
  it("zero hands give zero radians", () => {
    const r = clockHandsInRadians({ second: 0, minute: 0, hour: 0 });
    expect(r.second).toBeCloseTo(0);
    expect(r.minute).toBeCloseTo(0);
    expect(r.hour).toBeCloseTo(0);
  });

  it("30 seconds → π radians (half circle)", () => {
    const r = clockHandsInRadians({ second: 30, minute: 0, hour: 0 });
    expect(r.second).toBeCloseTo(Math.PI);
  });

  it("30 minutes → π radians (half circle)", () => {
    const r = clockHandsInRadians({ second: 0, minute: 30, hour: 0 });
    expect(r.minute).toBeCloseTo(Math.PI);
  });

  it("6 hours → π radians (half circle)", () => {
    const r = clockHandsInRadians({ second: 0, minute: 0, hour: 6 });
    expect(r.hour).toBeCloseTo(Math.PI);
  });

  it("15 seconds → π/2 radians (quarter circle)", () => {
    const r = clockHandsInRadians({ second: 15, minute: 0, hour: 0 });
    expect(r.second).toBeCloseTo(Math.PI / 2);
  });

  it("full second circle (60 s) → 2π", () => {
    const r = clockHandsInRadians({ second: 60, minute: 0, hour: 0 });
    expect(r.second).toBeCloseTo(2 * Math.PI);
  });

  it("full hour circle (12 h) → 2π", () => {
    const r = clockHandsInRadians({ second: 0, minute: 0, hour: 12 });
    expect(r.hour).toBeCloseTo(2 * Math.PI);
  });

  it("mirrors Python clock_hands_in_radians formula", () => {
    const hands: ClockHands = { second: 15, minute: 30, hour: 6 };
    const r = clockHandsInRadians(hands);
    expect(r.second).toBeCloseTo((15 / 60) * 2 * Math.PI);
    expect(r.minute).toBeCloseTo((30 / 60) * 2 * Math.PI);
    expect(r.hour).toBeCloseTo((6 / 12) * 2 * Math.PI);
  });
});

// ---------------------------------------------------------------------------
// polarToCartesian
// ---------------------------------------------------------------------------
describe("polarToCartesian", () => {
  it("angle 0 points straight up (north)", () => {
    const [x, y] = polarToCartesian(100, 100, 50, 0);
    expect(x).toBeCloseTo(100);
    expect(y).toBeCloseTo(50);
  });

  it("angle π/2 points right (east)", () => {
    const [x, y] = polarToCartesian(0, 0, 1, Math.PI / 2);
    expect(x).toBeCloseTo(1);
    expect(y).toBeCloseTo(0);
  });

  it("angle π points straight down (south)", () => {
    const [x, y] = polarToCartesian(0, 0, 10, Math.PI);
    expect(x).toBeCloseTo(0, 5);
    expect(y).toBeCloseTo(10, 5);
  });

  it("angle 3π/2 points left (west)", () => {
    const [x, y] = polarToCartesian(0, 0, 1, (3 * Math.PI) / 2);
    expect(x).toBeCloseTo(-1);
    expect(y).toBeCloseTo(0, 5);
  });

  it("respects center offset", () => {
    const [x, y] = polarToCartesian(50, 80, 20, 0);
    expect(x).toBeCloseTo(50);
    expect(y).toBeCloseTo(60);
  });

  it("re-exported from clockUtils produces identical results", () => {
    const a = polarToCartesian(100, 100, 50, Math.PI / 4);
    const b = polarFromUtils(100, 100, 50, Math.PI / 4);
    expect(a[0]).toBeCloseTo(b[0]);
    expect(a[1]).toBeCloseTo(b[1]);
  });
});

// ---------------------------------------------------------------------------
// formatTime
// ---------------------------------------------------------------------------
describe("formatTime", () => {
  it("formats HH:MM:SS.mmm using local time fields", () => {
    const dt = localDate(3, 4, 5, 678);
    const result = formatTime(dt);
    const hh = String(dt.getHours()).padStart(2, "0");
    const mm = String(dt.getMinutes()).padStart(2, "0");
    const ss = String(dt.getSeconds()).padStart(2, "0");
    expect(result).toBe(`${hh}:${mm}:${ss}.678`);
  });

  it("pads single-digit fields with zeros", () => {
    const dt = localDate(1, 2, 3, 4);
    const result = formatTime(dt);
    expect(result).toMatch(/^\d{2}:\d{2}:\d{2}\.\d{3}$/);
    expect(result.endsWith(".004")).toBe(true);
  });

  it("milliseconds are floored, not rounded", () => {
    const dt = localDate(0, 0, 0, 999);
    expect(formatTime(dt).endsWith(".999")).toBe(true);
  });

  it("re-exported from clockUtils produces identical result", () => {
    const dt = localDate(8, 30, 15, 123);
    expect(formatFromUtils(dt)).toBe(formatTime(dt));
  });
});

// ---------------------------------------------------------------------------
// ClockController
// ---------------------------------------------------------------------------
describe("ClockController", () => {
  it("starts with all hands at zero", () => {
    const c = new ClockController();
    expect(c._clockHands).toEqual({ second: 0, minute: 0, hour: 0 });
  });

  it("update advances hands from zero toward target", () => {
    const c = new ClockController();
    c.update(localDate(3, 30, 45));
    const { second, minute, hour } = c._clockHands;
    expect(second).toBeGreaterThan(0);
    expect(minute).toBeGreaterThan(0);
    expect(hour).toBeGreaterThan(0);
  });

  it("repeated updates converge hands toward target", () => {
    const c = new ClockController();
    const target = calculateHandAngles(localDate(6, 0, 0));
    let prev = { ...c._clockHands };

    for (let i = 0; i < 50; i++) {
      c.update(localDate(6, 0, 0));
      const curr = c._clockHands;
      // Hour hand must be getting closer (or equal) each tick
      expect(Math.abs(target.hour - curr.hour)).toBeLessThanOrEqual(
        Math.abs(target.hour - prev.hour) + 1e-9,
      );
      prev = { ...curr };
    }
  });

  it("reset zeroes all hands", () => {
    const c = new ClockController();
    c.update(localDate(12, 30, 45));
    c.reset();
    expect(c._clockHands).toEqual({ second: 0, minute: 0, hour: 0 });
  });

  it("after reset, same first update gives same result as a fresh controller", () => {
    const c1 = new ClockController();
    const c2 = new ClockController();
    const dt = localDate(9, 15, 0);

    c1.update(dt);
    c2.update(localDate(3, 0, 0)); // different first call
    c2.reset();
    c2.update(dt);

    expect(c1._clockHands.second).toBeCloseTo(c2._clockHands.second, 10);
    expect(c1._clockHands.minute).toBeCloseTo(c2._clockHands.minute, 10);
    expect(c1._clockHands.hour).toBeCloseTo(c2._clockHands.hour, 10);
  });

  it("re-exported from clockUtils is the same class", () => {
    const c = new ControllerFromUtils();
    c.update(localDate(1, 2, 3));
    expect(c._clockHands.second).toBeGreaterThan(0);
  });

  it("clockHandsInRadians applied to controller output stays within [0, 2π]", () => {
    const c = new ClockController();
    for (let h = 0; h < 12; h++) {
      c.reset();
      for (let i = 0; i < 20; i++) {
        c.update(localDate(h, h * 4, h * 3));
      }
      const r = clockHandsInRadians(c._clockHands);
      // Values should be non-negative (hands can only move forward from 0)
      expect(r.second).toBeGreaterThanOrEqual(0);
      expect(r.minute).toBeGreaterThanOrEqual(0);
      expect(r.hour).toBeGreaterThanOrEqual(0);
    }
  });
});
