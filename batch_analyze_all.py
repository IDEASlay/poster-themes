import os
import sys
import json
from audio_ear import listen_and_synthesize

TRACKS = [
    {
        "id": "gremlins",
        "title": "Quirky Ragtime Horror Comedy",
        "wav": r"C:\Users\caleb\Music\Gremlins Theme HD [RGLoLphCeGI].wav",
        "midi": r"C:\Users\caleb\Documents\bitwize-music\poster-themes\01-gremlins\gremlins_hook_clean.mid",
        "png": r"C:\Users\caleb\Documents\bitwize-music\poster-themes\01-gremlins\spectrogram.png",
        "orchestration": "upright ragtime tack piano lead, playful pizzicato strings, bright xylophone runs, triangle accents, and a single dry cowbell hit",
    },
    {
        "id": "indiana_jones",
        "title": "Swashbuckling Adventure March",
        "wav": r"C:\Users\caleb\Music\Indiana Jones Theme Song [HD] [-bTpp8PQSog].wav",
        "midi": None,
        "png": r"C:\Users\caleb\Documents\bitwize-music\poster-themes\02-indiana-jones\spectrogram.png",
        "orchestration": "majestic unison French horn fanfares, crisp heraldic trumpets, soaring classical violins, concert timpani, and rapid harp glissandos",
    },
    {
        "id": "star_wars",
        "title": "Grand Space Opera Fanfare",
        "wav": r"C:\Users\caleb\Music\Star Wars Intro HD 1080p [tGsKzZtRwxw].wav",
        "midi": None,
        "png": r"C:\Users\caleb\Documents\bitwize-music\poster-themes\03-star-wars\spectrogram.png",
        "orchestration": "stately four-part brass chorale, brilliant virtuoso trumpet fanfare, sweeping symphonic string section, deep thunderous orchestral timpani rolls, and ringing tubular bells",
    },
    {
        "id": "back_to_future",
        "title": "Time Traveler Orchestral Adventure",
        "wav": r"C:\Users\caleb\Music\The Back to the Future Theme Tune [e8TZbze72Bc].wav",
        "midi": None,
        "png": r"C:\Users\caleb\Documents\bitwize-music\poster-themes\04-back-to-future\spectrogram.png",
        "orchestration": "delicate acoustic grand piano intro blooming into soaring warm violins, noble lyrical French horns, sparkling orchestral chimes, and a single dry cowbell stroke",
    },
    {
        "id": "jurassic_park",
        "title": "Majestic Prehistoric Symphonic Hymn",
        "wav": r"C:\Users\caleb\Music\Theme From Jurassic Park [lDlU08RU7Tk].wav",
        "midi": None,
        "png": r"C:\Users\caleb\Documents\bitwize-music\poster-themes\05-jurassic-park\spectrogram.png",
        "orchestration": "deep warm cello and double bass foundation, noble expressive French horn melody, lyrical pastoral woodwinds, sweeping romantic violins, and a soaring triumphant brass chorale",
    },
    {
        "id": "pluma",
        "title": "Neoclassical Porch Swing Piano Theme",
        "wav": r"C:\Users\caleb\Music\forrester.wav",
        "midi": None,
        "png": r"C:\Users\caleb\Documents\bitwize-music\poster-themes\06-forrest-gump\spectrogram.png",
        "orchestration": "solo acoustic grand piano with gentle rocking porch-swing arpeggios, warm sustained bass notes, soaring emotional cello countermelodies, and lush symphonic strings",
    },
]


def run_batch():
    results = {}
    print("=" * 60)
    print("🚀 ACOUSTIC EAR BATCH ANALYSIS SUITE (ALL 6 POSTER THEMES)")
    print("=" * 60)

    for track in TRACKS:
        tid = track["id"]
        print(f"\n>>> Analyzing: [{tid.upper()}] {track['title']}...")
        if not os.path.exists(track["wav"]):
            print(f"❌ Error: WAV file not found: {track['wav']}", file=sys.stderr)
            continue

        try:
            dossier = listen_and_synthesize(
                wav_path=track["wav"],
                midi_path=track["midi"] if track.get("midi") and os.path.exists(track["midi"]) else None,
                output_png=track["png"]
            )
            
            # Tailor the clean prompt with the acoustic analysis + specific orchestral palette
            bpm = dossier["bpm"]
            key = dossier["key"]
            timbre = dossier["timbre"]
            arc = dossier["dynamic_arc"]
            orch = track["orchestration"]
            
            tailored_prompt = (
                f"{bpm} BPM cinematic orchestral theme in {key}. "
                f"{timbre}. {arc}. "
                f"Featuring {orch}. "
                f"Completely drum-free, pristine acoustic film score recording."
            )
            
            dossier["tailored_prompt"] = tailored_prompt
            results[tid] = dossier
            print(f"✅ [{tid}] Analysis complete. Spectrogram saved.")
            print(f"✨ Acoustically Grounded Prompt:\n\"{tailored_prompt}\"")
        except Exception as e:
            print(f"❌ Failed analyzing {tid}: {e}", file=sys.stderr)

    # Save summary json
    summary_path = r"C:\Users\caleb\Documents\bitwize-music\poster-themes\acoustic_intelligence_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        # filter out numpy types
        clean_results = {}
        for k, v in results.items():
            clean_results[k] = {
                "bpm": int(v["bpm"]),
                "key": str(v["key"]),
                "centroid": float(v["centroid"]),
                "timbre": str(v["timbre"]),
                "dynamic_range": float(v["dynamic_range"]),
                "dynamic_arc": str(v["dynamic_arc"]),
                "tailored_prompt": str(v["tailored_prompt"]),
                "midi_info": v.get("midi_info")
            }
        json.dump(clean_results, f, indent=2)
    print(f"\nMaster dossier written to: {summary_path}")
    return results


if __name__ == "__main__":
    run_batch()
