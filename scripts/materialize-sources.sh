#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
registry="$root_dir/research/source-registry.json"
cache="$root_dir/cache/repositories"

mkdir -p "$cache"
python3 - "$registry" "$cache" "$root_dir/research/source-lock.json" <<'PY'
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

registry, cache, lock_path = map(Path, sys.argv[1:])
data = json.loads(registry.read_text(encoding="utf-8"))
entries = []
for source in data["repositories"]:
    destination = cache / source["name"]
    if destination.exists():
        subprocess.run(["git", "-C", str(destination), "fetch", "--tags", "--prune", "origin"], check=True)
        subprocess.run(["git", "-C", str(destination), "checkout", "main"], check=True)
        subprocess.run(["git", "-C", str(destination), "pull", "--ff-only", "origin", "main"], check=True)
    else:
        subprocess.run(["git", "clone", "--depth", "1", source["url"], str(destination)], check=True)
    revision = subprocess.check_output(["git", "-C", str(destination), "rev-parse", "HEAD"], text=True).strip()
    entries.append({"name": source["name"], "url": source["url"], "revision": revision, "cache_path": str(destination.relative_to(cache.parent.parent))})
lock_path.write_text(json.dumps({"generated_at": datetime.now(UTC).isoformat(), "repositories": entries}, indent=2) + "\n", encoding="utf-8")
print(f"Materialized {len(entries)} public repositories into {cache}")
PY
