"""
AI Pipeline Failure Triage - Main triage logic using Ollama LLM.
Refactored: uses config module, structured logging, typed return values, shared client.
"""
import logging
import time
from typing import Dict, Optional

from openai import OpenAI
import config

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("triage")

_client = OpenAI(
    base_url=config.BASE_URL,
    api_key=config.API_KEY,
    timeout=config.TIMEOUT_SECONDS,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _parse_response(response_text: str) -> Optional[Dict[str, str]]:
    """Extract the 6 required fields from the LLM response."""
    result: Dict[str, str] = {}
    lines = response_text.strip().splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        for field in config.REQUIRED_FIELDS:
            if line.startswith(field + ":"):
                result[field] = line[len(field) + 1:].strip()
                break
    return result if all(f in result and result[f].strip() for f in config.REQUIRED_FIELDS) else None


def _check_termination(analysis: Dict[str, str]) -> bool:
    """Return True if the analysis contains a critical condition."""
    text = " ".join(analysis.values()).upper()
    return any(kw.upper() in text for kw in config.TERMINATION_CONDITIONS)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def triage_pipeline_failure(build_log: str, pipeline_name: str = "unknown") -> Dict:
    """
    Triage a CodeBuild/pipeline failure using the LLM.

    Args:
        build_log:     Raw CodeBuild failure log text.
        pipeline_name: Descriptive name for logging.

    Returns:
        Dict with triage fields plus 'requires_human_intervention' bool
        and 'processing_time_seconds'.
    """
    logger.info("Starting triage for pipeline: %s", pipeline_name)
    start = time.time()

    from prompts import build_messages
    messages = build_messages(build_log)

    seen_responses: list = []

    for attempt in range(1, config.MAX_RETRIES + 1):
        elapsed = time.time() - start
        if elapsed > config.TIMEOUT_SECONDS:
            logger.error("Timeout after %.1fs", elapsed)
            return {"error": f"Timeout after {elapsed:.1f}s", "requires_human_intervention": True}

        try:
            response = _client.chat.completions.create(
                model=config.MODEL,
                messages=messages,
                temperature=0.1,
                max_tokens=400,
            )
            response_text = response.choices[0].message.content
            logger.debug("LLM response (attempt %d): %s", attempt, response_text[:120])
        except Exception as exc:
            logger.error("LLM call failed on attempt %d: %s", attempt, exc)
            time.sleep(2 ** attempt)
            continue

        # Loop detection
        if response_text in seen_responses:
            logger.warning("Loop detected on attempt %d, breaking.", attempt)
            break
        seen_responses.append(response_text)
        if len(seen_responses) >= config.LOOP_DETECTION_LIMIT:
            seen_responses.clear()

        analysis = _parse_response(response_text)
        if not analysis:
            logger.warning("Parse failed on attempt %d. Missing required fields.", attempt)
            time.sleep(1)
            continue

        needs_human = _check_termination(analysis)
        analysis["requires_human_intervention"] = needs_human
        analysis["processing_time_seconds"] = round(time.time() - start, 2)
        if needs_human:
            logger.warning("Critical condition detected - human intervention required!")
        logger.info("Triage complete in %.2fs", analysis["processing_time_seconds"])
        return analysis

    logger.error("All %d attempts exhausted.", config.MAX_RETRIES)
    return {"error": f"Failed after {config.MAX_RETRIES} retries", "requires_human_intervention": True}
