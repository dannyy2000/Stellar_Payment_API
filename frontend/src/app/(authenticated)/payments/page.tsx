"use client";

import RecentPayments from "@/components/RecentPayments";
import { useTranslations } from "next-intl";

export default function PaymentsPage() {
  const t = useTranslations("paymentsPage");

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="text-3xl font-bold text-white">{t("title")}</h1>
        <p className="mt-2 text-slate-400">
          {t("description")}
        </p>
      </div>
      <RecentPayments />
    </div>
  );
}
