import convertingAudioContentToText
import convertVideoToAudio
import inputExtraction
from multiprocessing import Process
import maninTopicIdentification
import checkRepetetion


def main():
    inputs = [143, 696, 1018, 1306, 1496, 2073, 2778, 3443, 4035, 4265, 5447, 5676]
    main_clip = 'data-sets/common sentence level problem.mp4'
    main_audio_transcript = 'data-sets/common sentence level problem.txt'
    # p1 = Process(target=func1)
    # p1.start()
    # p2 = Process(target=func2)
    # p2.start()
    # p1.join()
    # p2.join()
    time_list = inputExtraction.getting_time_stamp_list(inputs)
    print(time_list)
    audio_list = convertVideoToAudio.audio_segmentation(time_list, main_clip)
    print(audio_list)
    time_align_contents = convertingAudioContentToText.audio_transcript_segmentation(audio_list, main_audio_transcript)
    print(time_align_contents)
    video_main_topic = inputExtraction.get_the_main_topic(inputs)
    print(video_main_topic)
    transcipt_main_topic = maninTopicIdentification.main_topic_identification(main_audio_transcript)
    print(transcipt_main_topic)
    main_topic = maninTopicIdentification.compare_two_main_topics(video_main_topic, transcipt_main_topic)
    print(main_topic)


if __name__ == "__main__":
        main()
