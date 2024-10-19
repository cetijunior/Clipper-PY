import whisper
import os
from moviepy.editor import AudioFileClip

def transcribe_video(video_path):
    audio_path = "temp_audio.wav"
    try:
        # Extract audio from video
        print(f"Extracting audio from video: {video_path}")
        audio_clip = AudioFileClip(video_path)
        audio_clip.write_audiofile(audio_path)
        audio_clip.close()

        # Load the Whisper model
        print("Loading Whisper model...")
        model = whisper.load_model("base")  # Choose model size based on your needs

        # Transcribe audio
        print("Transcribing audio...")
        result = model.transcribe(audio_path)

        if result and "text" in result:
            transcription_text = result["text"]
            print(f"Transcription successful: {transcription_text[:100]}...")  # Log first 100 characters
            return result
        else:
            print("No transcription text found in the result.")
            return None

    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print("Temporary audio file removed.")
