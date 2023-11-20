# ISC Pub Quiz
A script to generate ISC Pub Quizzes as an HTML presentation.
The quiz is defined using a YAML file, which is then passed to a Python script.
Using `pyyaml` and `jinja2`, an HTML file is generated.
The presentation uses [reveal.js](https://github.com/hakimel/reveal.js) for interactivity.
As of right now, the asset folder is necessary to show the presentation properly.

## TODO:
* make it possible to make the text or image larger
  * could be implemented by some dragable divider between the text and image columns, [like here](https://stackoverflow.com/questions/55565001/how-do-you-allow-a-user-to-manually-resize-a-div-element-vertically)
* save the images locally so that internet is not needed
  * this might need some YAML caching to detect changes in the definition
* improve layouts & make it look better in general
* auto search & download illustration image (with a potential override, of course)

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
Currently, three question types are defined:
* Simple: A basic question-answer pair.
* Choice: A question with a list of answers - a), b), etc. The wrong answers will be shuffled and the correct one will be placed at a random spot among them.
* Musical: A question where the player must identify the music played
* Sort: The order will be shuffled and players must find the correct order. It's possible to include additional info in the answer. 
```yaml
type: simple
text: Question text that will be shown.
answer: The correct answer.
question_img_src: Image to be shown alongside the question.
answer_img_src: Image to be shown alongside the question. If not provided, the question image will be shown.
```
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
question_img_src: Image to be shown alongside the question.
answer_img_src: Image to be shown alongside the question. If not provided, the question image will be shown.

```
```yaml
type: musical
text: Question text that will be shown.
answer: The correct answer.
wrong:
question_img_src: Image to be shown alongside the question.
answer_img_src: Image to be shown alongside the question. If not provided, the question image will be shown.

```
In the sort question, note that the order must be correct in both the `choices` and the `answers` field. 
```yaml
type: sort
text: Question text that will be shown.
choices: 
  - 1
  - 2
  - 3
answers:
  - 1 (lowest natural number)
  - 2 (twice the number as 1)
  - 3 (sum of the previous)
question_img_src: Image to be shown alongside the question.
answer_img_src: Image to be shown alongside the question. If not provided, the question image will be shown.

```

There's also a short header that defines the quiz metadata:
```yaml
date: 10/10/2022
place: ISC Point
template: presentation.j2
output: output.html
countdown_duration_minutes: How long will the countdown last?
results_url: URL of the results table
topics_per_block: 2
```
Most of it should be self-explanatory, except the last two.

The `results_url` can be a Google Sheets url (File > Share > Publish to web) that will be included before the next round of questions.

The quiz will have a block of `topics_per_block` topics (e.g. 2), then a break will be inserted, so that the organizers have time to "grade" the quizzes. Afterwards, the correct answers are shown, followed by another set of topics.
