import os
import sys
import wave
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

try:
    import mido
except ImportError:
    mido = None

# Krumhansl-Schmuckler key profiles for key-finding
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
PITCH_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# General MIDI Instrument Groups
GM_INSTRUMENTS = {
    range(0, 8): "Acoustic Piano / Keyboard",
    range(8, 16): "Chromatic Percussion (Xylophone, Celesta, Glockenspiel)",
    range(16, 24): "Organ",
    range(24, 32): "Acoustic / Electric Guitar",
    range(32, 40): "Bass (Acoustic / Upright / Electric)",
    range(40, 48): "Solo & Ensemble Strings (Violin, Cello, Pizzicato)",
    range(48, 56): "Orchestral String Ensembles & Harp",
    range(56, 64): "Brass Section (Trumpet, French Horn, Trombone, Tuba)",
    range(64, 72): "Reed / Woodwinds (Oboe, Clarinet, Bassoon)",
    range(72, 80): "Pipe Woodwinds (Flute, Piccolo)",
    range(80, 88): "Synth Leads",
    range(88, 96): "Synth Pads & Shimmers",
    range(112, 120): "Orchestral Percussion (Timpani, Tubular Bells)",
}


def parse_midi(midi_path):
    if not mido or not os.path.exists(midi_path):
        return None

    mid = mido.MidiFile(midi_path)
    tempos = []
    time_signatures = []
    instruments = set()
    total_notes = 0
    pitch_distribution = np.zeros(12)

    for track in mid.tracks:
        for msg in track:
            if msg.type == "set_tempo":
                tempos.append(round(mido.tempo2bpm(msg.tempo)))
            elif msg.type == "time_signature":
                time_signatures.append(f"{msg.numerator}/{msg.denominator}")
            elif msg.type == "program_change":
                prog = msg.program
                for prange, name in GM_INSTRUMENTS.items():
                    if prog in prange:
                        instruments.add(name)
                        break
            elif msg.type == "note_on" and msg.velocity > 0:
                pitch_distribution[msg.note % 12] += 1
                total_notes += 1

    avg_bpm = round(np.mean(tempos)) if tempos else None
    time_sig = time_signatures[0] if time_signatures else "4/4"
    
    # Estimate key from MIDI pitches
    best_key = None
    if total_notes > 0:
        norm_pitches = pitch_distribution / total_notes
        best_score = -1e9
        for i in range(12):
            rot = np.roll(norm_pitches, -i)
            maj = np.corrcoef(rot, MAJOR_PROFILE)[0, 1]
            if maj > best_score:
                best_score = maj
                best_key = f"{PITCH_NAMES[i]} major"
            mino = np.corrcoef(rot, MINOR_PROFILE)[0, 1]
            if mino > best_score:
                best_score = mino
                best_key = f"{PITCH_NAMES[i]} minor"

    return {
        "bpm": avg_bpm,
        "time_signature": time_sig,
        "detected_instruments": sorted(list(instruments)),
        "total_notes": total_notes,
        "key": best_key,
        "duration_seconds": round(mid.length, 1)
    }


