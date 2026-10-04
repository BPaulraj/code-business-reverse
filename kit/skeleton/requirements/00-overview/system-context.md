# System Context

`/re-discover` fills this in. It gives a business-level view of the platform: its components, the shared database, and the third parties it connects to.

## Components

| Component | One-line business purpose | Confidence | Details |
|---|---|---|---|

## Context diagram

```mermaid
flowchart LR
    U[Client users] --> FE[Front-end website]
    O[Operations users] --> BO[Back-office website]
    FE --> WS[Web services / REST API]
    WS --> BO
    WS --> DB[(Shared database)]
    WS --> CLI[Client service]
    WS --> CSH[Cash service]
    WS --> STK[Stock service]
    BO --> CLI
    CLI --> DB
    CSH --> DB
    STK --> DB
    SCH[Scheduler] --> BAT[Nightly batch jobs]
    BAT --> DB
    BAT --> FILES[/Output files/]
    CON[Connectivity] --> EXT[Third parties]
    FILES --> CON
```

## Interactions

| From | To | Mechanism (REST / event / DB / file) | Business reason | Evidence |
|---|---|---|---|---|

## Candidate end-to-end processes

| Proposed ID | Process | Likely entry point | Components |
|---|---|---|---|
