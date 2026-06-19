#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import zipfile
import argparse
from datetime import datetime
from pathlib import Path


VERSION = "0.2"
TOTAL_OFFICIAL_AUDIO = 16255
DEFAULT_PROJECT_ROOT_ENV = "DUBBING_007_PROJECT_ROOT"


MANIFEST_COLUMNS = [
    "source_hash",
    "asset_id",
    "chunk",
    "wem_path",
    "wem_size_bytes",
    "wem_sha1",
    "runtime_shape_ok",
    "target_it",
    "target_text_it_display",
    "target_text_it_tts",
    "source_duration_sec",
    "generated_duration_sec",
    "official_speaker_id",
    "official_speaker_name",
    "sourcefirst_policy",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha1_file(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def source_hash(row: dict[str, str]) -> str:
    value = row.get("source_hash") or row.get("hash") or row.get("_hash_norm") or ""
    return value.upper()


def chunk_name(row: dict[str, str]) -> str:
    for key in (
        row.get("actual_runtime_chunk", ""),
        row.get("chunk", ""),
        row.get("line_key", ""),
        row.get("asset_id", ""),
        row.get("job_id", ""),
    ):
        match = re.search(r"(chunk[01])", key or "", re.IGNORECASE)
        if match:
            return match.group(1).lower()
    raise RuntimeError(f"Cannot infer chunk for {source_hash(row)}")


def is_generated_wem(path_text: str) -> bool:
    lower = path_text.lower()
    blocked = [
        "\\runtime_dialogue_audio\\",
        "\\original_cache\\",
        "\\playable_cache\\",
        "\\audio\\original_cache\\",
        "\\audio\\playable_cache\\",
    ]
    return not any(token in lower for token in blocked)


def candidate_tokens(row: dict[str, str]) -> list[str]:
    fields = [
        "sourcefirst_batch",
        "production_batch_label",
        "promotion_pack",
        "repair_source_batch",
        "repair_source_pack",
        "round2_campaign",
        "source_pack_dir",
        "runtime_safe_manifest_path",
        "wem_path",
        "pre_marker_wem_path",
        "promotion_intersection_csv",
    ]
    tokens: list[str] = []
    for field in fields:
        value = row.get(field) or ""
        if not value:
            continue
        tokens.append(Path(value).name.lower())
        for part in re.split(r"[\\/]", value.lower()):
            if len(part) >= 8:
                tokens.append(part)
    return list(dict.fromkeys(tokens))


def rank_candidate(path: Path, row: dict[str, str]) -> int:
    lower = str(path).lower()
    score = 0
    if "\\production\\global_patch_with_approved_voices\\" in lower:
        score += 1000
    if "\\wem_marker_preserved\\" in lower:
        score += 700
    if "\\wem_marker\\" in lower:
        score += 600
    if "\\wem_work\\" in lower:
        score += 450
    if "\\wem_encoded\\" in lower:
        score += 350
    if "\\final\\" in lower:
        score += 250
    if lower.endswith(".wwes.wem"):
        score += 150
    if "\\converted\\windows\\" in lower:
        score -= 700
    if "\\backups\\" in lower or "\\original_segments\\" in lower:
        score -= 900
    if "vorbis_high" in lower or "_high_" in lower:
        score += 60
    if "vorbis_medium" in lower or "_medium_" in lower:
        score += 40
    if "vorbis_low" in lower or "_low_" in lower:
        score += 10
    for token in candidate_tokens(row):
        if token and token in lower:
            score += 80
    return score


def build_wem_index(root: Path, needed_hashes: set[str]) -> dict[str, list[Path]]:
    try:
        result = subprocess.run(
            ["rg", "--files", str(root), "-g", "*.wem"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        file_list = result.stdout.splitlines()
    except FileNotFoundError:
        file_list = [str(p) for p in root.rglob("*.wem")]

    by_hash = {h: [] for h in needed_hashes}
    pattern = re.compile(r"([0-9a-fA-F]{16})(?:\.WWES)?\.wem$")
    for item in file_list:
        if not is_generated_wem(item):
            continue
        match = pattern.search(item)
        if not match:
            continue
        h = match.group(1).upper()
        if h in by_hash:
            by_hash[h].append(Path(item))
    return by_hash


def safe_remove_tree(path: Path, repo_root: Path) -> None:
    resolved = path.resolve()
    root = repo_root.resolve()
    if not str(resolved).lower().startswith(str(root).lower() + os.sep):
        raise RuntimeError(f"Refusing to remove outside repo: {resolved}")
    if path.exists():
        shutil.rmtree(path)


def text_value(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = row.get(key) or ""
        if value:
            return value
    return ""


def progress_summary(progress_rows: list[dict[str, str]]) -> dict[str, str]:
    total = sum(int(float(r.get("total_audio") or 0)) for r in progress_rows)
    patched = sum(int(float(r.get("patched_audio") or 0)) for r in progress_rows)
    remaining = sum(int(float(r.get("remaining_audio") or 0)) for r in progress_rows)
    completion = (patched / total * 100) if total else 0
    bond = next((r for r in progress_rows if r.get("official_speaker_id") == "BOND"), {})
    return {
        "total": str(total),
        "patched": str(patched),
        "remaining": str(remaining),
        "completion": f"{completion:.2f}",
        "bond": f"{bond.get('patched_audio', '0')}/{bond.get('total_audio', '0')}",
    }


def write_progress_docs(repo: Path, progress_rows: list[dict[str, str]]) -> None:
    docs = repo / "docs"
    write_csv(docs / "progress_by_character.csv", progress_rows, list(progress_rows[0].keys()))
    summary = progress_summary(progress_rows)
    lines = [
        "# Progress by character - v0.2",
        "",
        f"- Total official audio: `{summary['total']}`",
        f"- Patched audio: `{summary['patched']}`",
        f"- Remaining audio: `{summary['remaining']}`",
        f"- Completion: `{summary['completion']}%`",
        "",
        "| Speaker | ID | Total | Patched | Remaining | % |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in progress_rows:
        lines.append(
            "| {name} | `{sid}` | {total} | {patched} | {remaining} | {pct}% |".format(
                name=row.get("official_speaker_name", ""),
                sid=row.get("official_speaker_id", ""),
                total=row.get("total_audio", ""),
                patched=row.get("patched_audio", ""),
                remaining=row.get("remaining_audio", ""),
                pct=row.get("patched_percent", ""),
            )
        )
    (docs / "progress_by_character.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_zip(repo: Path, output_zip: Path) -> None:
    if output_zip.exists():
        output_zip.unlink()
    include_roots = ["docs", "mod", "mod_manifest", "tools"]
    include_files = [
        ".gitignore",
        "install.ps1",
        "uninstall.ps1",
        "LICENSE",
        "NOTICE.md",
        "README.md",
        "RELEASE_NOTES.md",
        "PUBLISHING.md",
    ]
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name in include_files:
            path = repo / name
            if path.exists():
                zf.write(path, path.relative_to(repo).as_posix())
        for root_name in include_roots:
            root = repo / root_name
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.is_file():
                    zf.write(path, path.relative_to(repo).as_posix())


def public_path_hint(path: Path, project_root: Path) -> str:
    try:
        return path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return path.name


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the public release package from the local cumulative manifest.")
    parser.add_argument(
        "--project-root",
        default=os.environ.get(DEFAULT_PROJECT_ROOT_ENV, ""),
        help=f"Local 007 dubbing project root. Can also be set with ${DEFAULT_PROJECT_ROOT_ENV}.",
    )
    args = parser.parse_args()

    if not args.project_root:
        raise SystemExit(f"Set --project-root or ${DEFAULT_PROJECT_ROOT_ENV} before building this release.")

    repo = Path(__file__).resolve().parents[1]
    project_root = Path(args.project_root)
    production_root = project_root / "production" / "global_patch_with_approved_voices"
    cumulative_csv = production_root / "sourcefirst_runtime_applied_promoted_cumulative.csv"
    progress_csv = production_root / "007_full_official_speaker_progress_latest.csv"
    progress_md = production_root / "007_full_official_speaker_progress_latest.md"

    rows = read_csv(cumulative_csv)
    progress_rows = read_csv(progress_csv)
    if not rows:
        raise SystemExit("Cumulative CSV is empty")

    unique_rows: dict[str, dict[str, str]] = {}
    for row in rows:
        h = source_hash(row)
        if h:
            unique_rows[h] = row

    needed = set(unique_rows)
    wem_index = build_wem_index(project_root, needed)

    resolved: dict[str, Path] = {}
    missing: list[str] = []
    resolver_audit: list[dict[str, str]] = []
    for h, row in unique_rows.items():
        direct = Path(row.get("wem_path") or "")
        chosen: Path | None = direct if row.get("wem_path") and direct.exists() and is_generated_wem(str(direct)) else None
        source = "cumulative_wem_path" if chosen else ""
        if chosen is None:
            candidates = [p for p in wem_index.get(h, []) if p.exists()]
            if candidates:
                chosen = sorted(candidates, key=lambda p: rank_candidate(p, row), reverse=True)[0]
                source = "resolved_generated_candidate"
        if chosen is None:
            missing.append(h)
            continue
        resolved[h] = chosen
        resolver_audit.append(
            {
                "source_hash": h,
                "chunk": chunk_name(row),
                "resolver_source": source,
                "generated_path_hint": public_path_hint(chosen, project_root),
                "score": str(rank_candidate(chosen, row)),
                "official_speaker_id": row.get("official_speaker_id", ""),
                "official_speaker_name": row.get("official_speaker_name", ""),
            }
        )

    if missing:
        raise SystemExit(f"Missing generated WEM files for {len(missing)} hashes: {', '.join(missing[:20])}")

    mod_wem = repo / "mod" / "wem"
    safe_remove_tree(mod_wem, repo)
    (mod_wem / "chunk0").mkdir(parents=True, exist_ok=True)
    (mod_wem / "chunk1").mkdir(parents=True, exist_ok=True)

    manifest_rows: list[dict[str, str]] = []
    total_bytes = 0
    for h in sorted(unique_rows):
        row = unique_rows[h]
        chunk = chunk_name(row)
        src = resolved[h]
        dst = mod_wem / chunk / f"{h}.WWES.wem"
        shutil.copy2(src, dst)
        size = dst.stat().st_size
        total_bytes += size
        manifest_rows.append(
            {
                "source_hash": h,
                "asset_id": text_value(row, "asset_id", "job_id", "line_key"),
                "chunk": chunk,
                "wem_path": dst.relative_to(repo).as_posix(),
                "wem_size_bytes": str(size),
                "wem_sha1": sha1_file(dst),
                "runtime_shape_ok": text_value(row, "runtime_shape_ok") or "True",
                "target_it": text_value(row, "target_it", "final_spoken_text_it", "target_text_it_display"),
                "target_text_it_display": text_value(
                    row,
                    "target_text_it_display",
                    "subtitle_text_it",
                    "subtitle_adapted_it_text",
                    "target_it",
                ),
                "target_text_it_tts": text_value(
                    row,
                    "target_text_it_tts",
                    "final_spoken_text_it",
                    "target_it",
                    "target_text_it_display",
                ),
                "source_duration_sec": text_value(row, "source_duration_sec", "source_duration_sec_float"),
                "generated_duration_sec": text_value(row, "generated_duration_sec", "generated_duration_sec_float"),
                "official_speaker_id": row.get("official_speaker_id", ""),
                "official_speaker_name": row.get("official_speaker_name", ""),
                "sourcefirst_policy": text_value(row, "sourcefirst_policy")
                or "source_audio_acting_authority;approved_voice_identity_authority;no_accent_polish",
            }
        )

    write_csv(repo / "mod_manifest" / "runtime_wem_manifest.csv", manifest_rows, MANIFEST_COLUMNS)
    (repo / "mod_manifest" / "runtime_wem_manifest.json").write_text(
        json.dumps(
            {
                "version": VERSION,
                "rows": len(manifest_rows),
                "total_bytes": total_bytes,
                "manifest": "mod_manifest/runtime_wem_manifest.csv",
                "built_at": datetime.now().isoformat(timespec="seconds"),
                "source_cumulative_csv": cumulative_csv.name,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_csv(repo / "mod_manifest" / "wem_resolver_audit_v0.2.csv", resolver_audit, list(resolver_audit[0].keys()))
    write_progress_docs(repo, progress_rows)

    if progress_md.exists():
        shutil.copy2(progress_md, repo / "LOCAL_PRODUCTION_STATUS.md")

    output_zip = repo.parent / f"007-first-light-italian-dub-v{VERSION}.zip"
    make_zip(repo, output_zip)

    print(json.dumps(
        {
            "version": VERSION,
            "manifest_rows": len(manifest_rows),
            "mod_wem_files": len(list(mod_wem.rglob("*.wem"))),
            "total_bytes": total_bytes,
            "zip": str(output_zip),
            "zip_bytes": output_zip.stat().st_size,
        },
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
