import convertingAudioContentToText
import convertVideoToAudio
import inputExtraction


def main():
    inputs = [143, 696, 1018, 1306, 1496, 2073, 2778, 3443, 4035, 4265, 5447, 5676]
    main_clip = 'data-sets/common sentence level problem.mp4'
    main_audio_transcript = 'data-sets/common sentence level problem.txt'
    time_list = inputExtraction.getting_time_stamp_list(inputs)
    print(time_list)
    audio_list = convertVideoToAudio.audio_segmentation(time_list, main_clip)
    print(audio_list)
    time_align_contents = convertingAudioContentToText.audio_transcript_segmentation(audio_list, main_audio_transcript)
    print(time_align_contents)


if __name__ == "__main__":
        main()
