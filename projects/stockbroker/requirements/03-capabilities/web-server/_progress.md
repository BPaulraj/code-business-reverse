# Progress — web-server

Cross-cutting behaviour extracted first: auth, scoping, error handling.

- [x] 1 `POST /api/auth/register` — `packages/server/src/modules/auth/authRoutes.ts:26`
- [x] 2 `POST /api/auth/login` — `authRoutes.ts:62`
- [x] 3 `POST /api/auth/logout` — `authRoutes.ts:82`
- [x] 4 `GET /api/auth/me` — `authRoutes.ts:87`
- [x] 5 `PUT /api/auth/profile` — `authRoutes.ts:99`
- [x] 6 `GET /api/dashboard/summary` — `packages/server/src/modules/dashboard/dashboardRoutes.ts:12`
- [x] 7 `GET /api/holdings` — `packages/server/src/modules/holdings/holdingsRoutes.ts:10`
- [x] 8 `GET /api/companies` — `packages/server/src/modules/companies/companiesRoutes.ts:12`
- [x] 9 `GET /api/wallet` — `packages/server/src/modules/wallet/walletRoutes.ts:20`
- [x] 10 `GET /api/wallet/transactions` — `walletRoutes.ts:29`
- [x] 11 `POST /api/wallet/add-funds` — `walletRoutes.ts:41`
- [x] 12 `GET /api/trades` — `packages/server/src/modules/trades/tradesRoutes.ts:13`
- [x] 13 `POST /api/trades` — `tradesRoutes.ts:25`
- [x] 14 `GET /api/invoices` — `packages/server/src/modules/invoices/invoicesRoutes.ts:12`
- [x] 15 `GET /api/invoices/:id/pdf` — `invoicesRoutes.ts:24`
- [x] 16 `GET /api/inbox` — `packages/server/src/modules/inbox/inboxRoutes.ts:13`
- [x] 17 `GET /api/inbox/unread-count` — `inboxRoutes.ts:24`
- [x] 18 `PATCH /api/inbox/:id` — `inboxRoutes.ts:34`
- [x] 19 `GET /api/health` — `packages/server/src/index.ts:22`
