import wx
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx import fadein, fadeout
import os

class YTPCreator(wx.Frame):
    def __init__(self, *args, **kw):
        super(YTPCreator, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)

        # Create layout
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.file_list = wx.ListBox(panel, style=wx.LB_MULTIPLE)
        vbox.Add(self.file_list, 1, wx.EXPAND | wx.ALL, 10)

        self.add_button = wx.Button(panel, label='Add Video')
        self.add_button.Bind(wx.EVT_BUTTON, self.OnAdd)
        vbox.Add(self.add_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.create_button = wx.Button(panel, label='Create YTP Video')
        self.create_button.Bind(wx.EVT_BUTTON, self.OnCreate)
        vbox.Add(self.create_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        panel.SetSizer(vbox)
        self.SetSize((400, 300))
        self.SetTitle('Automatic YTP Creator')
        self.Centre()

    def OnAdd(self, event):
        with wx.FileDialog(self, "Open Video file", wildcard="Video files (*.mp4;*.mov;*.avi)|*.mp4;*.mov;*.avi",
                           style=wx.FD_OPEN | wx.FD_MULTIPLE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_OK:
                paths = fileDialog.GetPaths()
                for path in paths:
                    self.file_list.Append(path)

    def OnCreate(self, event):
        clips = []
        for i in range(self.file_list.GetCount()):
            video_path = self.file_list.GetString(i)
            clip = VideoFileClip(video_path)
            # Apply effects: fade in and fade out for 1 second
            clip = fadein(clip, 1).fx(fadeout, 1)
            clips.append(clip)

        # Concatenate clips
        final_clip = concatenate_videoclips(clips)

        # Set duration limit
        if final_clip.duration > 180:
            final_clip = final_clip.subclip(0, 180)

        output_path = wx.SaveFileDialog(self, "Save YTP Video", wildcard="MP4 files (*.mp4)|*.mp4",
                                         style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if output_path.ShowModal() == wx.ID_OK:
            output_file = output_path.GetPath()
            final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

        # Close all clips
        for clip in clips:
            clip.close()

        final_clip.close()

def main():
    app = wx.App(False)
    frame = YTPCreator(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
