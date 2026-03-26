"use client";

import { useEffect, useRef, useState } from "react";
import PaymentDetailModal from "@/components/PaymentDetailModal";
import {
  useHydrateMerchantStore,
  useMerchantApiKey,
  useMerchantHydrated,
} from "@/lib/merchant-store";

interface Payment {
  id: string;
  amount: number;
  asset: string;
  status: string;
  description: string | null;
  created_at: string;
}

interface PaginatedResponse {
  payments: Payment[];
  total_count: number;
  total_pages: number;
  page: number;
  limit: number;
}

const LIMIT = 10;

export default function RecentPayments() {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page] = useState(1);
  const [, setTotalPages] = useState(1);
  const [, setTotalCount] = useState(0);
  const [selectedPayment, setSelectedPayment] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [bulkMode, setBulkMode] = useState(false);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const selectAllRef = useRef<HTMLInputElement | null>(null);
  const apiKey = useMerchantApiKey();
  const hydrated = useMerchantHydrated();

  useHydrateMerchantStore();

  useEffect(() => {
    if (!hydrated) return;

    const controller = new AbortController();

    const fetchPayments = async () => {
      try {
        if (!apiKey) {
          setError("API key not found. Please register or log in.");
          setLoading(false);
          return;
        }

        const apiUrl =
          process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";
        const response = await fetch(
          `${apiUrl}/api/payments?page=${page}&limit=${LIMIT}`,
          {
            headers: {
              "x-api-key": apiKey,
            },
            signal: controller.signal,
          },
        );

        if (!response.ok) {
          throw new Error("Failed to fetch payments");
        }

        const data: PaginatedResponse = await response.json();
        setPayments(data.payments ?? []);
        setTotalPages(data.total_pages ?? 1);
        setTotalCount(data.total_count ?? 0);
      } catch (err: unknown) {
        if (err instanceof Error && err.name === "AbortError") return;
        setError(
          err instanceof Error ? err.message : "Failed to load payments",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchPayments();

    return () => controller.abort();
  }, [apiKey, page, hydrated]);

  const handlePaymentClick = (paymentId: string) => {
    setSelectedPayment(paymentId);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedPayment(null);
  };

  const allPaymentIds = payments.map((payment) => payment.id);
  const selectedCount = selectedIds.size;
  const allSelected = allPaymentIds.length > 0 && selectedCount === allPaymentIds.length;
  const someSelected = selectedCount > 0 && !allSelected;

  useEffect(() => {
    if (selectAllRef.current) {
      selectAllRef.current.indeterminate = someSelected;
    }
  }, [someSelected]);

  const toggleBulkMode = () => {
    setBulkMode((prev) => {
      const next = !prev;
      if (!next) {
        setSelectedIds(new Set());
      }
      return next;
    });
  };

  const toggleSelection = (id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const toggleSelectAll = () => {
    if (allSelected) {
      setSelectedIds(new Set());
      return;
    }
    setSelectedIds(new Set(allPaymentIds));
  };

  const cancelSelected = () => {
    if (selectedCount === 0) return;
    setPayments((prev) => prev.filter((payment) => !selectedIds.has(payment.id)));
    setSelectedIds(new Set());
  };

  if (loading) {
    return (
      <div className="animate-pulse space-y-3">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="h-12 w-full rounded-lg bg-white/5" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-yellow-500/30 bg-yellow-500/10 p-8 text-center">
        {/* Error State Illustration */}
        <div className="mx-auto mb-6 w-24 h-24 relative">
          <div className="absolute inset-0 bg-yellow-500/10 rounded-full blur-xl animate-pulse" />
          <div className="relative w-full h-full flex items-center justify-center">
            <svg
              className="w-12 h-12 text-yellow-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.502 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
              />
            </svg>
          </div>
        </div>

        <div className="space-y-4">
          <div className="space-y-2">
            <h3 className="text-lg font-semibold text-white">
              Connection Error
            </h3>
            <p className="text-sm text-yellow-400">{error}</p>
            <p className="text-xs text-slate-500 max-w-md mx-auto">
              Make sure the backend is running and the payments endpoint is
              available.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 justify-center items-center">
            <button
              onClick={() => window.location.reload()}
              className="inline-flex items-center gap-2 rounded-lg bg-yellow-500/20 border border-yellow-500/30 px-4 py-2 text-sm font-medium text-yellow-400 transition-all hover:bg-yellow-500/30"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              Retry Connection
            </button>

            <button
              onClick={() => window.open("https://webhook.site", "_blank")}
              className="inline-flex items-center gap-2 rounded-lg border border-mint/30 bg-mint/5 px-4 py-2 text-sm font-medium text-mint transition-all hover:bg-mint/10"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              Test Webhook Anyway
            </button>
          </div>

          <div className="mt-4 p-3 rounded-lg border border-yellow-500/20 bg-yellow-500/5">
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 rounded-full bg-yellow-400 mt-1.5 flex-shrink-0" />
              <div className="text-left">
                <p className="text-xs font-medium text-yellow-400">
                  Troubleshooting Tip
                </p>
                <p className="text-xs text-slate-500">
                  You can still test webhook functionality while backend
                  services are being restored.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (payments.length === 0) {
    return (
      <div className="rounded-xl border border-white/10 bg-white/5 p-8 text-center">
        {/* Empty State Illustration */}
        <div className="mx-auto mb-6 w-24 h-24 relative">
          <div className="absolute inset-0 bg-mint/10 rounded-full blur-xl" />
          <div className="relative w-full h-full flex items-center justify-center">
            <svg
              className="w-12 h-12 text-mint/60"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
              />
            </svg>
          </div>
        </div>

        <div className="space-y-4">
          <div className="space-y-2">
            <h3 className="text-lg font-semibold text-white">
              No payments yet
            </h3>
            <p className="text-sm text-slate-400 max-w-md mx-auto">
              Start accepting payments by creating your first payment link or
              testing webhooks to see transaction data flow.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 justify-center items-center">
            <button
              onClick={() => window.open("/dashboard/create", "_self")}
              className="group relative inline-flex items-center gap-2 rounded-lg bg-mint px-4 py-2 text-sm font-medium text-black transition-all hover:bg-glow"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Create Payment Link
              <div className="absolute inset-0 -z-10 bg-mint/20 opacity-0 blur-xl transition-opacity group-hover:opacity-100" />
            </button>

            <button
              onClick={() => window.open("https://webhook.site", "_blank")}
              className="inline-flex items-center gap-2 rounded-lg border border-mint/30 bg-mint/5 px-4 py-2 text-sm font-medium text-mint transition-all hover:bg-mint/10"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              Send Test Webhook
            </button>
          </div>

          <div className="mt-6 p-4 rounded-lg border border-slate-700/50 bg-slate-800/30">
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 rounded-full bg-mint mt-1.5 flex-shrink-0" />
              <div className="text-left space-y-1">
                <p className="text-xs font-medium text-mint">
                  Getting Started Guide
                </p>
                <p className="text-xs text-slate-400">
                  Use webhook tools to test payment notifications and see
                  real-time data appear in this dashboard.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Table */}
      <div className="overflow-x-auto rounded-xl border border-white/10">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-white/10 bg-white/5">
              <th className="px-4 py-3 font-mono text-xs uppercase tracking-wider text-slate-400">
                Status
              </th>
              <th className="px-4 py-3 font-mono text-xs uppercase tracking-wider text-slate-400">
                Amount
              </th>
              <th className="hidden px-4 py-3 font-mono text-xs uppercase tracking-wider text-slate-400 sm:table-cell">
                Description
              </th>
              <th className="hidden px-4 py-3 font-mono text-xs uppercase tracking-wider text-slate-400 md:table-cell">
                Date
              </th>
              <th className="px-4 py-3 font-mono text-xs uppercase tracking-wider text-slate-400">
                Link
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {payments.map((payment) => (
              <tr
                key={payment.id}
                className="transition-colors hover:bg-white/5 cursor-pointer"
                onClick={() => handlePaymentClick(payment.id)}
              >
                <td className="px-4 py-3">
                  <span
                    className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium ${
                      payment.status === "confirmed"
                        ? "bg-green-500/20 text-green-400"
                        : "bg-yellow-500/20 text-yellow-400"
                    }`}
                  >
                    {payment.status}
                  </span>
                </td>
                <td className="px-4 py-3 font-medium text-white">
                  {payment.amount} {payment.asset}
                </td>
                <td className="hidden px-4 py-3 text-slate-400 sm:table-cell">
                  {payment.description || "—"}
                </td>
                <td className="hidden px-4 py-3 text-slate-400 md:table-cell">
                  {new Date(payment.created_at).toLocaleDateString()}
                </td>
                <td className="px-4 py-3">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handlePaymentClick(payment.id);
                    }}
                    className="font-mono text-xs text-mint transition-colors hover:text-glow"
                  >
                    View →
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <PaymentDetailModal
        paymentId={selectedPayment || ""}
        isOpen={isModalOpen}
        onClose={closeModal}
      />
    </div>
  );
}
