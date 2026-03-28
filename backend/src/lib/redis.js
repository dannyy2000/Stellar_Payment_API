import { createClient } from "redis";

let redisClient;

export function getRedisClient({
  redisUrl = process.env.REDIS_URL,
  clientFactory = createClient,
} = {}) {
  if (!redisClient) {
    redisClient = clientFactory({ url: redisUrl });
    redisClient.on("error", (err) => {
      console.error("Redis client error:", err.message);
    });
  }
  return redisClient;
}

export async function connectRedisClient(options) {
  const client = getRedisClient(options);
  if (!client.isOpen) {
    await client.connect();
  }
  return client;
}

export async function closeRedisClient() {
  if (!redisClient) {
    return;
  }
  if (redisClient.isOpen) {
    await redisClient.close();
  }
}

export function resetRedisClientForTests() {
  redisClient = undefined;
}

// ---------------------------------------------------------------------------
// Payment status cache helpers
// ---------------------------------------------------------------------------

/** TTL in seconds for payment-status cache entries. */
export const PAYMENT_STATUS_TTL = 2;

/** Consistent cache key for a payment-status entry. */
export function paymentCacheKey(id) {
  return `payment:status:${id}`;
}

/**
 * Return the cached payment object, or null on miss / Redis unavailable.
 * @param {import("redis").RedisClientType} client
 * @param {string} id  payment UUID
 */
export async function getCachedPayment(client, id) {
  try {
    const raw = await client.get(paymentCacheKey(id));
    return raw ? JSON.parse(raw) : null;
  } catch (err) {
    // Never let a cache failure block the request
    console.error("Redis GET error:", err.message);
    return null;
  }
}

/**
 * Store a payment object in the cache with a ~2 s TTL.
 * @param {import("redis").RedisClientType} client
 * @param {string} id  payment UUID
 * @param {object} data  the payment row to cache
 */
export async function setCachedPayment(client, id, data) {
  try {
    await client.set(paymentCacheKey(id), JSON.stringify(data), {
      EX: PAYMENT_STATUS_TTL,
    });
  } catch (err) {
    console.error("Redis SET error:", err.message);
  }
}

/**
 * Invalidate the cache entry for a payment (call after any write).
 * @param {import("redis").RedisClientType} client
 * @param {string} id  payment UUID
 */
export async function invalidatePaymentCache(client, id) {
  try {
    await client.del(paymentCacheKey(id));
  } catch (err) {
    console.error("Redis DEL error:", err.message);
  }
}