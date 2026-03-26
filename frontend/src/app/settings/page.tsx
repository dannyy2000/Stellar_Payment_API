"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import CopyButton from "@/components/CopyButton";
import toast from "react-hot-toast";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:4000";

// ─── Eye icon (show / hide key) ──────────────────────────────────────────────

function EyeIcon({ open }: { open: boolean }) {
  return open ? (
    <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth={1.8}>
      <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="12" cy="12" r="3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  ) : (
    <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth={1.8}>
      <path d="M17.94 17.94A10.1 10.1 0 0 1 12 19c-6.4 0-10-7-10-7a18.1 18.1 0 0 1 5.06-5.94M9.9 4.24A9.1 9.1 0 0 1 12 4c6.4 0 10 7 10 7a18.1 18.1 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" strokeLinecap="round" strokeLinejoin="round" />
      <line x1="1" y1="1" x2="23" y2="23" strokeLinecap="round" />
    </svg>
  );
}

// ─── Masked key display ───────────────────────────────────────────────────────

function mask(key: string) {
  if (key.length <= 12) return "•".repeat(key.length);
  return key.slice(0, 7) + "•".repeat(key.length - 13) + key.slice(-6);
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function SettingsPage() {
  const [apiKey, setApiKey] = useState<string | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  // Rotation flow state
  const [confirming, setConfirming] = useState(false);
  const [rotating, setRotating] = useState(false);
  const [rotateError, setRotateError] = useState<string | null>(null);

  // Load from localStorage after hydration to avoid SSR mismatch
  useEffect(() => {
    setApiKey(localStorage.getItem("merchant_api_key"));
    setHydrated(true);
  }, []);

  const startRotate = () => {
    setRotateError(null);
    setConfirming(true);
  };

  const cancelRotate = () => {
    setConfirming(false);
  };

  const confirmRotate = async () => {
    if (!apiKey) return;
    setRotating(true);
    setRotateError(null);

    try {
      const res = await fetch(`${API_URL}/api/rotate-key`, {
        method: "POST",
        headers: { "x-api-key": apiKey },
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Failed to rotate key");

      const newKey: string = data.api_key;
      localStorage.setItem("merchant_api_key", newKey);
      setApiKey(newKey);
      setRevealed(true); // show the new key immediately
      setConfirming(false);
      toast.success("API key rotated — update any integrations using the old key.");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to rotate key";
      setRotateError(msg);
      toast.error(msg);
    } finally {
      setRotating(false);
    }
  };

  // ── Await hydration ──────────────────────────────────────────────────────
  if (!hydrated) return null;

  // ── No key stored ────────────────────────────────────────────────────────
  if (!apiKey) {
    return (
      <main className="mx-auto flex min-h-screen max-w-lg flex-col justify-center gap-8 px-6 py-16">
        <header className="flex flex-col gap-3 text-center">
          <p className="font-mono text-xs uppercase tracking-[0.3em] text-mint">Settings</p>
          <h1 className="text-3xl font-bold text-white">Merchant Settings</h1>
        </header>

        <div className="flex flex-col items-center gap-4 rounded-2xl border border-yellow-500/30 bg-yellow-500/10 p-8 text-center">
          <p className="text-base font-medium text-yellow-200">No API key found</p>
          <p className="text-sm text-slate-400">
            Register a merchant account first to manage your credentials here.
          </p>
          <Link
            href="/register"
            className="mt-2 rounded-xl bg-mint px-5 py-2.5 text-sm font-bold text-black transition-all hover:bg-glow"
          >
            Register as Merchant
          </Link>
        </div>
      </main>
    );
  }

  const displayKey = revealed ? apiKey : mask(apiKey);

  return (
    <main className="mx-auto flex min-h-screen max-w-lg flex-col justify-center gap-10 px-6 py-16">
      {/* ── Header ── */}
      <header className="flex flex-col gap-3 text-center">
        <p className="font-mono text-xs uppercase tracking-[0.3em] text-mint">Settings</p>
        <h1 className="text-3xl font-bold text-white">Merchant Settings</h1>
        <p className="text-sm text-slate-400">
          Manage your API credentials. Keep your key secret — treat it like a password.
        </p>
      </header>

      {/* ── Main card ── */}
      <div className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl backdrop-blur">
        <div className="flex flex-col gap-8">

          {/* API Key section */}
          <section className="flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <h2 className="text-xs font-medium uppercase tracking-wider text-slate-400">
                API Key
              </h2>
              <button
                type="button"
                onClick={() => setRevealed((v) => !v)}
                aria-label={revealed ? "Hide API key" : "Reveal API key"}
                className="flex items-center gap-1.5 rounded-lg px-2 py-1 text-xs text-slate-400 transition-colors hover:bg-white/5 hover:text-white"
              >
                <EyeIcon open={revealed} />
                {revealed ? "Hide" : "Reveal"}
              </button>
            </div>

            <div className="flex items-center gap-2 overflow-hidden rounded-xl border border-white/10 bg-black/40 p-1 pl-4">
              <code
                className={`flex-1 truncate font-mono text-sm transition-colors ${
                  revealed ? "text-mint" : "text-slate-500"
                }`}
              >
                {displayKey}
              </code>
              {/* Only allow copying when revealed to prevent accidental exposure */}
              {revealed && <CopyButton text={apiKey} />}
            </div>

            <p className="text-[11px] text-slate-600">
              Pass this as the <code className="text-slate-500">x-api-key</code> header on every API request.
            </p>
          </section>

          {/* Divider */}
          <div className="h-px bg-white/10" />

          {/* Rotate Key section */}
          <section className="flex flex-col gap-4">
            <div className="flex flex-col gap-1">
              <h2 className="text-xs font-medium uppercase tracking-wider text-slate-400">
                Rotate API Key
              </h2>
              <p className="text-sm text-slate-500">
                Generates a new key and immediately invalidates the current one.
                Any integration still using the old key will stop working.
              </p>
            </div>

            {rotateError && (
              <div
                role="alert"
                className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400"
              >
                {rotateError}
              </div>
            )}

            {!confirming ? (
              <button
                type="button"
                onClick={startRotate}
                className="flex h-11 items-center justify-center rounded-xl border border-red-500/40 bg-red-500/10 px-5 text-sm font-semibold text-red-400 transition-all hover:border-red-500/70 hover:bg-red-500/20"
              >
                Rotate Key…
              </button>
            ) : (
              <div className="flex flex-col gap-3 rounded-xl border border-yellow-500/30 bg-yellow-500/10 p-4">
                <p className="text-sm font-medium text-yellow-200">
                  Are you sure? This cannot be undone.
                </p>
                <p className="text-xs text-slate-400">
                  The old key will stop working immediately. Make sure to update all your
                  integrations with the new key.
                </p>
                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={confirmRotate}
                    disabled={rotating}
                    className="group relative flex flex-1 h-10 items-center justify-center rounded-xl bg-mint font-bold text-black text-sm transition-all hover:bg-glow disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {rotating ? (
                      <span className="flex items-center gap-2">
                        <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        Rotating…
                      </span>
                    ) : (
                      "Yes, rotate key"
                    )}
                  </button>
                  <button
                    type="button"
                    onClick={cancelRotate}
                    disabled={rotating}
                    className="flex flex-1 h-10 items-center justify-center rounded-xl border border-white/10 bg-white/5 text-sm font-medium text-slate-300 transition-all hover:bg-white/10 disabled:opacity-50"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </section>
        </div>
      </div>

      {/* Footer nav */}
      <footer className="flex justify-center gap-6 text-xs text-slate-500">
        <Link href="/" className="hover:text-slate-300 transition-colors">Dashboard</Link>
        <Link href="/dashboard/create" className="hover:text-slate-300 transition-colors">Create Payment</Link>
      </footer>
    </main>
  );
}
