import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#////////////////// Define DTMF frequencies///////////
dtmf_freqs = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '0': (941, 1336), '*': (941, 1209), '#': (941, 1477)
}

# Load the audio files
filenames = ['tone01.wav', 'tone02.wav', 'tone03.wav']
data_list = []
fs_list = []

for filename in filenames:
    data, fs = sf.read(filename, dtype='float32')
    data_list.append(data)
    fs_list.append(fs)

# Play the audio files
for data, fs in zip(data_list, fs_list):
    sd.play(data, fs)
    sd.wait()

def detect_dtmf_tone(segment, fs):
    n = len(segment)
    frequencies = np.fft.fftfreq(n, d=1/fs)
    fft_values = np.fft.fft(segment)
    magnitude_spectrum = np.abs(fft_values)[:n // 2]
    peaks, _ = find_peaks(magnitude_spectrum, height=np.max(magnitude_spectrum)/10)
    peak_freqs = frequencies[peaks]
    
    for digit, (low_freq, high_freq) in dtmf_freqs.items():
        if (any(abs(peak_freqs - low_freq) < 20) and 
            any(abs(peak_freqs - high_freq) < 20)):
            return digit
    return None

# Analyze the audio 
all_detected_digits = []

for data, fs in zip(data_list, fs_list):
    detected_digits = []
    window_size = int(0.05 * fs)
    overlap = int(0.025 * fs)
    start = 0
    while start < len(data):
        segment = data[start:start + window_size]
        digit = detect_dtmf_tone(segment, fs)
        if digit and (not detected_digits or digit != detected_digits[-1]):
            detected_digits.append(digit)
            if len(detected_digits) == 10:
                break
        start += window_size - overlap
    all_detected_digits.append(detected_digits)

# Display the detected digits 
for i, digits in enumerate(all_detected_digits):
    print(f"Detected DTMF digits for tone0{i+1}.wav:", ''.join(digits))

# Plot the time domain waveform and frequency domain
fig, axs = plt.subplots(len(data_list), 2, figsize=(12, 6))

for i, (data, fs) in enumerate(zip(data_list, fs_list)):
    # Time domain plot
    axs[i, 0].plot(np.arange(len(data)) / fs, data)
    axs[i, 0].set_title(f'Time Domain Waveform (tone0{i+1}.wav)')
    axs[i, 0].set_xlabel('Time (seconds)')
    axs[i, 0].set_ylabel('Amplitude')

    # Frequency domain plot
    frequencies = np.fft.fftfreq(len(data), d=1/fs)
    fft_values = np.fft.fft(data)
    magnitude_spectrum = np.abs(fft_values)[:len(data) // 2]
    axs[i, 1].plot(frequencies[:len(data) // 2], magnitude_spectrum)
    axs[i, 1].set_title(f'Frequency Domain (tone0{i+1}.wav)')
    axs[i, 1].set_xlabel('Frequency (Hz)')
    axs[i, 1].set_ylabel('Magnitude')

plt.tight_layout()
plt.show()
