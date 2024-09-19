import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from pydub import AudioSegment
import random

# Directories for song covers and videos
audio_dir = 'path_to_audio_directory'
video_dir = 'path_to_video_directory'
output_dir = 'path_to_output_directory'

# Get list of video and audio files
video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov'))]
audio_files = [f for f in os.listdir(audio_dir) if f.endswith(('.mp3', '.wav'))]

def create_audio_mix(audio_files, output_audio):
    """Mix audio covers randomly into a single audio track"""
    mixed_audio = None
    
    for audio_file in audio_files:
        audio_path = os.path.join(audio_dir, audio_file)
        cover_audio = AudioSegment.from_file(audio_path)

        # If it's the first track, assign it as mixed_audio, else overlay
        if mixed_audio is None:
            mixed_audio = cover_audio
        else:
            mixed_audio = mixed_audio.overlay(cover_audio)
    
    mixed_audio.export(output_audio, format="mp3")

def create_video_remix(video_files, output_video, audio_file):
    """Create a remix of video clips and sync it with the mixed audio"""
    video_clips = []
    for video_file in video_files:
        video_path = os.path.join(video_dir, video_file)
        clip = VideoFileClip(video_path)
        video_clips.append(clip)

    # Randomize order of videos
    random.shuffle(video_clips)

    # Concatenate all video clips together
    final_video = concatenate_videoclips(video_clips)

    # Load the mixed audio
    mixed_audio = AudioFileClip(audio_file)

    # Set the audio of the final video to the mixed audio
    final_video = final_video.set_audio(mixed_audio)

    # Export the final video
    final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")

def main():
    # Define output files
    output_audio = os.path.join(output_dir, 'mixed_audio.mp3')
    output_video = os.path.join(output_dir, 'video_remix.mp4')

    # Step 1: Create mixed audio
    create_audio_mix(audio_files, output_audio)

    # Step 2: Create video remix and sync with mixed audio
    create_video_remix(video_files, output_video, output_audio)

if __name__ == '__main__':
    main()
