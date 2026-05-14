from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysubs2
import os

# Define paths
video_path = "input_video.mp4"  # Replace with your video file path
output_video_path = "output_video_with_subtitles.mp4"
srt_file_path = "subtitles.srt"

# Step 1: Create an SRT subtitle file
subtitles = pysubs2.SSAFile()

# Create subtitle entries
# Assuming the video is at least 10 seconds long for this example
subtitles.events.append(
    pysubs2.SSAEvent(
        start=pysubs2.make_time(s=0),  # Start at 0 seconds
        end=pysubs2.make_time(s=5),    # End at 5 seconds
        text="The Secret Keeper of the Universe",
        style="TitleStyle"
    )
)
subtitles.events.append(
    pysubs2.SSAEvent(
        start=pysubs2.make_time(s=5),  # Start at 5 seconds
        end=pysubs2.make_time(s=10),   # End at 10 seconds
        text="Space Stories Trailer",
        style="SubtitleStyle"
    )
)

# Define subtitle styles
subtitles.styles["TitleStyle"] = pysubs2.SSAStyle(
    fontsize=36,  # Larger font for main title
    fontname="Arial",
    primarycolour=pysubs2.Color(255, 255, 255, 0),  # White
    outlinecolour=pysubs2.Color(0, 0, 0, 0),        # Black outline
    outline=2,
    shadow=2,
    alignment=2  # Center alignment
)
subtitles.styles["SubtitleStyle"] = pysubs2.SSAStyle(
    fontsize=24,  # Smaller font for trailer text
    fontname="Arial",
    primarycolour=pysubs2.Color(192, 192, 192, 0),  # Silver
    outlinecolour=pysubs2.Color(0, 0, 0, 0),        # Black outline
    outline=1,
    shadow=1,
    alignment=2  # Center alignment
)

# Save subtitles to SRT file
subtitles.save(srt_file_path, format_="srt")
print(f"Subtitle file created: {srt_file_path}")

# Step 2: Load video and add subtitles
video_clip = VideoFileClip(video_path)

# Create a subtitle generator function for moviepy


def make_textclip(txt):
    return TextClip(
        txt,
        font="Arial",
        fontsize=36 if txt == "The Secret Keeper of the Universe" else 24,
        color="white" if txt == "The Secret Keeper of the Universe" else "silver",
        stroke_color="black",
        stroke_width=2 if txt == "The Secret Keeper of the Universe" else 1,
        method="caption",
        align="center",
        size=(video_clip.w, None)
    ).set_position(("center", "bottom"))


# Load subtitles into moviepy
subtitles_clip = SubtitlesClip(srt_file_path, make_textclip)

# Composite video with subtitles
final_clip = CompositeVideoClip([video_clip, subtitles_clip.set_pos(("center", "bottom"))])

# Step 3: Export the final video
final_clip.write_videofile(
    output_video_path,
    codec="libx264",
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True,
    fps=video_clip.fps
)
print(f"Video with subtitles created: {output_video_path}")

# Clean up
video_clip.close()
final_clip.close()