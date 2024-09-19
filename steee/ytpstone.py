import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx

class YTPForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic Concat YTP Longest Poopism Effects")

        # Add buttons and labels
        tk.Label(root, text="Select Video Files:").pack()
        self.file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=10)
        self.file_listbox.pack()

        tk.Button(root, text="Add Files", command=self.add_files).pack()
        tk.Button(root, text="Remove Selected", command=self.remove_files).pack()
        tk.Button(root, text="Process Videos", command=self.process_videos).pack()

        tk.Label(root, text="Output Video Duration (minutes):").pack()
        self.duration_entry = tk.Entry(root)
        self.duration_entry.pack()
        self.duration_entry.insert(0, "3")

        self.video_files = []

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        for file in files:
            self.file_listbox.insert(tk.END, file)
            self.video_files.append(file)

    def remove_files(self):
        selected_indices = list(self.file_listbox.curselection())
        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
            del self.video_files[index]

    def process_videos(self):
        if not self.video_files:
            messagebox.showerror("Error", "No files selected")
            return

        try:
            duration = float(self.duration_entry.get())
            if duration <= 0:
                raise ValueError("Duration must be positive")

            clips = [VideoFileClip(f) for f in self.video_files]
            concatenated_clip = concatenate_videoclips(clips)

            # Apply Poopism Effects
            effect_clip = concatenated_clip.fx(vfx.colorx, 0.7)  # Example effect

            # Trim to the desired duration (in minutes)
            max_duration = duration * 120
            if effect_clip.duration > max_duration:
                effect_clip = effect_clip.subclip(0, max_duration)

            output_filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")])
            if output_filename:
                effect_clip.write_videofile(output_filename, codec='libx264')

            messagebox.showinfo("Success", "Video processing complete!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YTPForm(root)
    root.mainloop()
