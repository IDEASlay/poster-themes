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
    Raiders March - Pure Instrumental Adventure Film Score
    Uses fal-ai/minimax-music/v2.6 with is_instrumental=True to prevent
    the AI vocal synthesizer from speaking or singing prompt text.
    """
    prompt = (
        "Heroic cinematic adventure march, John Williams Raiders of the Lost Ark style. "
        "Majestic French horns, heraldic trumpets, classical orchestral strings, concert timpani, "
        "and harp glissandos in triumphant C major, brisk energetic march tempo."
    )

    print(f"Submitting instrumental score to fal-ai/minimax-music/v2.6...")
    print(f"Prompt ({len(prompt)} chars): {prompt}")

    try:
        result = fal_client.subscribe(
            "fal-ai/minimax-music/v2.6",
            arguments={
                "prompt": prompt,
                "is_instrumental": True,
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
