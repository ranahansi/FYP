import moviepy.editor as mp


def audio_segmentation(time_of_visual_changes, main_clip):
    """method to segmenting audio with given time stamps"""
    start_time = 0
    file_name = 1
    audio_list = []
    for stime in time_of_visual_changes:
        audio_file = {}
        time = float(stime)
        print(time)
        audio_file['time'] = time
        clip = mp.VideoFileClip(main_clip).subclip(start_time, time)
        file_path = 'audio set/%s.wav' % file_name
        clip.audio.write_audiofile(file_path)
        start_time = time
        file_name += 1
        audio_file['file path'] = file_path
        audio_list.append(audio_file)

        clip.reader.close()
        clip.audio.reader.close_proc()
    return audio_list
