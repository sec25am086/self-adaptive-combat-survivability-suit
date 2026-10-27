"""Terrain detector and 8x8 camouflage pattern generator.

Takes an image (as captured by the ESP32-CAM), finds the dominant terrain by
comparing its average colour with reference terrain colours, and produces an
8x8 RGB grid that can be sent to a WS2812B matrix.
"""
import io

import numpy as np
from PIL import Image

# Reference colours (RGB) for each terrain
TERRAINS = {
    "Forest":    (34, 70, 34),
    "Grassland": (110, 150, 60),
    "Soil":      (120, 90, 60),
    "Road":      (80, 80, 85),
    "Building":  (160, 155, 150),
}


def _load(image_bytes):
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")


def make_pattern(img, size=8):
    """Downsample the image to size x size pixels = camouflage pattern."""
    small = img.resize((size, size), Image.Resampling.BILINEAR)
    arr = np.asarray(small, dtype=int)
    return arr.tolist()


def detect(image_bytes):
    """Return dict: terrain, confidence (0-1), average_rgb, pattern (8x8 RGB)."""
    img = _load(image_bytes)
    arr = np.asarray(img.resize((64, 64)), dtype=float)
    avg = arr.reshape(-1, 3).mean(axis=0)

    names = list(TERRAINS)
    dists = np.array([np.linalg.norm(avg - np.array(TERRAINS[n])) for n in names])
    # Softmax over negative distance -> confidence
    scores = np.exp(-dists / 30.0)
    probs = scores / scores.sum()
    best = int(np.argmax(probs))

    return {
        "terrain": names[best],
        "confidence": round(float(probs[best]), 3),
        "average_rgb": [int(v) for v in avg],
        "pattern": make_pattern(img),
    }


if __name__ == "__main__":
    import sys
    with open(sys.argv[1], "rb") as f:
        result = detect(f.read())
    print(result["terrain"], result["confidence"], result["average_rgb"])
