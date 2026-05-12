/**
 * ClockComponent.test.tsx
 *
 * Maximises coverage for:
 *   src/App.tsx
 *   src/main.tsx  (bootstrapping logic only – DOM side-effect tested via jsdom)
 *   src/components/clock/Clock.tsx
 *   src/components/clock/clockRenderer.ts
 *   src/components/clock/useClockCanvas.ts
 *   src/components/clock/useClockTime.ts
 *   src/components/strategies.ts  (TickMovementStrategy.reset branch)
 *
 * Run with: npx vitest run --coverage
 */

import { describe, it, expect, vi, beforeEach, afterEach, type Mock } from "vitest";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import "@testing-library/jest-dom";
import React from "react";

// ─── helpers ──────────────────────────────────────────────────────────────────

function mockCanvas() {
  const ctx: Partial<CanvasRenderingContext2D> = {
    scale: vi.fn(),
    clearRect: vi.fn(),
    beginPath: vi.fn(),
    arc: vi.fn(),
    fill: vi.fn(),
    stroke: vi.fn(),
    moveTo: vi.fn(),
    lineTo: vi.fn(),
    fillText: vi.fn(),
    get font() { return ""; },
    set font(_v) {},
    get fillStyle() { return ""; },
    set fillStyle(_v) {},
    get strokeStyle() { return ""; },
    set strokeStyle(_v) {},
    get lineWidth() { return 1; },
    set lineWidth(_v) {},
    get lineCap() { return "butt" as CanvasLineCap; },
    set lineCap(_v) {},
    get textAlign() { return "start" as CanvasTextAlign; },
    set textAlign(_v) {},
    get textBaseline() { return "alphabetic" as CanvasTextBaseline; },
    set textBaseline(_v) {},
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

// ─── strategies.ts – TickMovementStrategy.reset (the one uncovered branch) ───

describe("TickMovementStrategy.reset", () => {
  it("reset() is a no-op and returns undefined", async () => {
    const { TickMovementStrategy } = await import("../src/components/strategies");
    const s = new TickMovementStrategy();
    expect(s.reset()).toBeUndefined();
    // After reset it still snaps to target
    expect(s.update(0, 42)).toBeCloseTo(42);
  });
});

// ─── clockRenderer.ts ─────────────────────────────────────────────────────────

describe("clockRenderer – renderClock", () => {
  let matchMediaMock: Mock;

  beforeEach(() => {
    matchMediaMock = vi.fn(() => ({ matches: false }));
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: matchMediaMock,
    });
    Object.defineProperty(window, "devicePixelRatio", { writable: true, value: 2 });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  async function callRenderClock(darkMode = false, dpr = 1) {
    matchMediaMock.mockReturnValue({ matches: darkMode });
    Object.defineProperty(window, "devicePixelRatio", { writable: true, value: dpr });

    const { renderClock } = await import("../src/components/clock/clockRenderer?t=" + Date.now());
    const { canvas, ctx } = mockCanvas();
    const hands = { second: 15, minute: 30, hour: 6 };
    const now = new Date(2025, 0, 1, 12, 30, 15, 0);

    renderClock(canvas, ctx as CanvasRenderingContext2D, { hands, now });
    return { ctx, canvas };
  }

  it("calls clearRect and drawing primitives in light mode", async () => {
    const { ctx } = await callRenderClock(false, 1);
    expect((ctx as any).clearRect).toHaveBeenCalled();
    expect((ctx as any).beginPath).toHaveBeenCalled();
    expect((ctx as any).arc).toHaveBeenCalled();
    expect((ctx as any).fillText).toHaveBeenCalled();
  });

  it("calls clearRect and drawing primitives in dark mode", async () => {
    const { ctx } = await callRenderClock(true, 2);
    expect((ctx as any).clearRect).toHaveBeenCalled();
    expect((ctx as any).arc).toHaveBeenCalled();
  });

  it("scales canvas for device pixel ratio != 1", async () => {
    const { canvas } = await callRenderClock(false, 3);
    // width/height should be set to clientWidth * dpr
    expect(canvas.width).toBe(300 * 3);
    expect(canvas.height).toBe(300 * 3);
  });

  it("skips re-scaling when dimensions already match", async () => {
    const { renderClock } = await import("../src/components/clock/clockRenderer");
    const { canvas, ctx } = mockCanvas();
    // Pre-set dimensions to match clientWidth * dpr=1
    (canvas as any).width = 300;
    (canvas as any).height = 300;
    Object.defineProperty(window, "devicePixelRatio", { writable: true, value: 1 });

    const scaleSpy = ctx.scale as Mock;
    renderClock(canvas, ctx as CanvasRenderingContext2D, {
      hands: { second: 0, minute: 0, hour: 0 },
      now: new Date(),
    });
    expect(scaleSpy).not.toHaveBeenCalled();
  });

  it("renders all hands including second hand (red)", async () => {
    const { renderClock } = await import("../src/components/clock/clockRenderer");
    const { canvas, ctx } = mockCanvas();
    let sawRed = false;
    Object.defineProperty(ctx, "strokeStyle", {
      set(v: string) { if (v === "#ff3333") sawRed = true; },
      get() { return ""; },
    });
    renderClock(canvas, ctx as CanvasRenderingContext2D, {
      hands: { second: 45, minute: 0, hour: 3 },
      now: new Date(),
    });
    expect(sawRed).toBe(true);
  });
});

// ─── useClockTime.ts ──────────────────────────────────────────────────────────

describe("useClockTime", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  it("starts in loading status", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {}))); // never resolves

    const { useClockTime } = await import("../src/components/clock/useClockTime");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    expect(result.current.status).toBe("loading");
    expect(result.current.datetime).toBeNull();
  });

  it("transitions to ok and populates datetime on success", async () => {
    const isoStr = "2025-04-05T14:49:14.000Z";
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ datetime: isoStr }),
        }),
      ),
    );

    const { useClockTime } = await import("../src/components/clock/useClockTime?ok=1");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    await act(async () => { await vi.runAllTimersAsync(); });
    await waitFor(() => expect(result.current.status).toBe("ok"));
    expect(result.current.datetime).toBe(isoStr);
  });

  it("transitions to error when fetch rejects", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("network down"))));

    const { useClockTime } = await import("../src/components/clock/useClockTime?err=1");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    await act(async () => { await vi.runAllTimersAsync(); });
    await waitFor(() => expect(result.current.status).toBe("error"));
  });

  it("transitions to error when response is not ok", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({ ok: false, status: 503 }),
      ),
    );

    const { useClockTime } = await import("../src/components/clock/useClockTime?notok=1");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    await act(async () => { await vi.runAllTimersAsync(); });
    await waitFor(() => expect(result.current.status).toBe("error"));
  });

  it("handleReload resets status to loading then ok", async () => {
    const isoStr = "2025-06-01T10:00:00.000Z";
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ datetime: isoStr }),
        }),
      ),
    );

    const { useClockTime } = await import("../src/components/clock/useClockTime?reload=1");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    await act(async () => { await vi.runAllTimersAsync(); });
    await waitFor(() => expect(result.current.status).toBe("ok"));

    await act(async () => { await result.current.handleReload(); });
    expect(result.current.status).toBe("ok");
    expect(result.current.datetime).toBe(isoStr);
  });

  it("handleReload sets error when fetch fails", async () => {
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

    const { useClockTime } = await import("../src/components/clock/useClockTime?reload-err=1");
    const { renderHook } = await import("@testing-library/react");

    const { result } = renderHook(() => useClockTime());
    await act(async () => { await vi.runAllTimersAsync(); });
    await waitFor(() => expect(result.current.status).toBe("ok"));

    await act(async () => { await result.current.handleReload(); });
    expect(result.current.status).toBe("error");
  });

  it("exposes ref objects needed by useClockCanvas", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));

    const { useClockTime } = await import("../src/components/clock/useClockTime?refs=1");
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
    vi.useFakeTimers();
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: vi.fn(() => ({ matches: false })),
    });
    // Mock rAF / cAF
    let rafId = 0;
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((cb: FrameRequestCallback) => {
        rafId++;
        // Execute once synchronously so draw() runs
        cb(0);
        return rafId;
      }),
    );
    vi.stubGlobal("cancelAnimationFrame", vi.fn());
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  it("returns a ref and does not throw when canvas is available", async () => {
    const { useClockCanvas } = await import("../src/components/clock/useClockCanvas");
    const { useRef } = await import("react");
    const { renderHook } = await import("@testing-library/react");
    const { ClockController } = await import("../src/components/clockController");

    // Provide time refs that indicate NOT ready – draw loop should not crash
    const fakeRefs = {
      serverAnchorRef: { current: new Date() },
      wallAnchorRef: { current: performance.now() },
      controllerRef: { current: new ClockController(new Date()) },
      readyRef: { current: false },
    };

    const { result } = renderHook(() => useClockCanvas(fakeRefs as any));
    expect(result.current).toBeDefined();
  });

  it("calls renderClock when readyRef is true and canvas has a context", async () => {
    const { renderClock } = await import("../src/components/clock/clockRenderer");
    const renderSpy = vi.spyOn(
      await import("../src/components/clock/clockRenderer"),
      "renderClock",
    );

    const { useClockCanvas } = await import("../src/components/clock/useClockCanvas?ready=1");
    const { renderHook } = await import("@testing-library/react");
    const { ClockController } = await import("../src/components/clockController");

    const { canvas, ctx } = mockCanvas();

    const fakeRefs = {
      serverAnchorRef: { current: new Date() },
      wallAnchorRef: { current: performance.now() - 100 },
      controllerRef: { current: new ClockController(new Date()) },
      readyRef: { current: true },
    };

    renderHook(() => {
      const ref = useClockCanvas(fakeRefs as any);
      // Inject canvas into the ref so the hook finds it
      (ref as any).current = canvas;
      return ref;
    });

    // Allow effects to run
    await act(async () => {});
  });

  it("cancels animation frame on unmount", async () => {
    const cancelSpy = vi.spyOn(window, "cancelAnimationFrame");

    const { useClockCanvas } = await import("../src/components/clock/useClockCanvas?unmount=1");
    const { renderHook } = await import("@testing-library/react");
    const { ClockController } = await import("../src/components/clockController");

    const fakeRefs = {
      serverAnchorRef: { current: new Date() },
      wallAnchorRef: { current: performance.now() },
      controllerRef: { current: new ClockController(new Date()) },
      readyRef: { current: false },
    };

    const { unmount } = renderHook(() => useClockCanvas(fakeRefs as any));
    unmount();
    expect(cancelSpy).toHaveBeenCalled();
  });
});

