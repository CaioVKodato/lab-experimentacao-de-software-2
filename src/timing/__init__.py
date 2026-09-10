"""Coleta de tempo (RQ1) e taxa de sucesso (RQ2) dos trials."""

from src.timing.clock import resolve_time
from src.timing.protocol import finish, record, start
from src.timing.schema import Trial, build_trial

__all__ = ["Trial", "build_trial", "finish", "record", "resolve_time", "start"]
