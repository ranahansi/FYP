import convertingAudioContentToText


def main():
    seperatedTextContents = convertingAudioContentToText.audioTranscriptSegmentation()
    print(seperatedTextContents)

if __name__ == "__main__":
        main()
