import { beforeEach, describe, expect, it, vi } from "vitest";

const {
  frontendStellarSdkPath,
  nativeAsset,
  textMemo,
  pathPaymentStrictReceiveOperation,
  transactionBuilderFactory,
  loadAccount,
} = vi.hoisted(() => ({
  frontendStellarSdkPath:
    "/Users/marvellous/Desktop/Stellar_Payment_API/frontend/node_modules/stellar-sdk/lib/index.js",
  nativeAsset: { type: "native" },
  textMemo: vi.fn(),
  pathPaymentStrictReceiveOperation: vi.fn(),
  transactionBuilderFactory: vi.fn(),
  loadAccount: vi.fn(),
}));

vi.mock(frontendStellarSdkPath, () => {
  class MockAsset {
    constructor(code, issuer) {
      this.code = code;
      this.issuer = issuer;
      this.type = "credit";
    }

    static native() {
      return nativeAsset;
    }
  }

  return {
    Asset: MockAsset,
    BASE_FEE: "100",
    Memo: {
      text: textMemo,
      id: vi.fn(),
      hash: vi.fn(),
      return: vi.fn(),
    },
    Horizon: {
      Server: vi.fn(() => ({
        loadAccount,
      })),
    },
    Operation: {
      payment: vi.fn(),
      pathPaymentStrictReceive: pathPaymentStrictReceiveOperation,
    },
    TransactionBuilder: transactionBuilderFactory,
  };
});

describe("frontend Stellar path payment builder", () => {
  beforeEach(() => {
    vi.resetModules();
    vi.clearAllMocks();
  });

  it("builds a strict-receive path payment with memo for an XLM to USDC invoice", async () => {
    const addOperation = vi.fn();
    const addMemo = vi.fn();
    const setTimeout = vi.fn();
    const build = vi.fn();

    addOperation.mockReturnThis();
    addMemo.mockReturnThis();
    setTimeout.mockReturnThis();
    build.mockReturnValue({
      toXDR: () => "AAAA-path-payment-xdr",
    });

    transactionBuilderFactory.mockImplementation(() => ({
      addOperation,
      addMemo,
      setTimeout,
      build,
    }));

    loadAccount.mockResolvedValue({
      accountId: () => "GTESTSOURCEACCOUNT",
      sequence: "1234567890",
    });

    textMemo.mockImplementation((value) => ({ type: "text", value }));
    pathPaymentStrictReceiveOperation.mockImplementation((params) => ({
      type: "path_payment_strict_receive",
      ...params,
    }));

    const { buildPathPaymentTransaction } = await import(
      "../../../frontend/src/lib/stellar.ts"
    );

    const xdr = await buildPathPaymentTransaction({
      sourcePublicKey: "GTESTSOURCEACCOUNT",
      destinationPublicKey: "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
      sendMax: "60.7262500",
      sendAssetCode: "XLM",
      sendAssetIssuer: null,
      destAmount: "25.0000000",
      destAssetCode: "USDC",
      destAssetIssuer: "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
      path: [],
      memo: "invoice-123",
      memoType: "text",
      horizonUrl: "https://horizon-testnet.stellar.org",
      networkPassphrase: "Test SDF Network ; September 2015",
    });

    expect(pathPaymentStrictReceiveOperation).toHaveBeenCalledWith({
      sendAsset: nativeAsset,
      sendMax: "60.7262500",
      destination: "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
      destAsset: expect.objectContaining({
        type: "credit",
        code: "USDC",
        issuer: "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
      }),
      destAmount: "25.0000000",
      path: [],
    });
    expect(textMemo).toHaveBeenCalledWith("invoice-123");
    expect(addMemo).toHaveBeenCalledWith({ type: "text", value: "invoice-123" });
    expect(xdr).toBe("AAAA-path-payment-xdr");
  });
});
