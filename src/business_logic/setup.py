def install_nltk_data() -> None:
    import nltk
    nltk.download('punkt')


if __name__ == "__main__":
    install_nltk_data()
    # ToDo: move init corpus into this file
