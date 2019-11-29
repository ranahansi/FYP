import moviepy.editor as mp


def audioSegmentation():
    time_Of_Visual_Changes = [0.09, 0.11, 0.14, 0.34, 0.57, 1.10, 1.22, 1.45, 1.54, 2.08, 2.24, 2.31, 2.49, 2.58, 3.14, 3.29, 4.08, 4.25, 4.33, 4.40, 4.52, 5.07, 5.31, 5.42, 5.47, 5.51, 5.56]
    start_Time = 0
    audioList = []
    for time in time_Of_Visual_Changes:
        fileName = time
        time = time*60
        clip = mp.VideoFileClip("data-sets/verb tences and verb moods.mp4").subclip(start_Time, time)
        clip.audio.write_audiofile('audio set/%s.wav' % fileName)
        audioList.append('audio set/%s.wav' % fileName)
        start_Time = time

        clip.reader.close()
        clip.audio.reader.close_proc()

    return audioList