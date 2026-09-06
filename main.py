"""
AI Signal Optimization System for Smart Tactical Helmet - CLI Orchestrator
---------------------------------------------------------------------------
Main entrypoint for model training, real-time ESP32 telemetry monitoring,
simulation mode, and Streamlit dashboard launcher.
"""

import os
import sys
import time
import argparse
import subprocess

# Ensure root directory is in sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.train_model import train_all_models
from src.signal_optimizer import SignalOptimizer
from src.esp32_serial import ESP32SerialInterface, list_available_serial_ports

def run_terminal_monitor(port=None, simulation=True, interval=1.5):
    """
    Runs terminal real-time signal monitoring & optimization output.
    """
    print("\n=======================================================")
    print("      AI SIGNAL OPTIMIZATION MONITOR (CLI MODE)        ")
    print("=======================================================")
    print(f"Mode: {'SIMULATION' if simulation else f'ESP32 HARDWARE ({port})'}")
    print("Press Ctrl+C to terminate monitoring.\n")

    optimizer = SignalOptimizer()
    esp = ESP32SerialInterface(port=port, simulation_mode=simulation)

    try:
        sample_count = 0
        while True:
            sample_count += 1
            telemetry = esp.read_telemetry()
            opt_result = optimizer.evaluate_optimization(telemetry)

            print(f"--- [SAMPLE #{sample_count:03d}] {time.strftime('%H:%M:%S')} ---")
            print(f"RSSI        : {telemetry['RSSI']} dBm")
            print(f"SNR         : {telemetry['SNR']} dB")
            print(f"Packet Loss : {telemetry['PacketLoss']} %")
            print(f"Latency     : {telemetry['Latency']} ms")
            print(f"Throughput  : {telemetry['Throughput']} Mbps")
            print("------------------------------------")
            print(f"AI SIGNAL STATUS  : {opt_result['current_status']}")
            print(f"AI CONFIDENCE     : {opt_result['confidence']} %")
            print(f"RECOMMENDED ACTION: {opt_result['recommended_action']}")
            print(f"TARGET CONFIG     : {opt_result['target_config']}")
            print(f"REASONING         : {opt_result['recommendation_reason']}")
            print("------------------------------------\n")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[MONITOR] Stopped by user.")
        esp.disconnect()

def launch_streamlit_dashboard():
    """Launches Streamlit dashboard web interface."""
    app_path = os.path.join("dashboard", "app.py")
    print(f"[DASHBOARD] Launching Streamlit web dashboard from '{app_path}'...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])

def main():
    parser = argparse.ArgumentParser(description="AI-Based Signal Optimization System for Smart Tactical Helmet")
    parser.add_argument("--train", action="store_true", help="Train and compare all ML models and save best model")
    parser.add_argument("--simulate", action="store_true", help="Run terminal-based real-time simulation monitor")
    parser.add_argument("--esp32", type=str, help="Run terminal monitor connected to specific ESP32 serial port (e.g. COM3 or /dev/ttyUSB0)")
    parser.add_argument("--ports", action="store_true", help="List available connected USB serial COM ports")
    parser.add_argument("--dashboard", action="store_true", help="Launch Streamlit web dashboard UI")

    args = parser.parse_args()

    if args.ports:
        ports = list_available_serial_ports()
        print("Connected Serial Ports:", ports if ports else "No physical COM ports detected.")
        return

    if args.train:
        train_all_models()
        return

    if args.simulate:
        run_terminal_monitor(simulation=True)
        return

    if args.esp32:
        run_terminal_monitor(port=args.esp32, simulation=False)
        return

    if args.dashboard:
        launch_streamlit_dashboard()
        return

    # Default fallback if no flags provided: Launch dashboard
    launch_streamlit_dashboard()

if __name__ == "__main__":
    main()
