import asyncio

from agent import run_video_analysis


if __name__ == "__main__":
    result = asyncio.run(
        run_video_analysis(
            "https://youtu.be/ChoV5h7tw5A?si=v_2pxObmdpx0czjS",
            "Summarize this video with action items.",
        )
    )
    print(result)