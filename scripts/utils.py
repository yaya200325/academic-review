import json
import hashlib


def deduplicate_papers(papers: list) -> list:
    seen = set()
    result = []
    for p in papers:
        pid = p.get("paperId") or ""
        doi = (p.get("externalIds") or {}).get("DOI") or ""
        if pid:
            key = pid
        elif doi:
            key = doi
        else:
            title = (p.get("title") or "").lower().strip()[:60]
            year = str(p.get("year") or "")
            key = hashlib.md5((title + year).encode()).hexdigest()
        if key and key not in seen:
            seen.add(key)
            result.append(p)
    return result


def build_paper_lookup(knowledge: list) -> dict:
    return {k["paper_id"]: k for k in knowledge if k.get("paper_id")}


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path: str) -> None:
    import os
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_list_from_response(raw: str) -> list:
    parsed = json.loads(raw)
    if isinstance(parsed, list):
        return parsed
    if isinstance(parsed, dict):
        for v in parsed.values():
            if isinstance(v, list):
                return v
    return []
