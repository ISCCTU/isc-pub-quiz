import logging
import random
import string
from abc import ABC
from dataclasses import astuple, dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Mapping, Self, Tuple
from urllib.parse import urlparse
from urllib.request import url2pathname

import pytube
import requests
from pydub import AudioSegment
from pytube import YouTube
from pytube.query import StreamQuery


def asset_folder_path() -> Path:
    return Path(__file__).parent / "assets"


class Question(ABC):
    def __init__(
        self,
        text: str,
        question_img_src: str | None,
        answer_img_src: str | None,
    ):
        self.text = text
        self.question_img_src = self.cache_image(question_img_src)
        if answer_img_src is None:
            self.answer_img_src = self.question_img_src
        else:
            self.answer_img_src = self.cache_image(answer_img_src)

    def cache_image(self, img_src: str | None) -> str:
        # if the image is an URL, tries to download it
        # returns the path to be included in the website
        if img_src is None:
            return None
        if (Path(__file__).parent / img_src).is_file():
            logging.debug(f"File {img_src} already exists!")
            return img_src
        url = urlparse(img_src)
        filename = url2pathname(url.path.replace(":", "")).split("\\")[-1]
        prefix = f"images/cache/{url.netloc}/"
        folder_char_l = len(str(asset_folder_path())) + len(prefix)
        if folder_char_l + len(filename) > 255:
            # Windows only supports paths of max length 255 -> shorten filename
            characters_left = 255 - folder_char_l
            filename = filename[-characters_left:]
        suffix = f"images/cache/{url.netloc}/{filename}"

        filepath = asset_folder_path() / suffix
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if filepath.is_file():
            logging.debug(f"File {img_src} already exists!")
            return "assets/" + suffix
        try:
            # wikimedia sometimes refuses to return the image without a user-agent...
            headers = {"User-Agent": "ISC Pub Quiz Caching"}
            img_data = requests.get(img_src, stream=True, headers=headers).content
        except requests.ConnectionError as e:
            logging.info(f"Connection error ({e}) for image {img_src}")
            return img_src
        except requests.exceptions.MissingSchema as e:
            logging.info(f"Invalid URL for image {img_src} ({e})")
            return img_src
        with filepath.open("wb") as f:
            f.write(img_data)

        return "assets/" + suffix


@dataclass
class CommonQData:
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

    def __init__(
        self,
        common_data: CommonQData,
        answer: str,
        audio_file: str,
        answer_audio_file: str | None = None,
    ):
        super().__init__(*common_data)
        self.answer = answer
        self.audio_file = audio_file
        self.answer_audio_file = answer_audio_file

    @classmethod
    def from_youtube(
        cls,
        common_data: CommonQData,
        answer: str,
        url: str,
        start_time: int,
        end_time: int,
    ) -> Self:
        video = YouTube(url)
        video_id = pytube.extract.video_id(url)
        relative_filename = f"music/youtube/{video_id}.mp3"
        filename = asset_folder_path() / relative_filename
        filename.parent.mkdir(parents=True, exist_ok=True)
        if filename.is_file():
            logging.debug("Already downloaded video", video_id)
            return cls(common_data, answer, "assets/" + relative_filename)
        else:
            logging.info("Downloading video", video_id)
        if not (0 <= start_time <= video.length):
            raise ValueError(
                f"Invalid choice of start/end of YouTube audio in {common_data.title}"
            )
        try:
            audio_stream = StreamQuery(video.streams).get_audio_only(subtype="mp4")
        except pytube.exceptions.AgeRestrictedError as e:
            raise ValueError(
                f"Video {url} for question '{common_data.text}' is age restricted and cannot be automatically downloaded. You will need to download it manually..."
            )
        audio_buffer = BytesIO()
        audio_stream.stream_to_buffer(audio_buffer)
        # get to the start of the buffer to feed it to pydub
        audio_buffer.seek(0)
        # NOTE: ffmpeg needed for this
        audio = AudioSegment.from_file(
            audio_buffer,
            format="mp4",
        )
        # trim audio and add fade-in/-out
        trimmed_audio = audio[start_time * 1000 : end_time * 1000]
        fade_l = 1000 * min(2, 0.1 * (end_time - start_time))
        trimmed_audio = trimmed_audio.fade_in(fade_l).fade_out(fade_l)
        trimmed_audio.export(filename, format="mp3")
        return cls(common_data, answer, "assets/" + relative_filename)
