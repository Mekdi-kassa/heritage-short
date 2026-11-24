"""
Centralized structured logger for multi-model pipeline calls.
Appends one valid JSON line per model call to runs.jsonl.
Tracks: timestamp, stage, shot_id, model, parameters, seed, latency, cost_usd, cached, status.
"""

import datetime
import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, Optional

_LOG_LOCK = threading.Lock()


class PipelineLogger:
    def __init__(self, log_path: Optional[Path] = None):
        if log_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            log_path = base_dir / "runs.jsonl"
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        stage: str,
        model: str,
        parameters: Dict[str, Any],
        seed: Optional[int],
        latency_seconds: float,
        cost_usd: float = 0.0,
        shot_id: Optional[str] = None,
        cached: bool = False,
        status: str = "success",
        notes: str = ""
    ) -> Dict[str, Any]:
        """Record a single model execution entry into runs.jsonl."""
        entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "stage": stage,
            "shot_id": shot_id,
            "model": model,
            "parameters": parameters,
            "seed": seed,
            "latency_seconds": round(latency_seconds, 4),
            "cost_usd": round(cost_usd, 6),
            "cached": cached,
            "status": status,
            "notes": notes
        }

        with _LOG_LOCK:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        cache_str = " (CACHED)" if cached else ""
        print(f"[{stage.upper()}] [{model}] Shot: {shot_id or 'all'} | {latency_seconds:.2f}s | ${cost_usd:.4f}{cache_str} -> {status}")
        return entry


# Global singleton instance
logger = PipelineLogger()
