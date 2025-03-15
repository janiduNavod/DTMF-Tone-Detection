# DTMF Number Detector Using Python
## Project Overview

This project processes audio files containing DTMF (Dual-Tone Multi-Frequency) tones, detects the corresponding phone number digits, and visualizes the results using time and frequency domain plots. It uses Fast Fourier Transform (FFT) to identify the DTMF tones and map them to their respective numbers.

## Features
Reads and processes multiple audio files.

Detects DTMF tones and extracts numbers from them.

Plays the detected tones.

Displays the detected phone numbers.

Plots time-domain and frequency-domain representations of the audio signals.

## Technologies Used

Python

numpy for numerical computations

matplotlib for visualization

scipy.signal for peak detection

sounddevice for audio playback

soundfile for reading audio files

## Usage

Place the .wav audio files in the project directory.
Run the script:
python dtmf_detection.py
The script will:
Play the audio files.
Detect and print the DTMF digits (phone numbers).
Display time-domain and frequency-domain plots.

## File Structure
.
├── dtmf_detection.py   # Main script for detecting DTMF numbers
├── tone01.wav          # Example audio file
├── tone02.wav          # Example audio file
├── tone03.wav          # Example audio file
├── README.md           # Project documentation
