#!/usr/bin/env python3
"""
Part 9 CLI.
"""

from typing import List
import time

from .constants import BANNER, HELP
from .models import Sonnet, SearchResult
from .file_utilities import load_config, load_sonnets


def print_results(
    query: str,
    results: List[SearchResult],
    highlight: bool,
    hl_mode: str,
    query_time_ms: float | None = None,
) -> None:
    total_docs = len(results)
    matched = [r for r in results if r.matches > 0]

    line = f'{len(matched)} out of {total_docs} sonnets contain "{query}".'
    if query_time_ms is not None:
        line += f" Your query took {query_time_ms:.2f}ms."
    print(line)

    for idx, r in enumerate(matched, start=1):
        r.print(idx, highlight, total_docs, hl_mode)


def main() -> None:
    print(BANNER)
    config = load_config()

    start = time.perf_counter()
    sonnets = load_sonnets()

    elapsed = (time.perf_counter() - start) * 1000
    print(f"Loading sonnets took: {elapsed:.3f} [ms]")

    print(f"Loaded {len(sonnets)} sonnets.")

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not raw:
            continue

        if raw.startswith(":"):
            if raw == ":quit":
                print("Bye.")
                break

            if raw == ":help":
                print(HELP)
                continue

            if raw.startswith(":highlight"):
                parts = raw.split()
                if len(parts) == 2 and parts[1].lower() in ("on", "off"):
                    config.highlight = parts[1].lower() == "on"
                    print("Highlighting", "ON" if config.highlight else "OFF")
                    config.save()
                else:
                    print("Usage: :highlight on|off")
                continue

            if raw.startswith(":search-mode"):
                parts = raw.split()
                if len(parts) == 2 and parts[1].upper() in ("AND", "OR"):
                    config.search_mode = parts[1].upper()
                    print("Search mode set to", config.search_mode)
                    config.save()
                else:
                    print("Usage: :search-mode AND|OR")
                continue

            if raw.startswith(":hl-mode"):
                parts = raw.split()
                if len(parts) == 2 and parts[1].upper() in ("DEFAULT", "GREEN"):
                    config.hl_mode = parts[1].upper()
                    print("Highlight mode set to", config.hl_mode)
                    config.save()
                else:
                    print("Usage: :hl-mode DEFAULT|GREEN")
                continue

            print("Unknown command. Type :help for commands.")
            continue

        words = raw.split()
        if not words:
            continue

        start = time.perf_counter()

        combined_results = []

        for word in words:
            results = [s.search_for(word) for s in sonnets]

            if not combined_results:
                combined_results = results
            else:
                for i in range(len(combined_results)):
                    combined_result = combined_results[i]
                    result = results[i]

                    if config.search_mode == "AND":
                        if combined_result.matches > 0 and result.matches > 0:
                            combined_results[i] = combined_result.combine_with(result)
                        else:
                            combined_result.matches = 0
                    elif config.search_mode == "OR":
                        combined_results[i] = combined_result.combine_with(result)

        elapsed_ms = (time.perf_counter() - start) * 1000

        print_results(raw, combined_results, config.highlight, config.hl_mode, elapsed_ms)


if __name__ == "__main__":
    main()