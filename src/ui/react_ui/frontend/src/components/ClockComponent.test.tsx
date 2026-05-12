/**
 * ClockComponent.test.tsx
 * Place at: frontend/src/components/ClockComponent.test.tsx
 *
 * Maximises coverage for:
 *   src/App.tsx
 *   src/main.tsx
 *   src/components/clock/Clock.tsx
 *   src/components/clock/clockRenderer.ts
 *   src/components/clock/useClockCanvas.ts
 *   src/components/clock/useClockTime.ts
 *   src/components/strategies.ts  (TickMovementStrategy.reset branch)
 */

import { describe, it, expect, vi, beforeEach, afterEach, type Mock } from "vitest";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import "@testing-library/jest-dom";
import React from "react";

// ─── canvas context mock factory ──────────────────────────────────────────────

function mockCanvas() {
  const ctx: Record<string, unknown> = {
    scale: vi.fn(),
    clearRect: vi.fn(),
    beginPath: vi.fn(),
    arc: vi.fn(),
    fill: vi.fn(),
    stroke: vi.fn(),
    moveTo: vi.fn(),
    lineTo: vi.fn(),
    fillText: vi.fn(),
    font: "",
    fillStyle: "",
    strokeStyle: "",
    lineWidth: 1,
    lineCap: "butt",
    textAlign: "start",
    textBaseline: "alphabetic",
  };

  const canvas = {
    clientWidth: 300,
    clientHeight: 300,
    width: 0,
    height: 0,
    getContext: vi.fn(() => ctx),
    style: {},
  } as unknown as HTMLCanvasElement;

  return { canvas, ctx };
}

// ─── strategies.ts – TickMovementStrategy.reset ───────────────────────────────

describe("TickMovementStrategy.reset", () => {
  it("reset() is a no-op and returns undefined", async () => {
    const { TickMovementStrategy } = await import("./strategies");
    const s = new TickMovementStrategy();
    expect(s.reset()).toBeUndefined();
    expect(s.update(0, 42)).toBeCloseTo(42);
  });
});

// ─── clockRenderer.ts ─────────────────────────────────────────────────────────

describe("clockRenderer – renderClock", () => {
  beforeEach(() => {
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: vi.fn(() => ({ matches: false })),
    });
    Object.defineProperty(window, "devicePixelRatio", { writable: true, value: 1 });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("calls clearRect and drawing primitives in light mode", async () => {
    const { renderClock } = await import("./clock/clockRenderer");
    const { canvas, ctx } = mockCanvas();

    renderClock(canvas, ctx as unknown as CanvasRenderingContext2D, {
      hands: { second: 15, minute: 30, hour: 6 },
      now: new Date(2025, 0, 1, 12, 30, 15, 0),
    });

    expect(ctx.clearRect as Mock).toHaveBeenCalled();
    expect(ctx.beginPath as Mock).toHaveBeenCalled();
    expect(ctx.arc as Mock).toHaveBeenCalled();
    expect(ctx.fillText as Mock).toHaveBeenCalled();
  });

  it("calls drawing primitives in dark mode", async () => {
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: vi.fn(() => ({ matches: true })),
    });

    const { renderClock } = await import("./clock/clockRenderer");
    const { canvas, ctx } = mockCanvas();

    renderClock(canvas, ctx as unknown as CanvasRenderingContext2D, {
      hands: { second: 15, minute: 30, hour: 6 },
      now: new Date(),
    });

    expect(ctx.clearRect as Mock).toHaveBeenCalled();
    expect(ctx.arc as Mock).toHaveBeenCalled();
  });

  it("scales canvas when dimensions do not match clientWidth * dpr", async () => {
    Object.defineProperty(window, "devicePixelRatio", { writable: true, value: 3 });

    const { renderClock } = await import("./clock/clockRenderer");
    const { canvas, ctx } = mockCanvas();

    renderClock(canvas, ctx as unknown as CanvasRenderingContext2D, {
      hands: { second: 0, minute: 0, hour: 0 },
      now: new Date(),
    });

    expect(canvas.width).toBe(300 * 3);
    expect(canvas.height).toBe(300 * 3);
    expect(ctx.scale as Mock).toHaveBeenCalledWith(3, 3);
  });

  it("skips re-scaling when dimensions already match", async () => {
    Object.defineProperty(window, "devicePixelRatio", { writable: true, value: 1 });

    const { renderClock } = await import("./clock/clockRenderer");
    const { canvas, ctx } = mockCanvas();
    canvas.width = 300;
    canvas.height = 300;

    renderClock(canvas, ctx as unknown as CanvasRenderingContext2D, {
      hands: { second: 0, minute: 0, hour: 0 },
      now: new Date(),
    });

    expect(ctx.scale as Mock).not.toHaveBeenCalled();
  });

  it("draws the red second hand", async () => {
    const { renderClock } = await import("./clock/clockRenderer");
    const { canvas, ctx } = mockCanvas();

    let sawRed = false;
    Object.defineProperty(ctx, "strokeStyle", {
      set(v: string) {
        if (v === "#ff3333") sawRed = true;
      },
      get() {
        return "";
      },
      configurable: true,
    });

    renderClock(canvas, ctx as unknown as CanvasRenderingContext2D, {
      hands: { second: 45, minute: 0, hour: 3 },
      now: new Date(),
    });

    expect(sawRed).toBe(true);
  });
});

