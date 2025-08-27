from src.stream_processing.service import StreamService


def main():
    stream = StreamService()
    stream.process()


if __name__ == "__main__":
    main()
