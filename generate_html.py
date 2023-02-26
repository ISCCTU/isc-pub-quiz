from jinja2 import Environment, FileSystemLoader
from typing import Optional, List

import random
import yaml

config = "example.yaml"
with open(config, 'r', encoding='utf8') as fp:
    quiz_config = yaml.safe_load(fp)

template=Environment(loader=FileSystemLoader("./slides")).get_template(quiz_config["template"])

def shuffle_choices(answer,wrong):
    # generate a random order and remember the correct answer
    num_options = len(wrong) + 1  # +1 for answer
    correct_idx = random.randint(0, num_options - 1)
    random.shuffle(wrong)
    wrong.insert(correct_idx, answer)
    choices=wrong
    return choices,correct_idx


def parse_question(topic,question,question_idx):
    question["title"]=f"{topic['name']}: Q{question_idx+1}"
    if question["type"]=="simple":
        pass
    elif question["type"]=="choice":
        choices,correct_idx=shuffle_choices(question["answer"],question["wrong"])
        question["choices"]=choices
        question["correct_idx"]=correct_idx
    return question

quiz={
    "date": quiz_config["date"],
    "place": quiz_config["place"],
    "blocks": [],
}
for t,topic in enumerate(quiz_config["topics"]):
    if t%quiz_config["topics_per_block"]==0:
        quiz["blocks"].append([])
    parsed_questions=[]
    for q,question in enumerate(topic["questions"]):
        parsed_questions.append(parse_question(topic,question,q))
    topic["questions"]=parsed_questions
    quiz["blocks"][-1].append(topic)


# quiz["blocks"]=[[quiz["topics"][i+j*quiz["topics_per_block"]] for i in range(quiz["topics_per_block"])] for j in range(len(quiz["topics"])//quiz["topics_per_block"])]
print(quiz)
content=template.render(quiz)

with open("output.html", "w",encoding="utf-8") as fh:
    fh.write(content)