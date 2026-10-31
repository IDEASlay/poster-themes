import os
import sys
import fal_client

# ==============================================================================
# ACOUSTICALLY GROUNDED & 100% IP-CLEAN POSTER THEMES (ELEVENLABS)
# Derived directly from signal-processing analysis (STFT spectrogram,
# spectral flux onset BPM, and Krumhansl-Schmuckler chroma profiling).
# Zero real composer names. Zero trademarked film titles.
# ==============================================================================

THEMES = {
    "gremlins": {
        "title": "Quirky Ragtime Horror Comedy (Acoustically Grounded)",
        "prompt": (
            "120 BPM cinematic orchestral theme in F# minor. "
            "Brilliant, crystalline, brass-forward and soaring high-register presence. "
            "Steady, noble, and deeply expressive melodic flow. "
            "Featuring upright ragtime tack piano lead, playful pizzicato strings, "
            "bright xylophone runs, triangle accents, and a single dry cowbell hit. "
            "Completely drum-free, pristine acoustic film score recording."
        ),
        "duration_ms": 60000,
    },
    "indiana_jones": {
        "title": "Swashbuckling Adventure March (Acoustically Grounded)",
        "prompt": (
            "128 BPM cinematic orchestral theme in F major. "
            "Balanced lyrical acoustic warmth with sparkling, expressive overtones. "
            "Intimate whisper building in a patient crescendo to a sweeping symphonic climax. "
            "Featuring majestic unison French horn fanfares, crisp heraldic trumpets, "
            "soaring classical violins, concert timpani, and rapid harp glissandos. "
            "Completely drum-free, pristine acoustic film score recording."
        ),
        "duration_ms": 60000,
    },
    "star_wars": {
        "title": "Grand Space Opera Fanfare (Acoustically Grounded)",
        "prompt": (
            "104 BPM cinematic orchestral theme in A# minor. "
            "Balanced lyrical acoustic warmth with sparkling, expressive overtones. "
            "Grand emotional opening gradually softening into a tender, contemplative resolution. "
            "Featuring stately four-part brass chorale, brilliant virtuoso trumpet fanfare, "
            "sweeping symphonic string section, deep thunderous orchestral timpani rolls, "
            "and ringing tubular bells. Completely drum-free, pristine acoustic film score recording."
        ),
        "duration_ms": 60000,
    },
    "back_to_future": {
        "title": "Time Traveler Orchestral Adventure (Acoustically Grounded)",
        "prompt": (
            "94 BPM cinematic orchestral theme in G# minor. "
            "Brilliant, crystalline, brass-forward and soaring high-register presence. "
            "Steady, noble, and deeply expressive melodic flow. "
            "Featuring delicate acoustic grand piano intro blooming into soaring warm violins, "
            "noble lyrical French horns, sparkling orchestral chimes, and a single dry cowbell stroke. "
            "Completely drum-free, pristine acoustic film score recording."
        ),
        "duration_ms": 60000,
    },
    "jurassic_park": {
        "title": "Majestic Prehistoric Symphonic Hymn (Acoustically Grounded)",
        "prompt": (
            "94 BPM cinematic orchestral theme in A# major. "
            "Balanced lyrical acoustic warmth with sparkling, expressive overtones. "
            "Intimate whisper building in a patient crescendo to a sweeping symphonic climax. "
            "Featuring deep warm cello and double bass foundation, noble expressive French horn melody, "
            "lyrical pastoral woodwinds, sweeping romantic violins, and a soaring triumphant brass chorale. "
            "Completely drum-free, pristine acoustic film score recording."
        ),
        "duration_ms": 60000,
    },
    "pluma": {
        "title": "Neoclassical Porch Swing Piano Theme (Acoustically Grounded)",
        "prompt": (
            "94 BPM cinematic orchestral theme in B major. "
            "Balanced lyrical acoustic warmth with sparkling, expressive overtones. "
            "Grand emotional opening gradually softening into a tender, contemplative resolution. "
            "Featuring solo acoustic grand piano with gentle rocking porch-swing arpeggios, "
            "warm sustained bass notes, soaring emotional cello countermelodies, and lush symphonic strings. "
            "Completely drum-free, pristine acoustic film score recording."
        ),
        "duration_ms": 75000,
    },
}


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        if update.logs:
            for log in update.logs:
                print(f"[fal-elevenlabs] {log['message']}")


def generate_theme(theme_key="indiana_jones"):
    if theme_key not in THEMES:
        available = ", ".join(THEMES.keys())
        raise ValueError(f"Unknown theme: '{theme_key}'. Choose from: {available}")

    theme = THEMES[theme_key]
    print(f"\n==========================================")
    print(f"Generating: {theme['title']}")
    print(f"Endpoint: fal-ai/elevenlabs/music")
    print(f"Force Instrumental: TRUE (Zero vocals guaranteed)")
    print(f"Duration: {theme['duration_ms'] / 1000} seconds")
    print(f"Prompt: {theme['prompt']}")
    print(f"==========================================\n")

    arguments = {
        "prompt": theme["prompt"],
        "force_instrumental": True,
        "music_length_ms": theme["duration_ms"],
        "output_format": "mp3_44100_128",
    }

    try:
        result = fal_client.subscribe(
            "fal-ai/elevenlabs/music",
            arguments=arguments,
            with_logs=True,
            on_queue_update=on_queue_update,
        )
    except Exception as exc:
        print(f"ElevenLabs generation failed: {exc}", file=sys.stderr)
        raise

    print("\nGeneration Complete!")
    audio_url = result.get("audio", {}).get("url")
    print(f"Audio URL: {audio_url}")
    return result


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "indiana_jones"
    generate_theme(key)
