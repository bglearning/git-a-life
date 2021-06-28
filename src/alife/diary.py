import datetime
from typing import Type, TypeVar

# Based on https://stackoverflow.com/a/39205612
_T = TypeVar("_T", bound="Diary")


class Diary:

    PREAMBLE_END_MARKER = "-------\n\n"

    def __init__(self, name: str = None, preamble: str = None, main_text: str = None):
        if name is None and preamble is None:
            raise ValueError("Both name and preamble can't be None")

        self.name = name
        self.preamble = preamble
        self.main_text = main_text

    def prepend_entry(self, entry_text: str) -> None:
        if self.main_text is not None:
            self.main_text = entry_text + self.main_text
        else:
            self.main_text = entry_text

    @property
    def preamble_text(self):
        if self.preamble is not None:
            return self.preamble
        return f"# {self.name}'s Life\n\n{Diary.PREAMBLE_END_MARKER}"

    @property
    def full_text(self):
        return self.preamble + Diary.PREAMBLE_END_MARKER + self.main_text

    @classmethod
    def from_text(cls: Type[_T], diary_text: str) -> _T:
        preamble_marker_splits = diary_text.split(Diary.PREAMBLE_END_MARKER)
        preamble_text = preamble_marker_splits[0]
        main_text = preamble_marker_splits[1]
        return cls(preamble=preamble_text, main_text=main_text)


class LifeEntry:
    def __init__(self, date: datetime.date, summary: str, description: str = None):
        self.date = date
        self.summary = summary
        description = "" if description is None else description
        self.description = description

    def __str__(self):
        return f"## {self.date.strftime('%Y-%m-%d')}\n{self.summary}\n{self.description}\n\n"
