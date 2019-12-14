import moviepy.editor as mp


def audio_segmentation():
    """method to segmenting audio with given time stamps"""
    time_of_visual_changes = [0.09, 0.11, 0.14, 0.34, 0.57, 1.10, 1.22, 1.45, 1.54, 2.08, 2.24, 2.31, 2.49, 2.58, 3.14, 3.29, 4.08, 4.25, 4.33, 4.40, 4.52, 5.07, 5.31, 5.42, 5.47, 5.51, 5.56]
    start_time = 0
    file_name = 1
    audio_list = []
    for time in time_of_visual_changes:
        audio_file = {}
        audio_file['time'] = time
        time = time*60
        clip = mp.VideoFileClip("data-sets/verb tenses and verb moods.mp4")\
            .subclip(start_time, time)
        file_path = 'audio set/%s.wav' % file_name
        clip.audio.write_audiofile(file_path)
        start_time = time
        file_name += 1
        audio_file['file path'] = file_path
        audio_list.append(audio_file)

        clip.reader.close()
        clip.audio.reader.close_proc()
    return audio_list
