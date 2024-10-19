import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from utils.transcription import transcribe_video
from utils.video_editor import cut_video
from PIL import Image, ImageTk
import os
import threading
import time


class VideoTranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Transcription & Clipper")
        self.root.geometry("550x650")
        self.root.configure(bg='#2c2c34')
        self.center_window()

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Create frames for each tab
        self.home_frame = ttk.Frame(self.notebook)
        self.clips_frame = ttk.Frame(self.notebook)
        self.transcriptions_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.home_frame, text='Home')
        self.notebook.add(self.clips_frame, text='Clips')
        self.notebook.add(self.transcriptions_frame, text='Transcriptions')

        # Responsive and Scrollable sections setup
        self.home_canvas = tk.Canvas(self.home_frame, bg='#2c2c34')
        self.home_scrollbar = ttk.Scrollbar(self.home_frame, orient="vertical", command=self.home_canvas.yview)
        self.home_scrollable_frame = ttk.Frame(self.home_canvas)

        self.home_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.home_canvas.configure(
                scrollregion=self.home_canvas.bbox("all")
            )
        )

        # Home Canvas Setup with Responsive Centering
        self.home_canvas.create_window((0, 0), window=self.home_scrollable_frame,
                                       anchor="n")  # anchor 'n' centers it horizontally
        self.home_canvas.configure(yscrollcommand=self.home_scrollbar.set)

        self.home_canvas.pack(side="left", fill="both", expand=True)
        self.home_scrollbar.pack(side="right", fill="y")

        # Centering and Propagating space for the scrollable frame
        self.home_scrollable_frame.pack_propagate(False)  # Prevent widgets from resizing their container
        self.home_scrollable_frame.update_idletasks()  # Ensure geometry updates

        # Home Tab Setup - Centered and Responsive
        self.title_label = tk.Label(self.home_scrollable_frame, text="Video Transcription & Clipper",
                                    font=("Helvetica", 25, "bold"), bg='#44475a', fg='white')
        self.title_label.pack(pady=20)

        self.upload_button = tk.Button(self.home_scrollable_frame, text="Upload Video", command=self.upload_video,
                                       font=("Helvetica", 16), bg='#50fa7b', fg='black', width=20, height=2)
        self.upload_button.pack(pady=(20, 10))  # Padding to make space responsive

        self.add_clip_button = tk.Button(self.home_scrollable_frame, text="Add Clip", command=self.add_clip_fields,
                                         font=("Helvetica", 16), bg='#ff79c6', fg='black', width=20, height=2)
        self.add_clip_button.pack(pady=10)

        self.cut_button = tk.Button(self.home_scrollable_frame, text="Cut Videos", command=self.cut_videos,
                                    font=("Helvetica", 16), bg='#bd93f9', fg='black', width=20, height=2)
        self.cut_button.pack(pady=10)

        self.transcription_button = tk.Button(self.home_scrollable_frame, text="Generate Transcription",
                                              command=self.generate_transcription, font=("Helvetica", 16), bg='#ffb86c',
                                              fg='black', width=25, height=2)
        self.transcription_button.pack(pady=10)

        self.progress_label = tk.Label(self.home_scrollable_frame, text="", font=("Helvetica", 14), bg='#2c2c34',
                                       fg='white')
        self.progress_label.pack(pady=10)

        # Make sure the main frame resizes accordingly
        self.home_scrollable_frame.pack(expand=True, fill="both")  # Make frame fill its space
        self.home_canvas.pack(expand=True, fill="both")

        # Clips Tab Setup
        self.clips_label = tk.Label(self.clips_frame, text="Clips:", font=("Helvetica", 16, "bold"), bg='#2c2c34', fg='white')
        self.clips_label.pack(pady=10)

        self.clips_listbox = tk.Listbox(self.clips_frame, width=70, font=("Helvetica", 12), bg='#282a36', fg='white')
        self.clips_listbox.pack(pady=5, fill="both", expand=True)

        self.view_clip_button = tk.Button(self.clips_frame, text="View Clip", command=self.view_clip, font=("Helvetica", 14), bg='#8be9fd', fg='black', width=15)
        self.view_clip_button.pack(pady=10)

        # Transcriptions Tab Setup
        self.transcriptions_label = tk.Label(self.transcriptions_frame, text="Transcriptions Folder", font=("Helvetica", 16, "bold"), bg='#2c2c34', fg='white')
        self.transcriptions_label.pack(pady=10)

        self.transcriptions_button = tk.Button(self.transcriptions_frame, text="Open Transcriptions Folder", command=self.open_transcriptions_folder, font=("Helvetica", 14), bg='#ffb86c', fg='black', width=25)
        self.transcriptions_button.pack(pady=10)

        self.clips_folder_label = tk.Label(self.transcriptions_frame, text="Clips Folder", font=("Helvetica", 16, "bold"), bg='#2c2c34', fg='white')
        self.clips_folder_label.pack(pady=10)

        self.clips_folder_button = tk.Button(self.transcriptions_frame, text="Open Clips Folder", command=self.open_clips_folder, font=("Helvetica", 14), bg='#bd93f9', fg='black', width=25)
        self.clips_folder_button.pack(pady=10)

        self.video_path = ""
        self.clip_entries = []

        # Make the window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.grid_columnconfigure(0, weight=1)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def upload_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mov;*.avi")])
        if self.video_path:
            messagebox.showinfo("Video Uploaded", f"Video successfully uploaded: {os.path.basename(self.video_path)}")

    def add_clip_fields(self):
        clip_frame = tk.Frame(self.home_scrollable_frame, bg='#2c2c34')
        clip_frame.pack(pady=5, fill="x")

        start_label = tk.Label(clip_frame, text="Start Time (MM:SS):", font=("Helvetica", 12), bg='#2c2c34', fg='white')
        start_label.grid(row=0, column=0, padx=5)
        start_entry = tk.Entry(clip_frame, width=10, font=("Helvetica", 12), bg='#44475a', fg='white')
        start_entry.grid(row=0, column=1, padx=5)

        end_label = tk.Label(clip_frame, text="End Time (MM:SS):", font=("Helvetica", 12), bg='#2c2c34', fg='white')
        end_label.grid(row=0, column=2, padx=5)
        end_entry = tk.Entry(clip_frame, width=10, font=("Helvetica", 12), bg='#44475a', fg='white')
        end_entry.grid(row=0, column=3, padx=5)

        self.clip_entries.append((start_entry, end_entry))

    def cut_videos(self):
        if not self.video_path:
            messagebox.showerror("Error", "Please upload a video first.")
            return

        threading.Thread(target=self._cut_videos_thread).start()

    def _cut_videos_thread(self):
        self.progress_label.config(text="Cutting videos, please wait...")
        for index, (start_entry, end_entry) in enumerate(self.clip_entries, start=1):
            start_time = start_entry.get()
            end_time = end_entry.get()
            if not start_time or not end_time:
                messagebox.showerror("Error", "Please enter both start and end times for all clips.")
                return

            try:
                start_minutes, start_seconds = map(int, start_time.split(":"))
                end_minutes, end_seconds = map(int, end_time.split(":"))
                start_time_seconds = start_minutes * 60 + start_seconds
                end_time_seconds = end_minutes * 60 + end_seconds

                output_path = cut_video(self.video_path, start_time_seconds, end_time_seconds)
                self.clips_listbox.insert(tk.END, output_path)
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter valid times in MM:SS format.")
                return

            self.progress_label.config(text=f"Processing clip {index}/{len(self.clip_entries)}... Done!")
            time.sleep(0.5)

        self.progress_label.config(text="All video clips created successfully!")
        messagebox.showinfo("Success", "All video clips created successfully!")

    def generate_transcription(self):
        if not self.video_path:
            messagebox.showerror("Error", "Please upload a video first.")
            return

        threading.Thread(target=self._generate_transcription_thread).start()

    def _generate_transcription_thread(self):
        self.progress_label.config(text="Generating transcription, please wait...")

        transcription_result = transcribe_video(self.video_path)

        if transcription_result and "segments" in transcription_result:
            transcription_file = f"transcriptions/{os.path.basename(self.video_path).split('.')[0]}.srt"
            os.makedirs(os.path.dirname(transcription_file), exist_ok=True)

            with open(transcription_file, "w") as f:
                for segment in transcription_result['segments']:
                    start = segment['start']
                    end = segment['end']
                    text = segment['text']
                    f.write(
                        f"{segment['id']}\n{self.format_timestamp(start)} --> {self.format_timestamp(end)}\n{text.strip()}\n\n")

            self.progress_label.config(text="Transcription generated successfully!")
            messagebox.showinfo("Success", "Transcription generated successfully!")
        else:
            self.progress_label.config(text="Failed to generate transcription.")
            messagebox.showerror("Error", "Failed to generate transcription.")

    def format_timestamp(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def view_clip(self):
        selected_clip = self.clips_listbox.get(tk.ACTIVE)
        if selected_clip:
            os.system(f"start {selected_clip}")

    def open_transcriptions_folder(self):
        os.system(f'start transcriptions')

    def open_clips_folder(self):
        os.system(f'start clips')


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoTranscriptionApp(root)
    root.mainloop()
