import moviepy.editor as mp
from pydub import AudioSegment


def audio_segmentation(time_of_visual_changes, main_clip):
    """method to segmenting audio with given time stamps"""
    start_time = 0
    file_name = 1
    audio_list = []
    # segmenting audio file.
    for stime in time_of_visual_changes:
        audio_file = {}
        time = float(stime)
        print(time)
        audio_file['time'] = time
        # main clip segment to sub clips.
        clip = mp.VideoFileClip(main_clip).subclip(start_time, time)
        file_path = 'audio set/'+str(file_name)+'.wav'
        clip.audio.write_audiofile(file_path)
        start_time = time
        file_name += 1
        audio_file['file path'] = file_path
        audio_file['duration'] = clip.duration
        audio_list.append(audio_file)

        # close the audio file reader.
        clip.reader.close()
        clip.audio.reader.close_proc()
    return audio_list


def sub_audio_segmentation(time_stamp, main_clip, audio_file_time):
    """method to segmenting audio with given time stamps"""
    start_time = 0
    file_name = 1
    audio_path_list = []
    # segmenting audio file.
    for stime in time_stamp:
        time = float(stime)
        print(time)
        newAudio = AudioSegment.from_wav(main_clip)
        newAudio = newAudio[start_time * 1000:time * 1000]
        file_path = 'audio set/'+str(audio_file_time)+'sub'+str(file_name)+'.wav'
        newAudio.export(file_path, format="wav")
        start_time = time
        file_name += 1
        audio_path_list.append(file_path)
    return audio_path_list
