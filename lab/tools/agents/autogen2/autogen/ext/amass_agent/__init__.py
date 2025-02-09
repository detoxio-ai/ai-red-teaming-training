
try:
    from ._amass_agent import AmassToolAgent
except ImportError as e:
    raise ImportError(
        "Dependencies for AmassAgent not found. "
        'Please install autoattack-ext with the "amass_agent" extra: '
        'pip install "autoattack-ext[magentic-one]"'
    ) from e

__all__ = ["AmassToolAgent"]