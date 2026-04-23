import { useEffect, useRef, useState } from "react";
import { ClockController } from "../clockController";
import { getApiBaseUrl } from "../../config";

export type ClockStatus = "loading" | "ok" | "error";

export interface ClockTimeRefs {
  serverAnchorRef: React.RefObject<Date>;
  wallAnchorRef: React.RefObject<number>;
  controllerRef: React.RefObject<ClockController>;
  readyRef: React.RefObject<boolean>;
}

export interface UseClockTimeResult extends ClockTimeRefs {
  datetime: string | null;
  status: ClockStatus;
  handleReload: () => Promise<void>;
}

async function fetchTimeData(): Promise<{ datetime: string }> {
  const res = await fetch(`${getApiBaseUrl()}/time`);
  if (!res.ok) throw new Error(`HTTP ${String(res.status)}`);
  return (await res.json()) as { datetime: string };
}

function applyTimeData(
  data: { datetime: string },
  refs: {
    serverAnchorRef: React.MutableRefObject<Date>;
    wallAnchorRef: React.MutableRefObject<number>;
    controllerRef: React.MutableRefObject<ClockController>;
    readyRef: React.MutableRefObject<boolean>;
  },
): Date {
  const serverDate = new Date(data.datetime);
  refs.serverAnchorRef.current = serverDate;
  refs.wallAnchorRef.current = performance.now();
  refs.controllerRef.current.reset(serverDate);
  refs.readyRef.current = true;
  return serverDate;
}

export function useClockTime(): UseClockTimeResult {
  const serverAnchorRef = useRef<Date>(new Date(0));
  const wallAnchorRef = useRef<number>(0);
  const controllerRef = useRef<ClockController>(new ClockController(new Date(0)));
  const readyRef = useRef<boolean>(false);

  const [datetime, setDatetime] = useState<string | null>(null);
  const [status, setStatus] = useState<ClockStatus>("loading");

  const loadTime = async () => {
    setStatus("loading");
    try {
      const data = await fetchTimeData();
      applyTimeData(data, {
        serverAnchorRef: serverAnchorRef,
        wallAnchorRef: wallAnchorRef,
        controllerRef: controllerRef,
        readyRef: readyRef,
      });
      setDatetime(data.datetime);
      setStatus("ok");
    } catch {
      setStatus("error");
    }
  };

  useEffect(() => {
    void loadTime();
  }, []);

  return {
    datetime,
    status,
    handleReload: loadTime,
    serverAnchorRef,
    wallAnchorRef,
    controllerRef,
    readyRef,
  };
}
