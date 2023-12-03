import sys
from dataclasses import astuple, dataclass
from typing import Any, Dict, List, Mapping, Optional, Tuple

import yaml
from jinja2 import Environment, FileSystemLoader

from questions import ChoiceQ, CommonQData, MusicQ, SimpleQ, SortQ


def parse_question(
    topic: Dict[str, Any], question: Dict[str, Any], question_idx: int
) -> Dict[str, Any]:
    common_data = CommonQData(
        question["text"],
        question.get("question_img_src"),
        question.get("answer_img_src"),
    )
    # this could possibly be refactored by searching for the class with correct ype but that might relate the yaml and class a bit too much...
    if question["type"] == SimpleQ.type:
        return SimpleQ(common_data, question["answer"])
    elif question["type"] == ChoiceQ.type:
        return ChoiceQ(common_data, question["answer"], question["wrong"])
    elif question["type"] == SortQ.type:
        return SortQ(common_data, question["choices"], question["answers"])
    elif question["type"] == MusicQ.type:
        answer = question["answer"]
        audio_file = question.get("audio_file")
        # TODO: add possible answer audio from YouTube
        if audio_file is not None:
            answer_audio_file = question.get("answer_audio_file")
            return MusicQ(common_data, answer, audio_file, answer_audio_file)
        else:
            youtube_cfg = question["youtube"]
            return MusicQ.from_youtube(
                common_data,
                answer,
                youtube_cfg["url"],
                youtube_cfg["start_time"],
                youtube_cfg["end_time"],
            )
    else:
        raise NotImplementedError("Unknown question type:", question["type"])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        config = sys.argv[1]
    else:
        # TODO: this should take the latest yaml...
        config = "pub_quizzes/2023-11-20.yaml"

    with open(config, "r", encoding="utf8") as fp:
        quiz_config = yaml.safe_load(fp)

    # parse the quiz for templating
    quiz = {
        "date": quiz_config["date"],
        "place": quiz_config["place"],
        "results": quiz_config.get("results"),
        "blocks": [],
        "countdown_duration_minutes": quiz_config["countdown_duration_minutes"],
    }
    for t, topic in enumerate(quiz_config["topics"]):
        if t % quiz_config["topics_per_block"] == 0:
            quiz["blocks"].append([])
        topic["questions"] = [
            parse_question(topic, q, i) for i, q in enumerate(topic["questions"])
        ]
        quiz["blocks"][-1].append(topic)

    # generate the web page from the template
    template = Environment(loader=FileSystemLoader("./slides")).get_template(
        quiz_config["template"]
    )
    content = template.render(quiz)

    with open(quiz_config["output"], "w", encoding="utf-8") as fh:
        fh.write(content)
