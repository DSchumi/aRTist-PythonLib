from PIL import Image
import numpy as np
from pathlib import Path
import json
import time


def load_projection(
    projection_path: Path, load_projection_geometry: bool = True
) -> tuple[np.ndarray, dict]:
    try:
        projection_array = np.array(Image.open(projection_path))
    except FileNotFoundError:
        time.sleep(1)
        projection_array = np.array(Image.open(projection_path))

    if not load_projection_geometry:
        return projection_array, None
    else:
        return projection_array, load_header(projection_path)


def load_header(projection_path) -> dict:
    with open(str(projection_path.parent / f"{projection_path.stem}.json"), "r") as f:
        projection_geometry = json.load(f)

    return projection_geometry
