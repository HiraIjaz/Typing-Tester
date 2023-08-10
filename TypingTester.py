import json
from getch import getch
import requests
import time
from dotenv import load_dotenv
import os

URL = "https://random-words-with-pronunciation.p.rapidapi.com/word"

HEADERS = {
    "X-RapidAPI-Host": "random-words-with-pronunciation.p.rapidapi.com"
}

load_dotenv()
API_KEY = os.getenv("RAPID_API_KEY")
HEADERS["X-RapidAPI-Key"] = API_KEY


def fetch_data():
    """
    Fetches random word data from the API.

    Returns:
        dict: Random word data.
    """

    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print("error fetching data", e)
    else:
        return json.loads(response.text)


def count_mismatches(str1, str2):
    """
    Counts the number of character mismatches between two strings.

    Args:
        str1 (str): First string.
        str2 (str): Second string.

    Returns:
        int: Number of character mismatches.
    """
    min_length = min(len(str1), len(str2))
    mismatch_count = 0

    for char1, char2 in zip(str1, str2):
        if char1 != char2:
            mismatch_count += 1

    mismatch_count += abs(len(str1) - len(str2))

    return mismatch_count


def calc_accuracy_score(typed_word, test_word, backspace_count):
    """
    Calculates the accuracy score for the typed word.

    Args:
        typed_word (str): The word typed by the user.
        test_word (str): The reference test word.
        backspace_count (int): Number of backspaces used.

    Returns:
        float: Accuracy score.
    """
    per_letter_score = float(100 / len(test_word))
    bs_penalty = float(backspace_count * per_letter_score)
    mismatch_count = count_mismatches(test_word, typed_word)
    mismatch_penalty = float(mismatch_count * per_letter_score)

    return round(float(abs(100 - bs_penalty - mismatch_penalty)), 2)


def calc_time_score(start_time, end_time, typed_word):
    """
    Calculates the time score for the typing test.

    Args:
        start_time (float): Start time of typing.
        end_time (float): End time of typing.
        typed_word (str): The word typed by the user.

    Returns:
        float: Time score.
    """
    avg_one_keystroke_time = 0.28
    avg_transition_time = 0.4
    final_score = 0
    elapsed_time = end_time - start_time
    raw_score = float(elapsed_time / (avg_transition_time + (avg_one_keystroke_time * (len(typed_word) + 1))))

    if raw_score < 1:
        final_score = 100
    elif raw_score > 1:
        final_score = max(float(100 / raw_score), 0)

    return round(final_score, 2)


def typing_tester(test_word):
    """
    Conducts a typing test for the given word.

    Args:
        test_word (str): The word to be typed by the user.
    """
    backspace_count = 0

    enter_key = 10
    backspace_key = 127

    word = ''
    stop = False

    print(f'Type {test_word} and press Enter')

    accuracy_score = 0
    time_score = 0
    end_time = 0
    start_time = time.time()

    while not stop:
        key = ord(getch())
        if key == enter_key:  # enter is pressed
            end_time = time.time()
            accuracy_score = calc_accuracy_score(word, test_word, backspace_count)
            time_score = calc_time_score(start_time, end_time, word)
            stop = True
        elif key == backspace_key:  # backspace
            backspace_count += 1
            word = word[: -1]
        else:
            word += chr(key)

    total_score = round(accuracy_score * 0.5 + time_score * 0.5, 2)

    print(f'Word: {test_word}')
    print(f'No. of letters: {len(test_word)}')
    print('\n')
    print('User typed: ', word)
    print(f'Time taken by user: {round(end_time - start_time, 2)}s')
    print('\n')
    print(f'AccuracyScore: {accuracy_score}')
    print(f'Time Score: {time_score}s')
    print('\n')
    print('Total Score: ', total_score)
