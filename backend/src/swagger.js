import path from "node:path";
import { fileURLToPath } from "node:url";
import swaggerJsdoc from "swagger-jsdoc";

const swaggerFilePath = fileURLToPath(import.meta.url);
const swaggerDirectory = path.dirname(swaggerFilePath);
const routeGlobs = [path.join(swaggerDirectory, "routes/*.js")];

export function createSwaggerDefinition({
  serverUrl = "http://localhost:4000",
} = {}) {
  return {
    openapi: "3.0.0",
    info: {
      title: "Stellar Payment API",
      version: "0.1.0",
      description: "API for creating and verifying Stellar network payments",
    },
    servers: [{ url: serverUrl }],
  };
}

export function createSwaggerSpec(options = {}) {
  return swaggerJsdoc({
    definition: createSwaggerDefinition(options),
    apis: routeGlobs,
  });
}

export const swaggerDocument = createSwaggerSpec();