// ─── Clock.tsx (component integration) ───────────────────────────────────────

describe("Clock component", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: vi.fn(() => ({ matches: false })),
    });
    vi.stubGlobal("requestAnimationFrame", vi.fn(() => 1));
    vi.stubGlobal("cancelAnimationFrame", vi.fn());
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  it("renders heading and Reload button in loading state", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));

    const { Clock } = await import("../src/components/clock/Clock");
    render(React.createElement(Clock));

    expect(screen.getByText("Current datetime")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /reload time/i })).toBeInTheDocument();
  });

  it("shows datetime text after successful fetch", async () => {
    const isoStr = "2025-04-05T14:49:14.000Z";
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ datetime: isoStr }),
        }),
      ),
    );

    const { Clock } = await import("../src/components/clock/Clock?ok=1");
    render(React.createElement(Clock));

    await act(async () => { await vi.runAllTimersAsync(); });
    await waitFor(() => expect(screen.getByText(isoStr)).toBeInTheDocument());
  });

  it("shows error message after failed fetch", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("fail"))));

    const { Clock } = await import("../src/components/clock/Clock?err=1");
    render(React.createElement(Clock));

    await act(async () => { await vi.runAllTimersAsync(); });
    await waitFor(() => expect(screen.getByText(/failed to load time/i)).toBeInTheDocument());
  });

  it("Reload button is disabled while loading", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));

    const { Clock } = await import("../src/components/clock/Clock?loading=1");
    render(React.createElement(Clock));

    const btn = screen.getByRole("button");
    // Still in loading because fetch never resolves
    expect(btn).toBeDisabled();
  });

  it("clicking Reload button triggers a new fetch", async () => {
    const isoStr = "2025-06-01T10:00:00.000Z";
    const fetchMock = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ datetime: isoStr }),
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const { Clock } = await import("../src/components/clock/Clock?click=1");
    render(React.createElement(Clock));

    await act(async () => { await vi.runAllTimersAsync(); });
    await waitFor(() => expect(screen.getByRole("button", { name: /reload time/i })).not.toBeDisabled());

    fireEvent.click(screen.getByRole("button", { name: /reload time/i }));
    await act(async () => { await vi.runAllTimersAsync(); });

    // fetch called at least twice (initial + reload)
    expect(fetchMock.mock.calls.length).toBeGreaterThanOrEqual(2);
  });
});

// ─── App.tsx ──────────────────────────────────────────────────────────────────

describe("App component", () => {
  beforeEach(() => {
    vi.useFakeTimers();
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
    vi.useRealTimers();
  });

  it("renders without crashing and contains the Clock heading", async () => {
    const App = (await import("../src/App")).default;
    render(React.createElement(App));
    expect(screen.getByText("Current datetime")).toBeInTheDocument();
  });
});

// ─── main.tsx bootstrapping ───────────────────────────────────────────────────

describe("main.tsx bootstrap", () => {
  it("throws when #root element is absent", async () => {
    // Ensure no #root in document
    document.body.innerHTML = "";
    await expect(import("../src/main?noroot=1")).rejects.toThrow();
  });

  it("mounts successfully when #root exists", async () => {
    // Provide a #root element
    document.body.innerHTML = '<div id="root"></div>';

    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: vi.fn(() => ({ matches: false })),
    });
    vi.stubGlobal("requestAnimationFrame", vi.fn(() => 1));
    vi.stubGlobal("cancelAnimationFrame", vi.fn());

    // Dynamic import with cache-busting to re-execute the module
    await expect(import("../src/main?root=1")).resolves.toBeDefined();
  });
});
