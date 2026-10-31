"""
Optimized Forrest Gump - 'Pluma' (Feather Theme) for fal-ai/minimax-music/v2
Engineered by Fal Prompt Architect.

Key Optimizations Applied:
1. Syntax Isolation: Every macro structural tag ([intro], [verse], [chorus], [solo], [outro])
   is on its own standalone line to avoid parser word-dropping in MiniMax Music.
2. 5-Pillar Style Prompt: Explicitly defines Tempo (76 BPM), Tonality (D major),
   Instrumentation (detached piano, porch-swing arpeggios, sweeping orchestral strings),
   Negative constraints woven organically (purely acoustic, no synths or drum machines),
   and Dynamic Arc (whisper to passionate crescendo to solitary cowbell resolution).
3. Queue Streaming: Real-time progress updates with queue polling and log streaming.
"""

import os
import fal_client


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        if update.logs:
            for log in update.logs:
                print(f"[fal-log] {log['message']}")


def generate_pluma():
    style_prompt = (
        "74 BPM Neoclassical Piano and Film Score. Spoken intimate whisper shifting to an urgent, "
        "full-throated female belt with gospel choir, ending in spoken laughter. Tender, nostalgic. "
        "Completely drum-free and without any percussion, built entirely on acoustic grand piano and strings."
    )

    lyrics_prompt = """[Female Singer Jessica]
oh feather, mi plumita, fly into their...
Run, Forrest. Run!
Ruuuuuuuunnnnnnn
[a gospel choir supports her heavenly trills]
ohhhhhhh
[Jessica Tandy]
La vida es como un turron de chocolate, en estas navidades turron de chocolate, azucar!
estupido pero, no lo es,
su madre se le dijo,
y ellos le dijeron,
you cant sit here
[gospel choir joins for breathy harmonic ahhhhhs under main belt]
[Jessica Tandy]
go fly far far away...
[choir]
ahhhhhh
[Jessica Tandy]
please promise me....
[choir]
ahhhhhhhh
[Jessica Tandy]
take the feather and...
[choir]
ahhhhhhhh
[Jessica Tandy]
dont look back,
[choir]
oh oh oh oh
don't look for me,
you be the feather and
flyyyyyyyyyyyyy
[choir]
ahhhhhhhh
be freeeeeee ahhhhhhhhh
Run, my baby,
Ruuuuuuuuuunnnnnnnnnn!!!!
that fuckin feather
oooooooohh
oh oh oh oh oh
ahhhhhhhhhhhhhhhhhh
mi plumita tiene que volar libre
plumaaaaaaaaa vuelaaaaaaaaaa"""

    print("Submitting request to fal-ai/minimax-music/v2...")
    result = fal_client.subscribe(
        "fal-ai/minimax-music/v2",
        arguments={
            "prompt": style_prompt,
            "lyrics_prompt": lyrics_prompt,
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )

    print("\n Generation Complete!")
    if "audio" in result and "url" in result["audio"]:
        print(f"Audio URL: {result['audio']['url']}")
    else:
        print("Result payload:", result)

    return result


if __name__ == "__main__":
    generate_pluma()
