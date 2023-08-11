import TypingTester

if __name__ == '__main__':
    data = TypingTester.fetch_data()[0]
    TypingTester.typing_tester(data.get('word'))
    print('\n')
    print('Definition: ', data.get('definition'))
    print('Pronunciation: ', data.get('pronunciation'))
