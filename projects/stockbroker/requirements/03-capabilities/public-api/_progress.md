# Progress — public-api

Cross-cutting behaviour extracted first: token auth, CORS, errors.

- [x] 1 `POST /api/v1/users` — `packages/api/src/modules/users/usersRoutes.ts:12`
- [x] 2 `GET /api/v1/users/me` — `usersRoutes.ts:48`
- [x] 3 `PUT /api/v1/users/me` — `usersRoutes.ts:58`
- [x] 4 `POST /api/v1/sessions` — `packages/api/src/modules/sessions/sessionsRoutes.ts:11`
- [x] 5 `GET /api/v1/companies` — `packages/api/src/modules/companies/companiesRoutes.ts:11`
- [x] 6 `GET /api/v1/portfolio` — `packages/api/src/modules/portfolio/portfolioRoutes.ts:10`
- [x] 7 `GET /api/v1/portfolio/holdings` — `portfolioRoutes.ts:31`
- [x] 8 `GET /api/v1/wallet/balance` — `packages/api/src/modules/wallet/walletRoutes.ts:12`
- [x] 9 `POST /api/v1/payments` — `packages/api/src/modules/payments/paymentsRoutes.ts:13`
- [x] 10 `GET /api/v1/trades` — `packages/api/src/modules/trades/tradesRoutes.ts:12`
- [x] 11 `POST /api/v1/trades` — `tradesRoutes.ts:24`
- [x] 12 `GET /api/v1/invoices/by-trade/{tradeId}` — `packages/api/src/modules/invoices/invoicesRoutes.ts:11`
- [x] 13 `GET /api/v1/invoices/{invoiceId}/pdf` — `invoicesRoutes.ts:30`
- [x] 14 `GET /api/v1/inbox` — `packages/api/src/modules/inbox/inboxRoutes.ts:11`
- [x] 15 `GET /api/v1/inbox/{id}` — `inboxRoutes.ts:22`
- [x] 16 docs — `packages/api/src/docs.ts:15`
- [x] 17 health — `packages/api/src/index.ts:25`
