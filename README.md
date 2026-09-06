# AI-Based Signal Optimization System for Smart Tactical Helmet 🪖📡

A working prototype of a Machine-Learning powered **Signal Optimization & Decision Support System** designed for smart tactical helmets in field operations. 

The system continuously monitors wireless radio frequency (RF) communication telemetry (**RSSI, SNR, Packet Loss, Latency, Throughput**), predicts signal link quality (**GOOD, MEDIUM, POOR**), and recommends optimal predefined RF/antenna configuration profiles (Configuration A, B, or C) to maintain squad communication integrity.

---

## 📋 Table of Contents
1. [Project Objective](#1-project-objective)
2. [System Architecture](#2-system-architecture)
3. [How the AI Model Works](#3-how-the-ai-model-works)
4. [Dataset Format & Synthetic Data Notice](#4-dataset-format--synthetic-data-notice)
5. [Model Training & Comparison](#5-model-training--comparison)
6. [ESP32 Hardware Integration & Serial Protocol](#6-esp32-hardware-integration--serial-protocol)
7. [Installation & Execution Guide](#7-installation--execution-guide)
8. [Signal Optimization & Decision Logic](#8-signal-optimization--decision-logic)
9. [Important Technical Limitations](#9-important-technical-limitations)
10. [Future Enhancements](#10-future-enhancements)

---

## 1. Project Objective

In high-risk tactical operations (urban combat, subterranean search, search and rescue), soldiers wearing tactical helmets face severe RF degradation caused by concrete structures, metallic shielding, terrain obstacles, and mobility fluctuations.

**System Goal**:
- Monitor 5 vital RF parameters in real time.
- Classify link status into `GOOD`, `MEDIUM`, or `POOR`.
- Recommend the best available RF configuration (profile switching) before a complete link outage occurs.

---

## 2. System Architecture

```
ai_signal_optimization/
│
├── data/
│   └── signal_data.csv        # Baseline dataset (labeled RF samples)
│
├── models/
│   └── signal_model.pkl       # Trained ML model pipeline & scaler
│
├── src/
│   ├── __init__.py
│   ├── generate_dataset.py    # Synthetic dataset generator
│   ├── data_preprocessing.py  # Data cleaning, outlier removal, train/test split
│   ├── train_model.py         # Multi-model training engine & selection
│   ├── evaluate_model.py      # Metrics computation & evaluation matrix
│   ├── signal_optimizer.py    # RF profile recommendation decision logic
│   └── esp32_serial.py        # ESP32 USB serial reader & simulator fallback
│
├── dashboard/
│   └── app.py                 # Interactive Streamlit UI Dashboard
│
├── requirements.txt           # Python dependencies list
├── README.md                  # Comprehensive project documentation
└── main.py                    # Unified CLI command line runner
```

---

## 3. How the AI Model Works

The application uses multi-class classification algorithms to map real-time telemetry inputs to signal quality categories:

Inputs (5 Features):
1. **RSSI** (Received Signal Strength Indicator in dBm, range: -105 to -40)
2. **SNR** (Signal-to-Noise Ratio in dB, range: 0 to 35)
3. **Packet Loss** (Percentage of dropped packets %, range: 0 to 50)
4. **Latency** (Network round-trip delay in ms, range: 10 to 400)
5. **Throughput** (Data rate in Mbps, range: 0.1 to 15.0)

Output (3 Classes):
- `GOOD` (Optimal link stability, low latency, high throughput)
- `MEDIUM` (Moderate signal strength, slight packet loss, acceptable link)
- `POOR` (Severe interference, high loss/latency, imminent disconnection)

---

## 4. Dataset Format & Synthetic Data Notice

### ⚠️ Data Notice
The baseline file `data/signal_data.csv` contains **synthetic sample data** modeled for prototyping and SIH demonstration. It reflects modeled tactical environments:
- Open area / Clear Line-of-Sight (LOS)
- Indoor room & narrow corridors
- Behind reinforced concrete walls
- Distance variations & movement/orientation shifts

### CSV Schema (`data/signal_data.csv`)
```csv
RSSI,SNR,PacketLoss,Latency,Throughput,Quality
-55.2,24.1,0.5,19.2,12.4,GOOD
-72.4,13.8,4.2,54.1,5.6,MEDIUM
-94.1,3.5,21.8,168.4,1.1,POOR
```

---

## 5. Model Training & Comparison

The system evaluates four distinct machine learning classifiers:
1. **Random Forest** (Primary Ensemble Model)
2. **Decision Tree**
3. **Support Vector Machine (SVM)**
4. **Logistic Regression**

The pipeline automatically splits data (80% train / 20% test), calculates **Accuracy, Precision, Recall, and F1-Score**, builds a **Confusion Matrix**, selects the best performing model, and saves the pipeline to `models/signal_model.pkl`.

To train the models manually:
```bash
python main.py --train
```

---

## 6. ESP32 Hardware Integration & Serial Protocol

### ESP32 Setup
The system interfaces directly with an ESP32 microcontroller connected via USB Serial (baud rate: **115200**).

### Serial Line Output Format
The ESP32 must print comma-separated values to the Serial stream matching:
```text
RSSI,SNR,PacketLoss,Latency,Throughput
```

**Example Serial Output**:
```text
-68,15,3,32,7.4
```

### ESP32 C++ Code Snippet (Arduino Framework)
```cpp
void setup() {
  Serial.begin(115200);
}

void loop() {
  // Read physical RF transceivers / sensors
  float rssi = -68.0;
  float snr = 15.0;
  float packetLoss = 3.0;
  float latency = 32.0;
  float throughput = 7.4;

  Serial.print(rssi); Serial.print(",");
  Serial.print(snr); Serial.print(",");
  Serial.print(packetLoss); Serial.print(",");
  Serial.print(latency); Serial.print(",");
  Serial.println(throughput);

  delay(1000);
}
```

### Simulation Mode Fallback
If no ESP32 hardware is connected, the application automatically defaults to **Simulation Mode**, generating dynamic realistic tactical operator signal variations.

---

## 7. Installation & Execution Guide

### Prerequisites
- Python 3.9+

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Streamlit Web Dashboard
```bash
streamlit run dashboard/app.py
```
*Alternatively:*
```bash
python main.py --dashboard
```

### 3. Run CLI Terminal Monitor (Simulation Mode)
```bash
python main.py --simulate
```

### 4. Run CLI Monitor with ESP32 Connected (e.g., COM3)
```bash
python main.py --esp32 COM3
```

---

## 8. Signal Optimization & Decision Logic

The `SignalOptimizer` evaluates candidate RF profiles (**Configuration A, B, and C**):
- **Configuration A**: Sub-GHz Narrowband profile (Superior range & obstacle penetration, lower throughput).
- **Configuration B**: 2.4 GHz High-Capacity profile (Optimal for line-of-sight & high bandwidth).
- **Configuration C**: 5 GHz Mesh profile (Balanced obstacle tolerance & moderate bandwidth).

### Decision Rules
```text
IF AI Predicts GOOD:
    Action: CONTINUE CURRENT CONFIGURATION
    Reason: Current link quality is optimal.

IF AI Predicts MEDIUM:
    Evaluate alternate candidate configurations.
    IF candidate score > current score:
        Action: TRY ALTERNATE CONFIGURATION (Config X)
    ELSE:
        Action: CONTINUE CURRENT CONFIGURATION

IF AI Predicts POOR:
    Evaluate all candidates (A, B, C).
    Action: RECOMMEND SWITCHING TO CONFIGURATION (Best Candidate)
    Reason: Critical degradation detected. Switch recommended for link survival.
```

---

## 9. Important Technical Limitations

> [!WARNING]
> 1. **No Physical Antenna Redesign**: The AI model **does NOT physically alter antenna dimensions or geometry**. It recommends optimal selections among predefined software/hardware RF configurations.
> 2. **Unrestricted RF Control**: The system does not directly modify licensed military frequency allocations without hardware API abstraction drivers.
> 3. **Synthetic Baseline**: Demo dataset uses synthetic modeled values for initial algorithm evaluation prior to hardware integration.

---

## 10. Future Enhancements

- Integrate Deep Q-Learning (Reinforcement Learning) for adaptive channel hopping.
- Add LoRa / Mesh Network multi-hop relay selection.
- Implement GPS/Location-aware spatial RF heatmaps for squad leaders.
