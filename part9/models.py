from __future__ import annotations
from typing import List, Dict, Any, Tuple

class Sonnet:
    def __init__(self, sonnet_data: Dict[str, Any]):
        self.title = sonnet_data["title"]
        self.lines = sonnet_data["lines"]

    @staticmethod
    def find_spans(text: str, pattern: str) -> List[Tuple[int, int]]:
        spans = []
        if not pattern:
            return spans
        for i in range(len(text) - len(pattern) + 1):
            if text[i:i + len(pattern)] == pattern:
                spans.append((i, i + len(pattern)))
        return spans

    def search_for(self, query: str) -> SearchResult:
        title_raw = str(self.title)
        q = query.lower()
        title_spans = Sonnet.find_spans(title_raw.lower(), q)

        line_matches = []
        for idx, line_raw in enumerate(self.lines, start=1):
            spans = Sonnet.find_spans(line_raw.lower(), q)
            if spans:
                line_matches.append(LineMatch(idx, line_raw, spans))

        total = len(title_spans) + sum(len(lm.spans) for lm in line_matches)
        return SearchResult(title_raw, title_spans, line_matches, total)


class LineMatch:
    def __init__(self, line_no: int, text: str, spans: List[Tuple[int, int]]):
        self.line_no = line_no
        self.text = text
        self.spans = spans

    def copy(self) -> LineMatch:
        return LineMatch(self.line_no, self.text, list(self.spans))

class SearchResult:
    def __init__(self, title: str, title_spans: List[Tuple[int, int]], line_matches: List[LineMatch], matches: int) -> None:
        self.title = title
        self.title_spans = title_spans
        self.line_matches = line_matches
        self.matches = matches

    def copy(self) -> SearchResult:
        return SearchResult(self.title, list(self.title_spans), [lm.copy() for lm in self.line_matches], self.matches)

    def combine_with(self, other: SearchResult) -> SearchResult:
        combined = self.copy()
        combined.matches = self.matches + other.matches
        combined.title_spans = sorted(self.title_spans + other.title_spans)

        lines_by_no = {lm.line_no: lm.copy() for lm in self.line_matches}
        for lm in other.line_matches:
            ln = lm.line_no
            if ln in lines_by_no:
                lines_by_no[ln].spans.extend(lm.spans)
            else:
                lines_by_no[ln] = lm.copy()

        combined.line_matches = sorted(lines_by_no.values(), key=lambda lm: lm.line_no)
        return combined

    @staticmethod
    def ansi_highlight(text: str, spans: List[Tuple[int, int]], hl_mode: str = "DEFAULT") -> str:
        if not spans:
            return text

        spans = sorted(spans)
        merged = []

        current_start, current_end = spans[0]
        for s, e in spans[1:]:
            if s <= current_end:
                current_end = max(current_end, e)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = s, e
        merged.append((current_start, current_end))

        if hl_mode == "GREEN":
            color_code = "\033[1;92m"
        else:
            color_code = "\033[43m\033[30m"

        out = []
        i = 0
        for s, e in merged:
            out.append(text[i:s])
            out.append(color_code)
            out.append(text[s:e])
            out.append("\033[0m")
            i = e
        out.append(text[i:])
        return "".join(out)

    def print(self, idx: int, highlight: bool, total_docs: int, hl_mode: str = "DEFAULT") -> None:
        title_line = SearchResult.ansi_highlight(self.title, self.title_spans, hl_mode) if highlight else self.title
        print(f"\n[{idx}/{total_docs}] {title_line}")
        for lm in self.line_matches:
            line_out = SearchResult.ansi_highlight(lm.text, lm.spans, hl_mode) if highlight else lm.text
            print(f"  [{lm.line_no:2}] {line_out}")


