# ISC Pub Quiz
A script to generate ISC Pub Quizzes as an HTML presentation.
The quiz is defined using a YAML file, which is then passed to a Python script.
Using `pyyaml` and `jinja2`, an HTML file is generated.
The presentation uses [reveal.js](https://github.com/hakimel/reveal.js) for interactivity.
As of right now, the asset folder is necessary to show the presentation properly.

## TODO:
* improve layouts & make it look better in general
* support audio questions
* possibly support a "sorting" question (although that can technically be done using the simple question type)
* create the rules slide
* create the end slide

## Quiz definition
The quiz is defined using a `.yaml` file.
The list of topics for the pub quiz is defined simply by
```yaml
topics:
  - name: topic A
    questions: ???
  - name: topic B
    questions: ???
  ...
```
The `questions` entry is again a list of questions.
Currently, two question types are defined:
* Simple: A basic question-answer pair.
* Choice: A question with a list of answers - a), b), etc. The wrong answers will be shuffled and the correct one will be placed at a random spot among them.
```yaml
type: simple
text: Question text that will be shown.
answer: The correct answer.
img_src: Image to be shown alongside the question.
```
and
```yaml
type: choice
text: Question text that will be shown.
answer: The correct answer.
wrong:
  - A
  - list
  - of
  - wrong
  - answers.
img_src: Image to be shown alongside the question.
```


There's also a short header that defines the quiz metadata:
```yaml
date: 10/10/2022
place: ISC Point
template: presentation.j2
output: output.html
topics_per_block: 2
```
Most of it should be self-explanatory, except the last one.
The quiz will have a block of `topics_per_block` topics (e.g. 2), then a break will be inserted, so that the organizers have time to "grade" the quizzes. Afterwards, the correct answers are shown, followed by another set of topics.
