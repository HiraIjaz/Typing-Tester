import TypingTester

if __name__ == "__main__":
    data = TypingTester.fetch_data()[0]
    TypingTester.typing_tester(data['word'])
    print('\n')
    print("Definition: ", data['definition'])
    print("Pronunciation: ", data['pronunciation'])