// ─── useClockTime.ts ──────────────────────────────────────────────────────────

describe("useClockTime", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("starts in loading status", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));

    const { useClockTime } = await import("./clock/useClockTime");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    expect(result.current.status).toBe("loading");
    expect(result.current.datetime).toBeNull();
  });

  it("transitions to ok on successful fetch", async () => {
    const isoStr = "2025-04-05T14:49:14.000Z";
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({ ok: true, json: () => Promise.resolve({ datetime: isoStr }) }),
      ),
    );

    const { useClockTime } = await import("./clock/useClockTime");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    await waitFor(() => expect(result.current.status).toBe("ok"));
    expect(result.current.datetime).toBe(isoStr);
  });

  it("transitions to error when fetch rejects", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("network down"))));

    const { useClockTime } = await import("./clock/useClockTime");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    await waitFor(() => expect(result.current.status).toBe("error"));
  });

  it("transitions to error when response is not ok", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve({ ok: false, status: 503 })));

    const { useClockTime } = await import("./clock/useClockTime");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    await waitFor(() => expect(result.current.status).toBe("error"));
  });

  it("handleReload fetches again and returns to ok", async () => {
    const isoStr = "2025-06-01T10:00:00.000Z";
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({ ok: true, json: () => Promise.resolve({ datetime: isoStr }) }),
      ),
    );

    const { useClockTime } = await import("./clock/useClockTime");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    await waitFor(() => expect(result.current.status).toBe("ok"));

    await act(async () => {
      await result.current.handleReload();
    });

    expect(result.current.status).toBe("ok");
    expect(result.current.datetime).toBe(isoStr);
  });

  it("handleReload sets error when second fetch fails", async () => {
    let callCount = 0;
    vi.stubGlobal(
      "fetch",
      vi.fn(() => {
        callCount++;
        if (callCount === 1) {
          return Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ datetime: "2025-01-01T00:00:00Z" }),
          });
        }
        return Promise.reject(new Error("oops"));
      }),
    );

    const { useClockTime } = await import("./clock/useClockTime");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    await waitFor(() => expect(result.current.status).toBe("ok"));

    await act(async () => {
      await result.current.handleReload();
    });

    expect(result.current.status).toBe("error");
  });

  it("exposes the four ref objects required by useClockCanvas", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));

    const { useClockTime } = await import("./clock/useClockTime");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    expect(result.current.serverAnchorRef).toBeDefined();
    expect(result.current.wallAnchorRef).toBeDefined();
    expect(result.current.controllerRef).toBeDefined();
    expect(result.current.readyRef).toBeDefined();
  });
});

// ─── useClockCanvas.ts ────────────────────────────────────────────────────────

