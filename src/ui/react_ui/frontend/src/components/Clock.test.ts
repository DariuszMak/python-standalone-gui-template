import { describe, it, expect } from "vitest";
import { PID, calculateHandAngles, polarToCartesian, formatTime } from "./Clock";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Build a UTC Date without any local-timezone offset influencing the result. */
function utc(h: number, m: number, s: number, ms = 0): Date {
  return new Date(Date.UTC(2025, 3, 27, h, m, s, ms)); // month is 0-indexed
}

// ---------------------------------------------------------------------------
// PID
// ---------------------------------------------------------------------------

describe("PID", () => {
  it("first update applies kp, ki, kd correctly", () => {
    const pid = new PID(1.0, 0.1, 0.5);
    // error=1, integral=1, derivative=1-0=1  →  1*1 + 0.1*1 + 0.5*1 = 1.6
    expect(pid.update(1.0)).toBeCloseTo(1.6);
  });

  it("second update uses accumulated integral and previous error", () => {
    const pid = new PID(1.0, 0.1, 0.5);
    pid.update(1.0);
    const out = pid.update(0.5);
    // error=0.5, integral=1.5, derivative=0.5-1.0=-0.5
    // 1*0.5 + 0.1*1.5 + 0.5*(-0.5) = 0.5 + 0.15 - 0.25 = 0.4
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
});

// ---------------------------------------------------------------------------
// calculateHandAngles
// Note: calculateHandAngles uses local time (getHours etc.), so we construct
// dates via Date.UTC and rely on the test runner using UTC (TZ=UTC in CI) or
// we derive expected values from the same Date methods — making tests
// timezone-agnostic.
// ---------------------------------------------------------------------------

describe("calculateHandAngles", () => {
  it("midnight gives all zeros", () => {
    const dt = utc(0, 0, 0);
    const h = calculateHandAngles(dt);
    expect(h.second).toBeCloseTo(0);
    expect(h.minute).toBeCloseTo(0);
    expect(h.hour).toBeCloseTo(0);
  });

  it("noon gives all zeros (12-hour wrap)", () => {
    const dt = utc(12, 0, 0);
    const h = calculateHandAngles(dt);
    expect(h.second).toBeCloseTo(0);
    expect(h.minute).toBeCloseTo(0);
    expect(h.hour).toBeCloseTo(0);
  });

  it("half past three", () => {
    const dt = utc(3, 30, 0);
    const h = calculateHandAngles(dt);
    expect(h.second).toBeCloseTo(0);
    expect(h.minute).toBeCloseTo(30);
    expect(h.hour).toBeCloseTo(3.5);
  });

  it("23:59:59 maximum hand positions", () => {
    const dt = utc(23, 59, 59);
    const h = calculateHandAngles(dt);
    expect(h.second).toBeCloseTo(59);
    expect(h.minute).toBeCloseTo(59 + 59 / 3600, 4); // ~59.9833…
    expect(h.hour).toBeCloseTo(11 + (59 * 60 + 59) / 3600, 4); // ~11.9997…
  });

  it("milliseconds contribute to smoothness", () => {
    const dt_0ms = utc(0, 0, 30, 0);
    const dt_500ms = utc(0, 0, 30, 500);
    const h0 = calculateHandAngles(dt_0ms);
    const h500 = calculateHandAngles(dt_500ms);
    expect(h500.second).toBeGreaterThan(h0.second);
  });

  it("second hand equals total-seconds mod 60", () => {
    const dt = utc(1, 2, 3);
    const h = calculateHandAngles(dt);
    const localH = dt.getHours() % 12;
    const total = localH * 3600 + dt.getMinutes() * 60 + dt.getSeconds();
    expect(h.second).toBeCloseTo(total % 60);
  });

  it("minute hand equals total-seconds/60 mod 60", () => {
    const dt = utc(2, 45, 10);
    const h = calculateHandAngles(dt);
    const localH = dt.getHours() % 12;
    const total = localH * 3600 + dt.getMinutes() * 60 + dt.getSeconds();
    expect(h.minute).toBeCloseTo((total / 60) % 60, 5);
  });

  it("hour hand equals total-seconds/3600 mod 12", () => {
    const dt = utc(7, 15, 0);
    const h = calculateHandAngles(dt);
    const localH = dt.getHours() % 12;
    const total = localH * 3600 + dt.getMinutes() * 60 + dt.getSeconds();
    expect(h.hour).toBeCloseTo((total / 3600) % 12, 5);
  });
});

// ---------------------------------------------------------------------------
// polarToCartesian
// ---------------------------------------------------------------------------

describe("polarToCartesian", () => {
  it("angle 0 points straight up (north)", () => {
    const [x, y] = polarToCartesian(100, 100, 50, 0);
    expect(x).toBeCloseTo(100);
    expect(y).toBeCloseTo(50); // cy - length
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
    expect(y).toBeCloseTo(60); // 80 - 20
  });
});

// ---------------------------------------------------------------------------
// formatTime
// ---------------------------------------------------------------------------

describe("formatTime", () => {
  it("formats HH:MM:SS.mmm from a UTC date", () => {
    // Build a date whose *local* fields match what we want to assert.
    // We read back via the same getHours/getMinutes/getSeconds methods
    // the implementation uses, so the test is tz-agnostic.
    const dt = utc(3, 4, 5, 678);
    const result = formatTime(dt);
    const hh = String(dt.getHours()).padStart(2, "0");
    const mm = String(dt.getMinutes()).padStart(2, "0");
    const ss = String(dt.getSeconds()).padStart(2, "0");
    expect(result).toBe(`${hh}:${mm}:${ss}.678`);
  });

  it("pads single-digit fields with zeros", () => {
    const dt = utc(1, 2, 3, 4);
    const result = formatTime(dt);
    expect(result).toMatch(/^\d{2}:\d{2}:\d{2}\.\d{3}$/);
    expect(result.endsWith(".004")).toBe(true);
  });

  it("milliseconds are floored, not rounded", () => {
    const dt = utc(0, 0, 0, 999);
    const result = formatTime(dt);
    expect(result.endsWith(".999")).toBe(true);
  });
});
