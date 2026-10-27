# Self-Adaptive AI-Driven Combat Survivability Suit

**Team Lead:** Meha S  
**Members:** Raja Vinayagam S, Rithika R

A prototype of a multi-layer, self-adaptive suit whose outer layer changes colour and pattern to match the surrounding environment.

## Problem Statement
- Fixed camouflage cannot adapt to forests, grasslands, soil, roads and buildings.
- A mismatch between camouflage and environment increases the risk of detection.
- Conventional fabric cannot change colour or pattern dynamically.
- Manually changing camouflage is slow and impractical in combat situations.

## Proposed Solution
- Multi-layer suit: armour layer + comfort layer + adaptive outer layer.
- **ESP32-CAM** captures the surroundings.
- **WS2812B 8x8 LED matrix** acts as the adaptive outer layer.
- Colour and pattern change dynamically to match the environment.

## Workflow
1. **Sense** – camera and environmental sensors capture the surroundings.
2. **Process** – ESP32 / detector analyses the image and decides the pattern.
3. **Control** – pixel-driver circuits control the WS2812B pixels.
4. **Adapt** – the matrix changes colour/pattern to match the terrain.
5. **Power & Communication** – battery management and wireless monitoring.

## Hardware (Prototype)
ESP32-CAM, WS2812B 8x8 matrix, FTDI USB-to-TTL, jumper wires, power source, laptop.

## Software in this Repository
| File | Purpose |
|------|---------|
| `run.py` | Flask server and API (collector, sensors, detection, data) |
| `detector.py` | Terrain detection + 8x8 camouflage pattern generator |
| `index.html`, `style.css`, `app.js` | Web dashboard |
| `sample_sensor_data.csv` | Sample environmental sensor records |
| `architecture.md` | System architecture |
| `test_cases.md` | Test cases |

## Run Locally
```bash
pip install -r requirements.txt
python run.py
```
Open http://127.0.0.1:5000

## Features
- Start / Stop the sensor collector
- Upload an image -> detected terrain, confidence, and an 8x8 camouflage preview
- Live sensor values (temperature, humidity, PM2.5, gas, light)
- Reads sample CSV data

## Impact
Enhanced concealment, dynamic camouflage, reduced detection risk, multi-terrain adaptability, real-time adaptation, and use in defence and rescue operations.

## License
MIT
