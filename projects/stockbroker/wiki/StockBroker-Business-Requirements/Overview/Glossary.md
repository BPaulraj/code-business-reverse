> 🔄 **Generated** by the reverse-engineering kit from project `stockbroker` (code commit `ae607a6`, 2026-10-04, business view). **Do not edit this page**: changes are overwritten on the next publish. Give feedback through the review packs.

Business terms used in all requirement statements. A statement must use the **Term** column, never the code names.
Definitions marked **TBC** need product confirmation.

| Term | Definition | Code / DB names (aliases) | Source | Confirmed by product |
|---|---|---|---|---|
| Client | A person registered on the platform who funds a wallet and trades | `User`, `userId` | `packages/db/prisma/schema.prisma:10-24` | |
| Client account | The client's registration record: name, email, phone, address, KYC status, member since | `User` | `schema.prisma:10-24` | |
| KYC status | Know-your-customer verification state: Unverified, Pending or Verified. Displayed as "mock"; never changed by any code. | `kycStatus` (`UNVERIFIED`/`PENDING`/`VERIFIED`) | `schema.prisma:17`, `packages/shared/src/index.ts:19` | |
| Wallet | The client's single cash account, used to pay for purchases and receive sale proceeds | `Wallet`, `balance` | `schema.prisma:26-33` | |
| Wallet balance | Cash available in the wallet, in USD | `Wallet.balance` | `schema.prisma:29`, `packages/web/src/lib/format.ts:2` | |
| Wallet transaction | A credit or debit to the wallet (funding or trade settlement) | `Transaction` | `schema.prisma:35-46` | |
| Funding / add funds | Crediting the wallet from an external bank account or debit card (simulated) | `add-funds`, `payments`, method `BANK_TRANSFER` / `DEBIT_CARD` | `packages/server/src/modules/wallet/walletRoutes.ts:41-97` | |
| Funding method | How a wallet transaction originated: Bank transfer, Debit card, or Trade | `TransactionMethod` | `packages/shared/src/index.ts:14` | |
| IFSC-style branch code | Bank branch identifier: 4 letters, a zero, 6 letters or digits (Indian IFSC format) | `ifsc`, `IFSC_REGEX` | `packages/shared/src/index.ts:146` | |
| Company | A listed company whose shares can be traded (41 seeded) | `Company` | `schema.prisma:48-57`, `packages/db/prisma/seed.ts:5-47` | |
| Ticker | The short exchange symbol identifying a company, e.g. AAPL | `ticker` | `schema.prisma:50` | |
| Sector | The company's industry group, e.g. Technology | `sector` | `schema.prisma:52` | |
| Base price | Reference price of a company's share. The simulated market price varies around it. | `basePrice` | `schema.prisma:53` | |
| Market price (simulated) | The current share price shown or used: base price ±2%, newly drawn on every request | `simulatePrice`, `price`, `currentPrice` | `packages/db/src/services/priceService.ts:1-9` | |
| Quoted price | The price shown to the client when building an order. Not guaranteed. | `selected.price` | `packages/web/src/pages/Trade.tsx:265-266` | |
| Execution price | The price at which the trade is actually executed, set by the server at confirmation | `pricePerShare` | `packages/server/src/modules/trades/tradesRoutes.ts:36` | |
| Trade / order | A client's instruction to buy or sell a whole number of shares of one company, executed immediately | `Trade`, `TradeRequest` | `schema.prisma:72-86` | |
| Trade type | Buy or Sell | `TradeType` `BUY`/`SELL` | `packages/shared/src/index.ts:16` | |
| Trade total | Execution price × quantity, rounded to the cent | `total` | `tradesRoutes.ts:37` | |
| Holding / position | The number of shares of one company the client owns, with their average cost | `Holding` | `schema.prisma:59-70` | |
| Average cost | Weighted average purchase price per share of a holding | `avgCost` | `tradesRoutes.ts:58` | |
| Portfolio value / stock value | Sum of current market value of all holdings | `portfolioValue`, `stockValue` | `packages/server/src/modules/dashboard/dashboardRoutes.ts:30`, `packages/api/src/modules/portfolio/portfolioRoutes.ts:19` | |
| Gain / loss (unrealised) | Current value minus cost (average cost × quantity) | `gainLoss`, `gainLossPct` | `packages/db/src/services/holdingsService.ts:13-16` | |
| Invoice (contract note) | A document issued for every executed trade, downloadable as PDF | `Invoice` | `schema.prisma:88-95` | |
| Invoice number | Human-readable invoice reference, `INV-` + 8 characters | `invoiceNumber` | `packages/db/src/services/invoiceService.ts:3-4` | |
| Brokerage fee (illustrative) | 0.1% of trade total (min $0.50). Shown on the invoice only; **not charged** | `illustrativeFee` | `packages/db/src/services/invoicePdfService.ts:51-59` | |
| Inbox / message | In-app notifications to the client: System messages and Invoice messages | `InboxMessage`, `MessageType` | `schema.prisma:97-108` | |
| Session | The signed-in period of a client (7 days) | JWT `token` cookie / bearer `accessToken` | `packages/server/src/modules/auth/authRoutes.ts:14-24` | |
| Demo mode | Platform-wide statement that no real money or trades are involved | `DemoModeBadge` | `packages/web/src/components/ui.tsx:71-76` | |
