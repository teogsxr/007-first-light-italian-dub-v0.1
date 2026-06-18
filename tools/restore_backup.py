#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Restore a backup created by apply_wem_manifest.py.")
    parser.add_argument("--backup", required=True)
    args = parser.parse_args()

    backup = Path(args.backup)
    manifest_path = backup / "patch_manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing patch_manifest.json in {backup}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    by_chunk: dict[str, list[dict[str, object]]] = {}
    for row in manifest.get("files", []):
        by_chunk.setdefault(str(row["chunk_path"]), []).append(row)

    restored = 0
    for chunk_path_text, rows in by_chunk.items():
        chunk_path = Path(chunk_path_text)
        if not chunk_path.exists():
            raise SystemExit(f"Missing chunk: {chunk_path}")
        with chunk_path.open("r+b") as f:
            for row in rows:
                original = (backup / str(row["original_relative_path"])).read_bytes()
                f.seek(int(row["data_offset"]))
                f.write(original)
                f.seek(int(row["data_offset_field_offset"]))
                f.write(struct.pack("<Q", int(row["data_offset"])))
                f.seek(int(row["data_size_raw_field_offset"]))
                f.write(struct.pack("<I", int(row["data_size_raw"])))
                f.seek(int(row["size_final_offset"]))
                f.write(struct.pack("<I", int(row["original_size_final"])))
                restored += 1

    print(f"Restored {restored} resources from {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
