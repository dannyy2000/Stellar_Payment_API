import 'dotenv/config';
import express from "express";
import morgan from "morgan";
import cors from "cors";
import swaggerJsdoc from "swagger-jsdoc";
import swaggerUi from "swagger-ui-express";
import paymentsRouter from "./routes/payments.js";
import merchantsRouter from "./routes/merchants.js";
import { requireApiKeyAuth } from "./lib/auth.js";
import { supabase } from "./lib/supabase.js";

const app = express();
const port = process.env.PORT || 4000;

const swaggerSpec = swaggerJsdoc({
  definition: {
    openapi: "3.0.0",
    info: {
      title: "Stellar Payment API",
      version: "0.1.0",
      description: "API for creating and verifying Stellar network payments"
    },
    servers: [{ url: `http://localhost:${port}` }]
  },
  apis: ["./src/routes/*.js"]
});

app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));

app.use(cors({
  origin: "http://localhost:3000"
}));

app.use(express.json({ limit: "1mb" }));
app.use(morgan("dev"));

app.get("/health", async (req, res) => {
  try {
    const { error } = await supabase.from("merchants").select("id").limit(1);

    if (error) {
      return res.status(503).json({
        ok: false,
        service: "stellar-payment-api",
        error: "Database unavailable"
      });
    }

    res.json({ ok: true, service: "stellar-payment-api" });
  } catch {
    res.status(503).json({
      ok: false,
      service: "stellar-payment-api",
      error: "Database unavailable"
    });
  }
});

app.use("/api/create-payment", requireApiKeyAuth());
app.use("/api/rotate-key", requireApiKeyAuth());
app.use("/api", paymentsRouter);
app.use("/api", merchantsRouter);

app.use((err, req, res, next) => {
  const status = err.status || 500;
  res.status(status).json({
    error: err.message || "Internal Server Error"
  });
});

app.listen(port, () => {
  console.log(`API listening on http://localhost:${port}`);
});
