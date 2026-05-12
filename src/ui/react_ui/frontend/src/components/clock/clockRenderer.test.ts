import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderClock } from "./clockRenderer";
import type { ClockHands } from "../clockHelpers";

function createMockContext(): CanvasRenderingContext2D {
  return {
    scale: vi.fn(),
    clearRect: vi.fn(),
    beginPath: vi.fn(),
    arc: vi.fn(),
    fill: vi.fn(),
    stroke: vi.fn(),
    moveTo: vi.fn(),
    lineTo: vi.fn(),
    fillText: vi.fn(),
    setTransform: vi.fn(),

    strokeStyle: "",
    fillStyle: "",
    lineWidth: 0,
    lineCap: "round",
    font: "",
    textAlign: "center",
    textBaseline: "middle",
  } as unknown as CanvasRenderingContext2D;
}

describe("renderClock", () => {
  let matchMediaSpy: ReturnType<typeof vi.spyOn>;

  beforeEach(() => {
    matchMediaSpy = vi.spyOn(window, "matchMedia").mockImplementation(
      () =>
        ({
          matches: false,
          addEventListener: vi.fn(),
          removeEventListener: vi.fn(),
        }) as MediaQueryList,
    );
  });

  afterEach(() => {
    matchMediaSpy.mockRestore();
  });

  it("renders without throwing", () => {
    const canvas = document.createElement("canvas");

    Object.defineProperty(canvas, "clientWidth", {
      value: 300,
    });

    Object.defineProperty(window, "devicePixelRatio", {
      value: 1,
      configurable: true,
    });

    const ctx = createMockContext();

    const hands: ClockHands = {
      second: 10,
      minute: 20,
      hour: 3,
    };

    expect(() => {
      renderClock(canvas, ctx, {
        hands,
        now: new Date(),
      });
    }).not.toThrow();
  });

  it("clears canvas before drawing", () => {
    const canvas = document.createElement("canvas");

    Object.defineProperty(canvas, "clientWidth", {
      value: 300,
    });

    const ctx = createMockContext();

    renderClock(canvas, ctx, {
      hands: {
        second: 1,
        minute: 1,
        hour: 1,
      },
      now: new Date(),
    });

    expect(ctx.clearRect).toHaveBeenCalled();
  });

  it("draws clock hands", () => {
    const canvas = document.createElement("canvas");

    Object.defineProperty(canvas, "clientWidth", {
      value: 300,
    });

    const ctx = createMockContext();

    renderClock(canvas, ctx, {
      hands: {
        second: 30,
        minute: 15,
        hour: 6,
      },
      now: new Date(),
    });

    expect(ctx.lineTo).toHaveBeenCalled();
    expect(ctx.stroke).toHaveBeenCalled();
  });

  it("draws time label", () => {
    const canvas = document.createElement("canvas");

    Object.defineProperty(canvas, "clientWidth", {
      value: 300,
    });

    const ctx = createMockContext();

    renderClock(canvas, ctx, {
      hands: {
        second: 0,
        minute: 0,
        hour: 0,
      },
      now: new Date(2025, 0, 1, 12, 34, 56, 789),
    });

    expect(ctx.fillText).toHaveBeenCalled();
  });

  it("handles dark mode", () => {
    matchMediaSpy.mockImplementation(
      () =>
        ({
          matches: true,
          addEventListener: vi.fn(),
          removeEventListener: vi.fn(),
        }) as MediaQueryList,
    );

    const canvas = document.createElement("canvas");

    Object.defineProperty(canvas, "clientWidth", {
      value: 300,
    });

    const ctx = createMockContext();

    expect(() => {
      renderClock(canvas, ctx, {
        hands: {
          second: 0,
          minute: 0,
          hour: 0,
        },
        now: new Date(),
      });
    }).not.toThrow();
  });
});
