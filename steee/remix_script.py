import os
import random
import argparse
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from pydub import AudioSegment
from tqdm import tqdm  # For progress reporting

# Fixed configuration (you can adjust it)
SUPPORTED_VIDEO_FORMATS = ('.mp4', '.avi', '.mov')
SUPPORTED_AUDIO_FORMATS = ('.mp3', '.wav')

def create_audio_mix(audio_files, output_audio):
    """Mix audio covers randomly into a single audio track."""
    mixed_audio = None
    
    print("\nMixing audio covers...")
    for audio_file in tqdm(audio_files, desc="Processing Audio"):
        audio_path = os.path.join(audio_dir, audio_file)
        cover_audio = AudioSegment.from_file(audio_path)

        # If it's the first track, assign it as mixed_audio, else overlay
        if mixed_audio is None:
            mixed_audio = cover_audio
        else:
            mixed_audio = mixed_audio.overlay(cover_audio)
    
    mixed_audio.export(output_audio, format="mp3")
    print(f"Mixed audio exported to {output_audio}")

def create_video_remix(video_files, output_video, audio_file):
    """Create a remix of video clips and sync it with the mixed audio."""
    video_clips = []
    print("\nCreating video remix...")

    for video_file in tqdm(video_files, desc="Processing Video"):
        video_path = os.path.join(video_dir, video_file)
        clip = VideoFileClip(video_path)
        video_clips.append(clip)

    # Randomize order of videos
    random.shuffle(video_clips)

    # Concatenate all video clips together
    final_video = concatenate_videoclips(video_clips)

    # Load the mixed audio
    mixed_audio = AudioFileClip(audio_file)

    # Trim or loop video if necessary to match audio length
    if final_video.duration > mixed_audio.duration:
        final_video = final_video.subclip(0, mixed_audio.duration)
    else:
        final_video = concatenate_videoclips([final_video] * (int(mixed_audio.duration // final_video.duration)) + [final_video.subclip(0, mixed_audio.duration % final_video.duration)])

    # Set the audio of the final video to the mixed audio
    final_video = final_video.set_audio(mixed_audio)

    # Export the final video
    final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")
    print(f"Final video exported to {output_video}")

def main(audio_dir, video_dir, output_dir):
    # Get list of video and audio files
    video_files = [f for f in os.listdir(video_dir) if f.endswith(SUPPORTED_VIDEO_FORMATS)]
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith(SUPPORTED_AUDIO_FORMATS)]

    # Check if there are video and audio files
    if not video_files:
        print(f"No video files found in {video_dir}")
        return
    if not audio_files:
        print(f"No audio files found in {audio_dir}")
        return

    # Define output files
    output_audio = os.path.join(output_dir, 'mixed_audio.mp3')
    output_video = os.path.join(output_dir, 'video_remix.mp4')

    # Step 1: Create mixed audio
    create_audio_mix(audio_files, output_audio)

    # Step 2: Create video remix and sync with mixed audio
    create_video_remix(video_files, output_video, output_audio)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Video Remix Songs - Covers Mix")
    
    parser.add_argument('--audio-dir', type=str, required=True, help="Directory containing audio covers")
    parser.add_argument('--video-dir', type=str, required=True, help="Directory containing video clips")
    parser.add_argument('--output-dir', type=str, required=True, help="Directory to save the output video and audio")
    
    args = parser.parse_args()

    audio_dir = args.audio_dir
    video_dir = args.video_dir
    output_dir = args.output_dir

    # Check if output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Run the main process
    main(audio_dir, video_dir, output_dir)
