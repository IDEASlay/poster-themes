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
    Time Traveler Theme - Pure Instrumental Adventure Film Score
    Uses fal-ai/minimax-music/v2.6 with is_instrumental=True to prevent
    the AI vocal synthesizer from speaking or singing prompt text.
    """
    prompt = (
        "Whimsical nostalgic orchestral theme, Alan Silvestri Back to the Future style. "
        "Solo acoustic piano, warm sweeping strings, French horns, subtle orchestral shimmer, "
        "and single cowbell stroke in A major, magical cinematic adventure."
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
