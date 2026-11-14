# Implementation & provenance notes

This repository is a curated presentation of a university AI coursework solution, not a production transit navigation service.

## Original coursework vs. portfolio additions

| Item | Origin |
| --- | --- |
| `SearchAlgorithm.py` | Submitted university coursework implementation, based on the provided assignment scaffold |
| `SubwayMap.py`, `utils.py` | Helper modules supplied with the coursework (included for reproducibility) |
| `CityInformation/` | Teaching datasets supplied with the coursework (Lyon and a simplified Barcelona network) |
| `demo.py`, `tests/test_routes.py` | Added to this portfolio edition for easy execution and reproducible examples |
| `assets/barcelona-example.png` | New diagram generated from the included sample-network data |

The original ZIP also contained an IDE configuration, an entire Windows Python virtual environment, copies of utility files, a course test suite and exam-practice scripts. These have **not** been included.

## Changes made for this presentation

- Removed a student identifier from the source header; the original algorithm implementation is otherwise retained.
- Added a defensive fallback in `Astar` so an unreachable destination returns `None` instead of raising an `IndexError` when the frontier is exhausted.
- Added a standalone command-line demo with station IDs and an optional coordinate-based A* example.
- Added independent smoke tests, separate from the course test suite.

## Verification

- The **original uploaded implementation**, before the portfolio adjustment, passed **12/12 supplied university unit tests** in a local environment with Python and NumPy. That suite is intentionally not republished here.
- The included portfolio smoke tests were run locally; see `python -m unittest discover -s tests -v`.
- No benchmark claims or real-world map accuracy claims are made.

## Limits

- This is a teaching dataset, not the current Barcelona transit network.
- DFS is not guaranteed to find a lowest-cost path. BFS minimizes unweighted number of edges; it does not minimize travel time.
- A* optimality depends on the cost definition, graph assumptions, and admissibility of the heuristic; no universal guarantee is claimed for all networks.
- The map geometry and the velocity conventions follow the coursework model.
- Before making the repository public, confirm that the university-supplied helper files and sample datasets may be redistributed and that collaborators agree to publication where applicable.
