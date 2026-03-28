import rateLimit from "express-rate-limit";
import { RedisStore } from "rate-limit-redis";

export const RATE_LIMIT_REDIS_PREFIX = "rl:";

export function createRedisRateLimitStore({
  client,
  StoreClass = RedisStore,
  prefix = RATE_LIMIT_REDIS_PREFIX,
} = {}) {
  return new StoreClass({
    sendCommand: (...args) => client.sendCommand(args),
    prefix,
  });
}

export function createVerifyPaymentRateLimit({
  store,
  rateLimitFactory = rateLimit,
} = {}) {
  return rateLimitFactory({
    windowMs: 15 * 60 * 1000,
    max: 10,
    message: {
      error: "Too many verification requests, please try again later.",
    },
    standardHeaders: true,
    legacyHeaders: false,
    store,
  });
}

export function createMerchantRegistrationRateLimit({
  store,
  rateLimitFactory = rateLimit,
} = {}) {
  return rateLimitFactory({
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 5, // 5 registration attempts per hour per IP
    message: {
      error: "Too many registration attempts, please try again later.",
    },
    standardHeaders: true,
    legacyHeaders: false,
    store,
    keyGenerator: (req) => {
      // Rate limit by IP address
      return req.ip || req.connection.remoteAddress;
    },
  });
}
