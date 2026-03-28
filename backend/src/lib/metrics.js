import client from "prom-client";

// Create a Registry which registers the metrics
const register = new client.Registry();

// Add a default label which is added to all metrics
register.setDefaultLabels({
  app: "stellar-payment-api",
});

// Enable the collection of default metrics
client.collectDefaultMetrics({ register });

/**
 * Payment Metrics
 */

export const paymentCreatedCounter = new client.Counter({
  name: "payment_created_total",
  help: "Total number of payment sessions created",
  labelNames: ["asset"],
});

export const paymentConfirmedCounter = new client.Counter({
  name: "payment_confirmed_total",
  help: "Total number of payments confirmed on the Stellar network",
  labelNames: ["asset"],
});

export const paymentFailedCounter = new client.Counter({
  name: "payment_failed_total",
  help: "Total number of failed payment attempts",
  labelNames: ["asset", "reason"],
});

export const paymentConfirmationLatency = new client.Histogram({
  name: "payment_confirmation_latency_seconds",
  help: "Time from payment creation to confirmation in seconds",
  labelNames: ["asset"],
  buckets: [10, 30, 60, 120, 300, 600, 1800, 3600], // Buckets in seconds
});

// Register custom metrics
register.registerMetric(paymentCreatedCounter);
register.registerMetric(paymentConfirmedCounter);
register.registerMetric(paymentFailedCounter);
register.registerMetric(paymentConfirmationLatency);

export { register };
