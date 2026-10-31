# fal.ai Music Generation Guide & Acoustic Intelligence Dossier
### Album: Poster-Themes

---

## 🎧 Grounded Acoustic Signal Analysis (All 6 Themes)

Every track in this suite was physically analyzed by the **Acoustic Ear & Music Intelligence Agent** (`audio_ear.py`).
- **Spectrograms**: Short-Time Fourier Transform (STFT) power distributions saved in each track folder.
- **BPM**: Spectral flux onset envelope autocorrelation.
- **Key**: Krumhansl-Schmuckler chroma profile correlation across 12 pitch classes.
- **Timbre & Dynamics**: Spectral Centroid (Hz) and RMS dynamic range curves.
- **MIDI Data**: Multi-track event parsing for note density, time signatures, and General MIDI instrumentation.

### Master Acoustic Dossier

| # | Track | Reference Audio File | BPM | Detected Key | Centroid | Dynamic Arc | Rendered Spectrogram |
|---|---|---|:---:|:---:|:---:|---|:---:|
| **01** | *Gremlins* | `Gremlins Theme HD [RGLoLphCeGI].wav` | **120** | **F# minor** | 3965 Hz | Steady, noble, syncopated | [spectrogram.png](file:///c:/Users/caleb/Documents/bitwize-music/poster-themes/01-gremlins/spectrogram.png) |
| **02** | *Indiana Jones* | `Indiana Jones Theme Song [HD] [-bTpp8PQSog].wav` | **128** | **F major** | 1625 Hz | Patient crescendo to symphonic climax | [spectrogram.png](file:///c:/Users/caleb/Documents/bitwize-music/poster-themes/02-indiana-jones/spectrogram.png) |
| **03** | *Star Wars* | `Star Wars Intro HD 1080p [tGsKzZtRwxw].wav` | **104** | **A# minor** | 1875 Hz | Grand opening to tender resolution | [spectrogram.png](file:///c:/Users/caleb/Documents/bitwize-music/poster-themes/03-star-wars/spectrogram.png) |
| **04** | *Back to the Future* | `The Back to the Future Theme Tune [e8TZbze72Bc].wav` | **94** | **G# minor** | 2308 Hz | Steady, noble, deeply expressive | [spectrogram.png](file:///c:/Users/caleb/Documents/bitwize-music/poster-themes/04-back-to-future/spectrogram.png) |
| **05** | *Jurassic Park* | `Theme From Jurassic Park [lDlU08RU7Tk].wav` | **94** | **A# major** | 1653 Hz | Intimate whisper to majestic climax | [spectrogram.png](file:///c:/Users/caleb/Documents/bitwize-music/poster-themes/05-jurassic-park/spectrogram.png) |
| **06** | *Forrest Gump* | `forrester.wav` | **94** | **B major** | 1511 Hz | Grand opening to fragile piano coda | [spectrogram.png](file:///c:/Users/caleb/Documents/bitwize-music/poster-themes/06-forrest-gump/spectrogram.png) |

---

## ⚖️ Legal & Copyright Compliance (ElevenLabs Safe)

> [!CAUTION]
> **STRICT ZERO-IP POLICY**: To prevent copyright infringement, API moderation triggers, and legal liability, prompts sent to `fal-ai/elevenlabs/music` **MUST NEVER** mention real living or deceased composers (e.g., John Williams, Alan Silvestri, Jerry Goldsmith, Hans Zimmer) or copyrighted film titles/franchises.
>
> All compositions are described strictly using **measured music theory, tonality, tempo (BPM), acoustic orchestration, and instrument articulation**.

---

## 🏆 Recommended Engine: ElevenLabs Music (`fal-ai/elevenlabs/music`)

- **Vocal Suppression**: Set `"force_instrumental": True` to guarantee 100% vocal-free instrumental scores (eliminates all spoken/sung prompt artifacts).
- **Duration Control**: Specify `"music_length_ms"` (e.g., `60000` = 60s, `75000` = 75s).
- **Master Script**: Run via [generate_elevenlabs.py](file:///c:/Users/caleb/Documents/bitwize-music/poster-themes/generate_elevenlabs.py).

---

## Agent Definitions in Codex

- **Acoustic Ear Agent**: [audio-acoustic-ear.toml](file:///c:/Users/caleb/.codex/agents/audio-acoustic-ear.toml)
- **ElevenLabs Maestro Agent**: [elevenlabs-music-agent.toml](file:///c:/Users/caleb/.codex/agents/elevenlabs-music-agent.toml)
