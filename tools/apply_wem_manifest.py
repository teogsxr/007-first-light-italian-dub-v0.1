#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


XOR_KEY = bytes([0xDC, 0x45, 0xA6, 0x9C, 0xD3, 0x72, 0x4C, 0xAB])


@dataclass
class Entry:
    index: int
    hash_text: str
    typ: str
    data_offset: int
    data_size_raw: int
    stored_size: int
    size_final: int
    xored: bool
    lz4ed: bool
    data_offset_field_offset: int
    data_size_raw_field_offset: int
    size_final_offset: int
    reference_table_size: int


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha1_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest().upper()


def apply_xor(data: bytes) -> bytes:
    return bytes(b ^ XOR_KEY[i % len(XOR_KEY)] for i, b in enumerate(data))


def parse_rpkg_entries(path: Path) -> dict[str, Entry]:
    entries: dict[str, Entry] = {}
    with path.open("rb") as f:
        if f.read(4) != b"2KPR":
            raise SystemExit(f"Unexpected RPKG magic: {path}")
        f.read(9)
        hash_count, hash_header_table_size, _ = struct.unpack("<III", f.read(12))
        hash_table_offset = 25
        resource_table_offset = hash_table_offset + hash_header_table_size

        headers = []
        f.seek(hash_table_offset)
        for index in range(hash_count):
            hash_record_offset = f.tell()
            hash_value, data_offset, data_size_raw = struct.unpack("<QQI", f.read(20))
            headers.append((index, hash_record_offset, hash_value, data_offset, data_size_raw))

        f.seek(resource_table_offset)
        for index, hash_record_offset, hash_value, data_offset, data_size_raw in headers:
            resource_record_offset = f.tell()
            raw = f.read(20)
            if len(raw) != 20:
                raise SystemExit(f"Short resource record in {path.name} index {index}")
            typ = raw[:4][::-1].decode("ascii", errors="replace")
            reference_table_size, size_final, _mem, _vmem = struct.unpack("<IIII", raw[4:20])
            if reference_table_size:
                f.seek(reference_table_size, 1)
            lz4ed = (data_size_raw & 0x3FFFFFFF) != 0
            xored = (data_size_raw & 0x80000000) != 0
            stored_size = (data_size_raw & 0x3FFFFFFF) if lz4ed else size_final
            entries[f"{hash_value:016X}"] = Entry(
                index=index,
                hash_text=f"{hash_value:016X}",
                typ=typ,
                data_offset=data_offset,
                data_size_raw=data_size_raw,
                stored_size=stored_size,
                size_final=size_final,
                xored=xored,
                lz4ed=lz4ed,
                data_offset_field_offset=hash_record_offset + 8,
                data_size_raw_field_offset=hash_record_offset + 16,
                size_final_offset=resource_record_offset + 8,
                reference_table_size=reference_table_size,
            )
    return entries


def read_runtime_resource(path: Path, entry: Entry) -> bytes:
    with path.open("rb") as f:
        f.seek(entry.data_offset)
        data = f.read(entry.stored_size)
    if entry.xored:
        data = apply_xor(data)
    if entry.lz4ed:
        raise SystemExit(f"LZ4 resource read not supported: {entry.hash_text}")
    return data


