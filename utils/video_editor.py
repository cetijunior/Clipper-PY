from moviepy.video.io.VideoFileClip import VideoFileClip
import os


def cut_video(video_path, start_time, end_time):
    try:
        video = VideoFileClip(video_path).subclip(start_time, end_time)
        output_path = f"clips/{os.path.basename(video_path).split('.')[0]}_clip_{start_time}_{end_time}.mp4"
        video.write_videofile(output_path, codec='libx264')
        video.close()
        return output_path
    except Exception as e:
        print(f"Error: {e}")
        return ""