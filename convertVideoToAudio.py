import moviepy.editor as mp

time_Of_Visual_Changes = [0.07, 0.10, 0.17, 0.31, 0.56, 1.18, 1.39, 2.27, 2.42, 2.51, 3.24, 3.40, 3.46, 3.51, 4.29, 4.46, 5.01, 5.09, 5.51]
start_Time = 0
for time in time_Of_Visual_Changes:
    fileName = time
    time = time*60
    clip = mp.VideoFileClip("data-sets/2.Principles and Words-20190603T102214Z-001/2.Principles and Words/1.mp4").subclip(start_Time, time)
    clip.audio.write_audiofile('audio set/%s.wav' % fileName)
    start_Time = time

    clip.reader.close()
    clip.audio.reader.close_proc()
