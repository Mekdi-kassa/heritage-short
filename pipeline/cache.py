"""
Content-Hash Pipeline Caching Engine.
Computes cryptographic SHA-256 hashes of stage inputs (prompts, seeds, durations, model versions).
Ensures idempotent execution: re-running the pipeline only regenerates shots whose inputs changed.
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class PipelineCache:
    def __init__(self, cache_dir: Optional[Path] = None):
        if cache_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
            cache_dir = base_dir / ".cache"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_file = self.cache_dir / "manifest.json"
        self._manifest = self._load_manifest()

    def _load_manifest(self) -> Dict[str, Any]:
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_manifest(self) -> None:
        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(self._manifest, f, indent=2, ensure_ascii=False)

    @staticmethod
    def compute_hash(stage: str, item_id: str, inputs: Dict[str, Any], model: str) -> str:
        """Create deterministic SHA-256 digest of execution inputs."""
        payload = {
            "stage": stage,
            "item_id": item_id,
            "model": model,
            "inputs": inputs
        }
        serialized = json.dumps(payload, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def get_cache_key(self, stage: str, item_id: str) -> str:
        return f"{stage}::{item_id}"

    def is_cached(
        self,
        stage: str,
        item_id: str,
        inputs: Dict[str, Any],
        model: str,
        expected_output: Path
    ) -> bool:
        """Check if output exists and input hash matches manifest."""
        if not expected_output.exists() or expected_output.stat().st_size == 0:
            return False

        key = self.get_cache_key(stage, item_id)
        current_hash = self.compute_hash(stage, item_id, inputs, model)
        cached_entry = self._manifest.get(key)

        if cached_entry and cached_entry.get("hash") == current_hash:
            return True
        return False

    def record_success(
        self,
        stage: str,
        item_id: str,
        inputs: Dict[str, Any],
        model: str,
        output_path: Path
    ) -> None:
        """Record successful generation into manifest."""
        key = self.get_cache_key(stage, item_id)
        h = self.compute_hash(stage, item_id, inputs, model)
        self._manifest[key] = {
            "hash": h,
            "model": model,
            "output_path": str(output_path.resolve()),
            "timestamp": output_path.stat().st_mtime if output_path.exists() else 0
        }
        self._save_manifest()

    def clear(self, stage: Optional[str] = None) -> None:
        """Clear cache entries for a stage, or completely."""
        if stage:
            keys_to_del = [k for k in self._manifest if k.startswith(f"{stage}::")]
            for k in keys_to_del:
                del self._manifest[k]
        else:
            self._manifest.clear()
        self._save_manifest()


# Global singleton instance
cache = PipelineCache()
