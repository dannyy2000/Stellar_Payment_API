"use client";

import { useEffect, useRef, useState, type RefObject } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import toast from "react-hot-toast";
import {
  useHydrateMerchantStore,
  useMerchantApiKey,
  useMerchantHydrated,
} from "@/lib/merchant-store";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface MetricData {
  date: string;
  volume: number;
  count: number;
}

interface MetricsResponse {
  data: MetricData[];
  total_volume: number;
  total_payments: number;
}

const CHART_HEIGHT = 300;
const EXPORT_SCALE = 2;

type ExportFormat = "png" | "svg";

function buildSvgMarkup(svg: SVGSVGElement): { markup: string; width: number; height: number } {
  const clone = svg.cloneNode(true) as SVGSVGElement;
  const bounds = svg.getBoundingClientRect();
  const width = Math.max(Math.round(bounds.width), 1);
  const height = Math.max(Math.round(bounds.height), 1);

  clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  clone.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
  clone.setAttribute("width", String(width));
  clone.setAttribute("height", String(height));

  if (!clone.getAttribute("viewBox")) {
    clone.setAttribute("viewBox", `0 0 ${width} ${height}`);
  }

  const background = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  background.setAttribute("width", "100%");
  background.setAttribute("height", "100%");
  background.setAttribute("fill", "#0f172a");
  clone.insertBefore(background, clone.firstChild);

  return {
    markup: new XMLSerializer().serializeToString(clone),
    width,
    height,
  };
}

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

async function exportChart(
  containerRef: RefObject<HTMLDivElement>,
  format: ExportFormat,
  filename: string,
) {
  const svg = containerRef.current?.querySelector("svg");
  if (!svg) {
    throw new Error("Chart export is unavailable until the chart finishes rendering.");
  }

  const { markup, width, height } = buildSvgMarkup(svg);
  const svgBlob = new Blob([markup], {
    type: "image/svg+xml;charset=utf-8",
  });

  if (format === "svg") {
    downloadBlob(svgBlob, `${filename}.svg`);
    return;
  }

  const url = URL.createObjectURL(svgBlob);

  try {
    const image = await new Promise<HTMLImageElement>((resolve, reject) => {
      const nextImage = new Image();
      nextImage.onload = () => resolve(nextImage);
      nextImage.onerror = () => reject(new Error("Failed to load chart for PNG export."));
      nextImage.src = url;
    });

    const canvas = document.createElement("canvas");
    canvas.width = width * EXPORT_SCALE;
    canvas.height = height * EXPORT_SCALE;

    const context = canvas.getContext("2d");
    if (!context) {
      throw new Error("Canvas export is not available in this browser.");
    }

    context.scale(EXPORT_SCALE, EXPORT_SCALE);
    context.drawImage(image, 0, 0, width, height);

    const pngBlob = await new Promise<Blob | null>((resolve) => {
      canvas.toBlob(resolve, "image/png");
    });

    if (!pngBlob) {
      throw new Error("Failed to generate PNG export.");
    }

    downloadBlob(pngBlob, `${filename}.png`);
  } finally {
    URL.revokeObjectURL(url);
  }
}

