import { Resend } from "resend";

/** @type {Resend | null} */
let resend = null;

function getClient() {
  if (!resend) {
    resend = new Resend(process.env.RESEND_API_KEY);
  }
  return resend;
}

const FROM_ADDRESS =
  process.env.RECEIPT_FROM_EMAIL || "receipts@notifications.dripsnetwork.com";

/**
 * Sends a receipt email via Resend.
 *
 * @param {{ to: string, subject: string, html: string }} options
 * @returns {Promise<{ ok: boolean, error?: unknown }>}
 */
export async function sendReceiptEmail({ to, subject, html }) {
  try {
    const client = getClient();
    const { error } = await client.emails.send({
      from: FROM_ADDRESS,
      to,
      subject,
      html,
    });

    if (error) {
      return { ok: false, error };
    }

    return { ok: true };
  } catch (err) {
    return { ok: false, error: err };
  }
}
