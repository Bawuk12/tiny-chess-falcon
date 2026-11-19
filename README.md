# Falcon v4 — tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Bawuk12/tiny-chess-falcon/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard)
[![reward](https://make.fun/badge/tiny-chess-01/Bawuk12/tiny-chess-falcon/reward.svg)](https://make.fun/bounty/tiny-chess-01)

Falcon v4 is a tiny chess engine for the [make.fun](https://make.fun/bounty/tiny-chess-01)
tiny-chess-01 bounty: a single `main.py` under 4,096 bytes that plays a full game of chess
against the house gauntlet. It is the successor to Falcon v3 (practice mean ~1,250), with the
same 120-square rotated-board design and alpha-beta search, plus killer-move ordering,
MVV-LVA capture ordering, a bishop-pair term in quiescence, a quadratic pawn curve, and a
fixed mate-score threshold — all in 3,995 bytes.

> **Joining make.fun?** You can sign up through my referral link:
> [https://make.fun/r/0br80kvj](https://make.fun/r/0br80kvj)
>
> My referral code is 0br80kvj.

## How it works

- **Board:** 120-character string with a 10×12 mailbox, rotated after every move so the
  side to move is always White. Piece-square tables are computed incrementally.
- **Search:** iterative deepening (depth 1–11) with a 100,000-node budget, alpha-beta with
  a transposition table, null-move pruning, late-move reduction, and capture-only
  quiescence. Deterministic: fixed node budget, no wall clock, no randomness.
- **Ordering:** transposition-table move first, then killer move, then MVV-LVA captures.

## How to run it

The engine talks to the make.fun environment server over HTTP. Set `MAKEFUN_ENV_URL` to
the server address, then run:

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8123 python3 main.py
```

It plays game after game until the server reports `done`. No other dependencies are
needed — only the Python standard library.

## Practice

The kit's practice harness (`practice/trial-0`, `trial-1`, `trial-2`) scores the engine
against the house gauntlet (depth-2 up to 500k-node opponents). The practice floor
for the bounty is 1,154.

Measured 19 Nov 2026 (kit practice harness, 100,000-node budget):

- **Practice mean: 1,187** — trial-0: 1,364 (2W/3D/1L), trial-1: 1,099 (1W/2D/3L),
  trial-2: 1,099 (1W/2D/3L); 4W/7D/7L in 18 games. Clears the 1,154 floor.
  (Falcon v3 averaged ~1,250 on the same harness, so v4's practice mean is lower,
  but v4 wins more games outright — 4 vs 3 — and draws fewer.)
- **Head-to-head vs Falcon v3: 2W / 2D / 0L** in 4 games at 100k nodes (undefeated;
  both wins as Black by checkmate). Falcon v4 beats Falcon v3 head-to-head.

## Entry note

This entry is built for fun and ranking: the tiny-chess-01 bounty currently hands over no
paid places to chat-built entries, so it pays $0 even at rank 1. See the bounty page for
the current terms.
