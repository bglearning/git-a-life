from src.alife.diary import Diary


def test_diary_from_text():
    preamble = "Life of Pi\n\n"
    main_text = "A Tiger and a Boy"
    combined_text = preamble + Diary.PREAMBLE_END_MARKER + main_text

    diary = Diary.from_text(combined_text)
    assert diary.preamble_text == preamble
    assert diary.main_text == main_text
