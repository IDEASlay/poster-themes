import os
import sys
import fal_client


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        if update.logs:
            for log in update.logs:
                print(f"[fal] {log['message']}")


def generate():
    """
    Forrest Gump - 'Pluma' (Feather Theme)
    Uses fal-ai/minimax-music/v2.6 with strictly isolated style prompt
    and clean lyrical arrangement to prevent prompt recitation.
    """
    style_prompt = (
        "74 BPM Neoclassical Piano and Film Score. Spoken intimate whisper shifting to an urgent, "
        "full-throated female belt with supporting gospel choir, ending in spoken laughter. "
        "Tender, nostalgic, completely drum-free acoustic grand piano, porch-swing arpeggios, and lush orchestral strings."
    )

    lyrics = """[Intro]

[Verse]
oh feather, mi plumita, fly into their...
Run, Forrest. Run!
Ruuuuuuuunnnnnnn
ohhhhhhh
La vida es como un turron de chocolate, en estas navidades turron de chocolate, azucar!
estupido pero, no lo es,
su madre se le dijo,
y ellos le dijeron,
you cant sit here
go fly far far away...
ahhhhhh
please promise me....
ahhhhhhhh
take the feather and...
ahhhhhhhh
dont look back,
oh oh oh oh
don't look for me,
you be the feather and
flyyyyyyyyyyyyy
ahhhhhhhh
be freeeeeee ahhhhhhhhh
Run, my baby,
Ruuuuuuuuunnnnnnnnnn!!!!
that fuckin feather

[Outro]
oooooooohh
oh oh oh oh oh
ahhhhhhhhhhhhhhhhhh
mi plumita tiene que volar libre
plumaaaaaaaaa vuelaaaaaaaaaa"""

    print(f"Submitting 'Pluma' to fal-ai/minimax-music/v2.6...")
    print(f"Style Prompt ({len(style_prompt)} chars): {style_prompt}")
    print(f"Lyrics ({len(lyrics)} chars): {len(lyrics)} chars")

    try:
        result = fal_client.subscribe(
            "fal-ai/minimax-music/v2.6",
            arguments={
                "prompt": style_prompt,
                "lyrics": lyrics,
                "is_instrumental": False,
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
    except Exception as exc:
        print(f"Generation failed with error: {exc}", file=sys.stderr)
        raise

    print("\nGeneration Complete!")
    if "audio" in result and "url" in result["audio"]:
        print(f"Audio URL: {result['audio']['url']}")
    else:
        print("Result payload:", result)
    return result


if __name__ == "__main__":
    generate()