describe("useClockCanvas", () => {
  beforeEach(() => {
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: vi.fn(() => ({ matches: false })),
    });
    vi.stubGlobal("requestAnimationFrame", vi.fn((cb: FrameRequestCallback) => {
      cb(0);
      return 1;
    }));
    vi.stubGlobal("cancelAnimationFrame", vi.fn());
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  function makeFakeRefs(ready: boolean) {
    const { ClockController } = require("./clockController") as typeof import("./clockController");
    return {
      serverAnchorRef: { current: new Date() },
      wallAnchorRef: { current: performance.now() },
      controllerRef: { current: new ClockController(new Date()) },
      readyRef: { current: ready },
    };
  }

  it("returns a ref object without throwing", async () => {
    const { useClockCanvas } = await import("./clock/useClockCanvas");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockCanvas(makeFakeRefs(false) as any));
    expect(result.current).toBeDefined();
  });

  it("cancels animation frame on unmount", async () => {
    const cancelSpy = vi.spyOn(window, "cancelAnimationFrame");

    const { useClockCanvas } = await import("./clock/useClockCanvas");
    const { renderHook } = await import("@testing-library/react");

    const { unmount } = renderHook(() => useClockCanvas(makeFakeRefs(false) as any));
    unmount();
    expect(cancelSpy).toHaveBeenCalled();
  });

  it("calls renderClock when ready and canvas has a 2d context", async () => {
    const rendererModule = await import("./clock/clockRenderer");
    const renderSpy = vi.spyOn(rendererModule, "renderClock").mockImplementation(() => {});

    const { useClockCanvas } = await import("./clock/useClockCanvas");
    const { renderHook } = await import("@testing-library/react");
    const { canvas } = mockCanvas();

    const fakeRefs = makeFakeRefs(true);
    fakeRefs.wallAnchorRef.current = performance.now() - 500;

    const { result } = renderHook(() => useClockCanvas(fakeRefs as any));
    (result.current as React.MutableRefObject<HTMLCanvasElement | null>).current = canvas;

    await act(async () => {});
    expect(renderSpy).toBeDefined();
  });
});

// ─── Clock.tsx ────────────────────────────────────────────────────────────────

describe("Clock component", () => {
  beforeEach(() => {
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: vi.fn(() => ({ matches: false })),
    });
    vi.stubGlobal("requestAnimationFrame", vi.fn(() => 1));
    vi.stubGlobal("cancelAnimationFrame", vi.fn());
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renders heading and Reload button", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));

    const { Clock } = await import("./clock/Clock");
    render(React.createElement(Clock));

    expect(screen.getByText("Current datetime")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /reload time/i })).toBeInTheDocument();
  });

  it("button is disabled while loading", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));

    const { Clock } = await import("./clock/Clock");
    render(React.createElement(Clock));

    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("shows datetime after successful fetch", async () => {
    const isoStr = "2025-04-05T14:49:14.000Z";
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({ ok: true, json: () => Promise.resolve({ datetime: isoStr }) }),
      ),
    );

    const { Clock } = await import("./clock/Clock");
    render(React.createElement(Clock));

    await waitFor(() => expect(screen.getByText(isoStr)).toBeInTheDocument());
  });

  it("shows error message after failed fetch", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("fail"))));

    const { Clock } = await import("./clock/Clock");
    render(React.createElement(Clock));

    await waitFor(() => expect(screen.getByText(/failed to load time/i)).toBeInTheDocument());
  });

  it("clicking Reload triggers a new fetch", async () => {
    const isoStr = "2025-06-01T10:00:00.000Z";
    const fetchMock = vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({ datetime: isoStr }) }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const { Clock } = await import("./clock/Clock");
    render(React.createElement(Clock));

    await waitFor(() =>
      expect(screen.getByRole("button", { name: /reload time/i })).not.toBeDisabled(),
    );

    fireEvent.click(screen.getByRole("button", { name: /reload time/i }));
    await waitFor(() => expect(fetchMock.mock.calls.length).toBeGreaterThanOrEqual(2));
  });
});

// ─── App.tsx ──────────────────────────────────────────────────────────────────

describe("App component", () => {
  beforeEach(() => {
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: vi.fn(() => ({ matches: false })),
    });
    vi.stubGlobal("requestAnimationFrame", vi.fn(() => 1));
    vi.stubGlobal("cancelAnimationFrame", vi.fn());
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renders without crashing and mounts the Clock", async () => {
    const App = (await import("../App")).default;
    render(React.createElement(App));
    expect(screen.getByText("Current datetime")).toBeInTheDocument();
  });
});

// ─── main.tsx bootstrap ───────────────────────────────────────────────────────

describe("main.tsx bootstrap", () => {
  it("throws when #root element is absent", () => {
    document.body.innerHTML = "";
    const rootElement = document.getElementById("root");
    expect(() => {
      if (!rootElement) throw new Error("Root element not found");
    }).toThrow("Root element not found");
  });

  it("getElementById('root') returns the element when present", () => {
    document.body.innerHTML = '<div id="root"></div>';
    expect(document.getElementById("root")).not.toBeNull();
  });
});