def ensure_game_not_running() -> None:
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-Process -Name 007FirstLight -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id",
            ],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return
    if result.returncode == 0 and result.stdout.strip():
        raise SystemExit(f"007FirstLight is running; close it before patching. PID: {result.stdout.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply generated Italian WEM files to 007 First Light RPKG chunks.")
    parser.add_argument("--game-path", default=r"C:\Program Files (x86)\Steam\steamapps\common\007 First Light")
    parser.add_argument("--manifest", default="mod_manifest/runtime_wem_manifest.csv")
    parser.add_argument("--label", default="007_it_dub_v0_1")
    parser.add_argument("--backup-root", default="backups")
    parser.add_argument("--apply", action="store_true", help="Actually patch the game. Without it, performs a dry run.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path
    rows = read_csv(manifest_path)
    if not rows:
        raise SystemExit("No rows in manifest")

    ensure_game_not_running()
    runtime = Path(args.game_path) / "Runtime"
    chunk_paths = {"chunk0": runtime / "chunk0.rpkg", "chunk1": runtime / "chunk1.rpkg"}
    for chunk_path in chunk_paths.values():
        if not chunk_path.exists():
            raise SystemExit(f"Missing runtime chunk: {chunk_path}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = root / args.backup_root / f"{stamp}_{args.label}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    planned: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []
    grouped: dict[str, list[dict[str, str]]] = {"chunk0": [], "chunk1": []}
    for row in rows:
        grouped.setdefault(row.get("chunk") or "chunk1", []).append(row)

    for chunk, chunk_rows in grouped.items():
        if not chunk_rows:
            continue
        chunk_path = chunk_paths.get(chunk)
        if chunk_path is None:
            errors.append({"chunk": chunk, "reason": "unknown_chunk"})
            continue
        entries = parse_rpkg_entries(chunk_path)
        (backup_dir / chunk / "original_segments").mkdir(parents=True, exist_ok=True)
        (backup_dir / chunk / "new_segments").mkdir(parents=True, exist_ok=True)

        for row in chunk_rows:
            hash_text = (row.get("source_hash") or "").upper()
            entry = entries.get(hash_text)
            if entry is None:
                errors.append({"hash": hash_text, "chunk": chunk, "reason": "hash_not_found"})
                continue
            if entry.typ != "WWES" or entry.lz4ed or not entry.xored or entry.reference_table_size:
                errors.append({"hash": hash_text, "chunk": chunk, "reason": f"unexpected_layout:{entry.typ}"})
                continue

            source_wem = root / row["wem_path"]
            if not source_wem.exists():
                errors.append({"hash": hash_text, "chunk": chunk, "reason": f"missing_wem:{source_wem}"})
                continue
            new_data = source_wem.read_bytes()
            if len(new_data) > entry.size_final:
                errors.append({"hash": hash_text, "chunk": chunk, "reason": f"oversize:{len(new_data)}>{entry.size_final}"})
                continue

            with chunk_path.open("rb") as f:
                f.seek(entry.data_offset)
                original_stored = f.read(entry.size_final)

            original_rel = Path(chunk) / "original_segments" / f"{entry.index}_{hash_text}.WWES.stored"
            new_rel = Path(chunk) / "new_segments" / f"{entry.index}_{hash_text}.WWES.new"
            (backup_dir / original_rel).write_bytes(original_stored)
            (backup_dir / new_rel).write_bytes(new_data)
            planned.append(
                {
                    "hash": hash_text,
                    "asset_id": row.get("asset_id", ""),
                    "chunk": chunk,
                    "chunk_path": str(chunk_path),
                    "data_offset": entry.data_offset,
                    "data_size_raw": entry.data_size_raw,
                    "data_offset_field_offset": entry.data_offset_field_offset,
                    "data_size_raw_field_offset": entry.data_size_raw_field_offset,
                    "size_final_offset": entry.size_final_offset,
                    "original_size_final": entry.size_final,
                    "new_size_final": len(new_data),
                    "pad_bytes": entry.size_final - len(new_data),
                    "original_relative_path": str(original_rel).replace("\\", "/"),
                    "new_relative_path": str(new_rel).replace("\\", "/"),
                    "original_sha1": sha1_bytes(apply_xor(original_stored)),
                    "new_sha1": sha1_bytes(new_data),
                    "target_it": row.get("target_it", ""),
                }
            )

    if errors:
        (backup_dir / "errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
        raise SystemExit(f"Patch refused: {len(errors)} errors. See {backup_dir / 'errors.json'}")

    if args.apply:
        by_chunk: dict[str, list[dict[str, object]]] = {}
        for row in planned:
            by_chunk.setdefault(str(row["chunk"]), []).append(row)
        for chunk_rows in by_chunk.values():
            chunk_path = Path(str(chunk_rows[0]["chunk_path"]))
            with chunk_path.open("r+b") as f:
                for row in chunk_rows:
                    new_data = (backup_dir / str(row["new_relative_path"])).read_bytes()
                    old_size = int(row["original_size_final"])
                    f.seek(int(row["data_offset"]))
                    f.write(apply_xor(new_data + (b"\x00" * (old_size - len(new_data)))))
                    f.seek(int(row["size_final_offset"]))
                    f.write(struct.pack("<I", old_size))
            entries = parse_rpkg_entries(chunk_path)
            for row in chunk_rows:
                entry = entries[str(row["hash"])]
                new_data = (backup_dir / str(row["new_relative_path"])).read_bytes()
                expected = new_data + (b"\x00" * (int(row["original_size_final"]) - len(new_data)))
                if read_runtime_resource(chunk_path, entry) != expected:
                    raise SystemExit(f"Verification failed for {row['hash']}")

    manifest = {
        "mode": "apply" if args.apply else "dry_run",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "game_path": str(Path(args.game_path)),
        "input_manifest": str(manifest_path),
        "backup_dir": str(backup_dir),
        "file_count": len(planned),
        "files": planned,
    }
    (backup_dir / "patch_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": manifest["mode"], "file_count": len(planned), "backup_dir": str(backup_dir)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
