"use client";

import React, { useState } from "react";
import PaymentMetrics from "@/components/PaymentMetrics";
import RecentPayments from "@/components/RecentPayments";
import WithdrawalModal from "@/components/WithdrawalModal";
import Link from "next/link";
import { useTranslations } from "next-intl";

export default function DashboardPage() {
  const t = useTranslations("dashboardPage");
  const [isWithdrawOpen, setIsWithdrawOpen] = useState(false);

  return (
    <div className="flex flex-col gap-10">
      <header className="flex flex-col gap-4">
        <h1 className="text-4xl font-bold text-white">{t("title")}</h1>
        <p className="max-w-2xl text-slate-400">
          {t("description")}
        </p>
      </header>

      <div className="grid gap-10 lg:grid-cols-3">
        {/* Left Column: Metrics and Activity */}
        <div className="flex flex-col gap-10 lg:col-span-2">
          <section className="flex flex-col gap-4">
            <h2 className="text-xl font-semibold text-white">{t("paymentMetrics")}</h2>
            <PaymentMetrics />
          </section>

          <section className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-white">{t("recentActivity")}</h2>
              <Link href="/payments" className="text-sm text-mint hover:text-glow">
                {t("viewAllPayments")} →
              </Link>
            </div>
            <RecentPayments />
          </section>
        </div>

        {/* Right Column: Quick Actions & Guides */}
        <aside className="flex flex-col gap-8">
          <section className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur">
            <h3 className="mb-4 text-lg font-semibold text-white">{t("quickActions")}</h3>
            <div className="flex flex-col gap-3">
              <Link
                href="/dashboard/create"
                className="flex items-center gap-3 rounded-xl border border-mint/20 bg-mint/5 px-4 py-3 text-sm font-medium text-mint transition-all hover:bg-mint/10"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                {t("createPaymentLink")}
              </Link>
              <button
                onClick={() => setIsWithdrawOpen(true)}
                className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm font-medium text-slate-300 transition-all hover:bg-white/10 hover:text-white"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                </svg>
                {t("withdrawFunds")}
              </button>
            </div>
          </section>

          <section className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur">
            <h3 className="mb-4 text-lg font-semibold text-white">{t("development")}</h3>
            <div className="space-y-4 text-sm text-slate-400">
              <div className="flex items-start gap-3">
                <div className="mt-1 h-1.5 w-1.5 rounded-full bg-mint" />
                <p>{t("apiKeysTip")}</p>
              </div>
              <div className="flex items-start gap-3">
                <div className="mt-1 h-1.5 w-1.5 rounded-full bg-mint" />
                <p>{t("webhookLogsTip")}</p>
              </div>
            </div>
          </section>
        </aside>
      </div>

      <WithdrawalModal 
        isOpen={isWithdrawOpen} 
        onClose={() => setIsWithdrawOpen(false)} 
      />
    </div>
  );
}
