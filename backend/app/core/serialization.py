import math
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import UUID

import numpy as np
import pandas as pd


class JsonSerializer:
    @classmethod
    def to_native(cls, obj: Any) -> Any:
        """Recursively converts all objects into native JSON-safe python types."""
        if isinstance(obj, dict):
            return {str(k): cls.to_native(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple, set)):
            return [cls.to_native(i) for i in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            # check for nan / inf
            val = float(obj)
            if math.isnan(val) or math.isinf(val):
                return None
            return val
        elif isinstance(obj, np.ndarray):
            return cls.to_native(obj.tolist())
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif pd.isna(obj):
            return None
        elif isinstance(obj, (Decimal, UUID, Path)):
            return str(obj)
        elif isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return None
            return obj

        return obj
