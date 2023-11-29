import random
import string
from abc import ABC
from dataclasses import astuple, dataclass
from typing import Any, Dict, List, Mapping, Optional, Tuple


class Question(ABC):
    def __init__(
        self,
        title: str,
        text: str,
        question_img_src: str | None,
        answer_img_src: str | None,
    ):
        self.title = title
        self.text = text
        self.question_img_src = question_img_src
        if answer_img_src is None:
            answer_img_src = self.question_img_src
        self.answer_img_src = answer_img_src


@dataclass
class CommonQData:
    title: str
    text: str
    question_img_src: str | None
    answer_img_src: str | None

    def __iter__(self):
        return iter(astuple(self))


class SimpleQ(Question):
    type: str = "simple"

    def __init__(self, common_data: CommonQData, answer: str):
        super().__init__(*common_data)
        self.answer = answer


class ChoiceQ(Question):
    type: str = "choice"

    def __init__(self, common_data: CommonQData, answer: str, wrong: List[str]):
        super().__init__(*common_data)
        self.choices, self.correct_idx = self.shuffle_choices(answer, wrong)

    @staticmethod
    def shuffle_choices(answer: str, wrong: List[str]) -> Tuple[List[str], int]:
        # generate a random order and remember the correct answer
        num_options = len(wrong) + 1  # +1 for answer
        correct_idx = random.randint(0, num_options - 1)
        random.shuffle(wrong)
        wrong.insert(correct_idx, answer)
        choices = wrong
        return choices, correct_idx


class SortQ(Question):
    type: str = "sort"

    def __init__(
        self, common_data: CommonQData, choices: List[str], answers: List[str]
    ):
        super().__init__(*common_data)
        self.choices, self.answers = self.shuffle_sort(choices, answers)

    @staticmethod
    def shuffle_sort(
        choices: List[str], answers: List[str]
    ) -> Tuple[List[str], List[str]]:
        # shuffle sorting question
        letters = list(string.ascii_uppercase[0 : len(choices)])
        random.shuffle(letters)
        answers = [f"{o}) {a}" for (o, a) in zip(letters, answers)]
        choices = sorted([f"{o}) {c}" for (o, c) in zip(letters, choices)])
        return choices, answers


class MusicQ(Question):
    type: str = "musical"

    def __init__(self, common_data: CommonQData, audio_file: str):
        super().__init__(*common_data)
        self.audio_file = audio_file