def load_wav(filepath, max_duration=120):
    with wave.open(filepath, "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        
        max_frames = min(n_frames, int(max_duration * framerate))
        raw_bytes = wf.readframes(max_frames)
        
        if sampwidth == 2:
            data = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        elif sampwidth == 4:
            data = np.frombuffer(raw_bytes, dtype=np.int32).astype(np.float32) / 2147483648.0
        elif sampwidth == 1:
            data = (np.frombuffer(raw_bytes, dtype=np.uint8).astype(np.float32) - 128) / 128.0
        else:
            raise ValueError(f"Unsupported sample width: {sampwidth}")
            
        if n_channels > 1:
            data = data.reshape(-1, n_channels).mean(axis=1)
            
        duration = len(data) / framerate
        return data, framerate, duration


def estimate_bpm(audio, sr):
    target_sr = 11025
    if sr > target_sr:
        decimate_factor = sr // target_sr
        audio_sub = signal.decimate(audio, decimate_factor)
        sr_sub = sr // decimate_factor
    else:
        audio_sub = audio
        sr_sub = sr

    hop_length = 256
    n_fft = 1024
    f, t, Zxx = signal.stft(audio_sub, fs=sr_sub, nperseg=n_fft, noverlap=n_fft - hop_length)
    mag = np.abs(Zxx)
    diff = np.diff(mag, axis=1)
    diff = np.maximum(0, diff)
    onset_env = np.mean(diff, axis=0)
    onset_env = onset_env - np.mean(onset_env)
    
    autocorr = np.correlate(onset_env, onset_env, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    
    fps = sr_sub / hop_length
    min_lag = int(fps * 60 / 180)
    max_lag = int(fps * 60 / 50)
    if max_lag > len(autocorr):
        max_lag = len(autocorr) - 1
        
    best_lag = min_lag + np.argmax(autocorr[min_lag:max_lag])
    bpm = (fps * 60) / best_lag
    
    # Normalize double-time / half-time to standard film score range (60 - 140 BPM)
    if bpm > 145:
        bpm = bpm / 2
    return round(bpm)


def estimate_key(audio, sr):
    hop_length = 2048
    n_fft = 4096
    f, t, Zxx = signal.stft(audio, fs=sr, nperseg=n_fft, noverlap=n_fft - hop_length)
    mag = np.abs(Zxx)
    
    chroma = np.zeros(12)
    valid_f = (f >= 65.4) & (f <= 2093.0)
    freqs = f[valid_f]
    mags = mag[valid_f, :].mean(axis=1)
    
    midi_notes = 69 + 12 * np.log2(freqs / 440.0)
    pitch_classes = np.round(midi_notes).astype(int) % 12
    
    for pc, m in zip(pitch_classes, mags):
        chroma[pc] += m
        
    if np.sum(chroma) > 0:
        chroma = chroma / np.sum(chroma)
        
    best_score = -1e9
    best_key = "C major"
    
    for i in range(12):
        rot_chroma = np.roll(chroma, -i)
        maj_corr = np.corrcoef(rot_chroma, MAJOR_PROFILE)[0, 1]
        if maj_corr > best_score:
            best_score = maj_corr
            best_key = f"{PITCH_NAMES[i]} major"
            
        min_corr = np.corrcoef(rot_chroma, MINOR_PROFILE)[0, 1]
        if min_corr > best_score:
            best_score = min_corr
            best_key = f"{PITCH_NAMES[i]} minor"
            
    return best_key


def analyze_timbre_and_dynamics(audio, sr):
    n_fft = 2048
    f, t, Zxx = signal.stft(audio, fs=sr, nperseg=n_fft)
    mag = np.abs(Zxx)
    freq_weights = f[:, np.newaxis]
    sum_mag = np.sum(mag, axis=0) + 1e-10
    spectral_centroid = np.mean(np.sum(freq_weights * mag, axis=0) / sum_mag)
    
    frame_len = int(sr * 0.5)
    rms = [np.sqrt(np.mean(audio[i:i+frame_len]**2)) for i in range(0, len(audio) - frame_len, frame_len)]
    rms = np.array(rms)
    dynamic_range_db = 20 * np.log10(np.max(rms) / (np.min(rms[rms > 0]) + 1e-8)) if len(rms) > 0 else 0
    
    if spectral_centroid < 1300:
        timbre_desc = "Warm, deep, resonant acoustic tone with rich lower harmonics"
    elif spectral_centroid < 2200:
        timbre_desc = "Balanced lyrical acoustic warmth with sparkling, expressive overtones"
    else:
        timbre_desc = "Brilliant, crystalline, brass-forward and soaring high-register presence"
        
    if len(rms) > 4:
        start_energy = np.mean(rms[:len(rms)//4])
        end_energy = np.mean(rms[-len(rms)//4:])
        if end_energy > start_energy * 1.4:
            arc_desc = "Intimate whisper building in a patient crescendo to a sweeping symphonic climax"
        elif start_energy > end_energy * 1.4:
            arc_desc = "Grand emotional opening gradually softening into a tender, contemplative resolution"
        else:
            arc_desc = "Steady, noble, and deeply expressive melodic flow"
    else:
        arc_desc = "Intimate and consistent expressive dynamic"
        
    return spectral_centroid, timbre_desc, dynamic_range_db, arc_desc


def generate_spectrogram_image(audio, sr, output_png):
    plt.figure(figsize=(10, 4), dpi=120)
    f, t, Sxx = signal.spectrogram(audio[:sr*60], fs=sr, nperseg=1024, noverlap=512)
    plt.pcolormesh(t, f[:256], 10 * np.log10(Sxx[:256, :] + 1e-10), cmap='magma', shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Acoustic Spectrogram Analysis (First 60s)')
    plt.colorbar(label='Power/Frequency [dB/Hz]')
    plt.tight_layout()
    plt.savefig(output_png)
    plt.close()


def listen_and_synthesize(wav_path, midi_path=None, output_png=None):
    if not os.path.exists(wav_path):
        raise FileNotFoundError(f"Audio file not found: {wav_path}")
        
    print(f"👂 Listening to Audio: {wav_path}...")
    audio, sr, duration = load_wav(wav_path, max_duration=90)
    
    bpm = estimate_bpm(audio, sr)
    key = estimate_key(audio, sr)
    centroid, timbre_desc, dyn_range, arc_desc = analyze_timbre_and_dynamics(audio, sr)
    
    midi_info = None
    if midi_path and os.path.exists(midi_path):
        print(f"🎹 Parsing MIDI score: {midi_path}...")
        midi_info = parse_midi(midi_path)
        if midi_info and midi_info.get("bpm"):
            bpm = midi_info["bpm"]
        if midi_info and midi_info.get("key"):
            key = midi_info["key"]

    if output_png:
        generate_spectrogram_image(audio, sr, output_png)
        print(f"📊 Spectrogram rendered to: {output_png}")
        
    instruments_str = "expressive solo acoustic grand piano, warm cello countermelodies, and lush symphonic strings"
    if midi_info and midi_info.get("detected_instruments"):
        instruments_str = ", ".join(midi_info["detected_instruments"])
        
    # Synthesize 100% IP-Clean ElevenLabs Prompt
    clean_prompt = (
        f"{bpm} BPM Neoclassical and cinematic orchestral theme in {key}. "
        f"{timbre_desc}. {arc_desc}. "
        f"Completely drum-free and purely acoustic, featuring {instruments_str}."
    )
    
    print("\n" + "="*50)
    print("🎧 ACOUSTIC EAR INTELLIGENCE DOSSIER")
    print("="*50)
    print(f"• Duration Analyzed : {duration:.1f}s")
    print(f"• Estimated Tempo   : {bpm} BPM")
    print(f"• Detected Tonality : {key}")
    print(f"• Timbre Profile    : {timbre_desc} (Centroid: {centroid:.1f} Hz)")
    print(f"• Dynamic Range     : {dyn_range:.1f} dB")
    print(f"• Dynamic Arc       : {arc_desc}")
    if midi_info:
        print(f"• MIDI Instruments  : {', '.join(midi_info.get('detected_instruments', []))}")
        print(f"• Time Signature    : {midi_info.get('time_signature')}")
    print("\n✨ OPTIMAL ELEVENLABS PROMPT (100% IP-CLEAN):")
    print(f'"{clean_prompt}"')
    print("="*50 + "\n")
    
    return {
        "bpm": bpm,
        "key": key,
        "centroid": centroid,
        "timbre": timbre_desc,
        "dynamic_range": dyn_range,
        "dynamic_arc": arc_desc,
        "clean_prompt": clean_prompt,
        "midi_info": midi_info
    }


if __name__ == "__main__":
    wav = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\caleb\Music\forrester.wav"
    midi = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].endswith((".mid", ".midi")) else None
    png = sys.argv[3] if len(sys.argv) > 3 else "spectrogram.png"
    listen_and_synthesize(wav, midi, png)