function ChartExportButton({
  chartId,
  containerRef,
  exportingChart,
  onExport,
}: {
  chartId: string;
  containerRef: RefObject<HTMLDivElement>;
  exportingChart: string | null;
  onExport: (
    chartId: string,
    format: ExportFormat,
    containerRef: RefObject<HTMLDivElement>,
  ) => Promise<void>;
}) {
  const isExporting = exportingChart === chartId;

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          type="button"
          disabled={isExporting}
          className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-300 transition-all hover:border-mint/30 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
        >
          <svg
            viewBox="0 0 24 24"
            className="h-4 w-4"
            fill="none"
            stroke="currentColor"
            strokeWidth={1.8}
          >
            <path d="M12 4v10" strokeLinecap="round" strokeLinejoin="round" />
            <path
              d="m8.5 10.5 3.5 3.5 3.5-3.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M5 18.5h14"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          {isExporting ? "Exporting..." : "Download Image"}
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onSelect={() => void onExport(chartId, "png", containerRef)}>
          Download PNG
        </DropdownMenuItem>
        <DropdownMenuItem onSelect={() => void onExport(chartId, "svg", containerRef)}>
          Download SVG
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export default function PaymentMetrics() {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exportingChart, setExportingChart] = useState<string | null>(null);
  const apiKey = useMerchantApiKey();
  const hydrated = useMerchantHydrated();
  const volumeChartRef = useRef<HTMLDivElement>(null);
  const countChartRef = useRef<HTMLDivElement>(null);

  useHydrateMerchantStore();

  useEffect(() => {
    if (!hydrated) return;

    const controller = new AbortController();

    const fetchMetrics = async () => {
      try {
        if (!apiKey) {
          setLoading(false);
          return;
        }

        const apiUrl =
          process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";
        const response = await fetch(`${apiUrl}/api/metrics/7day`, {
          headers: {
            "x-api-key": apiKey,
          },
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error("Failed to fetch metrics");
        }

        const data: MetricsResponse = await response.json();
        setMetrics(data);
      } catch (err: unknown) {
        if (err instanceof Error && err.name === "AbortError") return;
        setError(err instanceof Error ? err.message : "Failed to load metrics");
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();

    return () => controller.abort();
  }, [apiKey, hydrated]);

  if (loading || !hydrated) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-10 w-48 rounded-lg bg-white/5" />
        <div className="h-80 w-full rounded-xl bg-white/5" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-yellow-500/30 bg-yellow-500/10 p-6 text-center">
        <p className="text-sm text-yellow-400">{error}</p>
      </div>
    );
  }

  if (!metrics) {
    return null;
  }

  const formattedData = metrics.data.map((d) => ({
    ...d,
    dateShort: new Date(d.date).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    }),
  }));

  const handleExport = async (
    chartId: string,
    format: ExportFormat,
    containerRef: RefObject<HTMLDivElement>,
  ) => {
    setExportingChart(chartId);

    try {
      await exportChart(containerRef, format, chartId);
      toast.success(`Chart downloaded as ${format.toUpperCase()}`);
    } catch (exportError) {
      const message =
        exportError instanceof Error ? exportError.message : "Failed to export chart.";
      toast.error(message);
    } finally {
      setExportingChart(null);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Metrics Summary */}
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur">
          <p className="font-mono text-xs uppercase tracking-wider text-slate-400">
            7-Day Volume
          </p>
          <div className="mt-2 flex items-baseline gap-2">
            <p className="text-3xl font-bold text-mint">
              {metrics.total_volume.toLocaleString()}
            </p>
            <p className="text-sm text-slate-400">XLM</p>
          </div>
        </div>

        <div className="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur">
          <p className="font-mono text-xs uppercase tracking-wider text-slate-400">
            Total Payments
          </p>
          <div className="mt-2 flex items-baseline gap-2">
            <p className="text-3xl font-bold text-mint">
              {metrics.total_payments}
            </p>
            <p className="text-sm text-slate-400">
              {metrics.total_payments === 1 ? "payment" : "payments"}
            </p>
          </div>
        </div>
      </div>

      {/* Chart */}
      <div
        ref={volumeChartRef}
        className="flex flex-col gap-3 rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur"
      >
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex flex-col gap-1">
            <h3 className="font-semibold text-white">Payment Volume (7 Days)</h3>
            <p className="text-xs text-slate-400">Daily transaction amount</p>
          </div>
          <ChartExportButton
            chartId="payment-volume-7-days"
            containerRef={volumeChartRef}
            exportingChart={exportingChart}
            onExport={handleExport}
          />
        </div>

        <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
          <BarChart
            data={formattedData}
            margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorVolume" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#1e293b"
              horizontal={true}
              vertical={false}
            />
            <XAxis
              dataKey="dateShort"
              stroke="#64748b"
              style={{ fontSize: "12px" }}
            />
            <YAxis
              stroke="#64748b"
              style={{ fontSize: "12px" }}
              tickFormatter={(value) => value.toLocaleString()}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "1px solid #334155",
                borderRadius: "8px",
                padding: "8px 12px",
              }}
              labelStyle={{ color: "#e2e8f0", fontSize: "12px" }}
              formatter={(value: number) => [
                `${value.toLocaleString()} XLM`,
                "Volume",
              ]}
              cursor={{ fill: "rgba(14, 165, 233, 0.1)" }}
            />
            <Bar
              dataKey="volume"
              fill="url(#colorVolume)"
              isAnimationActive={true}
              animationDuration={500}
              radius={[8, 8, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Payment Count Chart */}
      <div
        ref={countChartRef}
        className="flex flex-col gap-3 rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur"
      >
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex flex-col gap-1">
            <h3 className="font-semibold text-white">Payment Count (7 Days)</h3>
            <p className="text-xs text-slate-400">
              Number of transactions per day
            </p>
          </div>
          <ChartExportButton
            chartId="payment-count-7-days"
            containerRef={countChartRef}
            exportingChart={exportingChart}
            onExport={handleExport}
          />
        </div>

        <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
          <LineChart
            data={formattedData}
            margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#1e293b"
              horizontal={true}
              vertical={false}
            />
            <XAxis
              dataKey="dateShort"
              stroke="#64748b"
              style={{ fontSize: "12px" }}
            />
            <YAxis
              stroke="#64748b"
              style={{ fontSize: "12px" }}
              allowDecimals={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "1px solid #334155",
                borderRadius: "8px",
                padding: "8px 12px",
              }}
              labelStyle={{ color: "#e2e8f0", fontSize: "12px" }}
              formatter={(value: number) => [
                value.toLocaleString(),
                "Payments",
              ]}
              cursor={{ stroke: "#10b981", strokeWidth: 2 }}
            />
            <Line
              type="monotone"
              dataKey="count"
              stroke="#10b981"
              strokeWidth={2}
              dot={{ fill: "#10b981", r: 4 }}
              activeDot={{ r: 6 }}
              isAnimationActive={true}
              animationDuration={500}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
