# ISC Pub Quiz
A script to generate ISC Pub Quizzes as an HTML presentation.
The quiz is defined using a YAML file, which is then passed to a Python script (use Python 3.11).
Using `pyyaml` and `jinja2`, an HTML file is generated. Optionally, `pytube` and `pydub` can be used to automate a part of the process of creating musical rounds.
The presentation uses [reveal.js](https://github.com/hakimel/reveal.js) for interactivity.

## TODO:
* make it possible to make the text or image larger
  * could be implemented by some dragable divider between the text and image columns, [like here](https://stackoverflow.com/questions/55565001/how-do-you-allow-a-user-to-manually-resize-a-div-element-vertically)
* save the images locally so that internet is not needed
  * this might need some YAML caching to detect changes in the definition
* improve layouts & make it look better in general
* auto search & download illustration image (with a potential override, of course)
* come up with a better way to embed the results (iframes are annoying and Google doesn't offer any customization)

## Quiz definition
The quiz is defined using a `.yaml` file which begins by a short header that defines the quiz metadata:
```yaml
date: 10/10/2022
place: ISC Point
template: presentation.j2
output: output.html
topics_per_block: 2
countdown_duration_minutes: How long will the countdown last?
additional_rules: # will be included in the 'Game Rules' page
  - To get bonus points, do a headstand!
  - Every beer drunk counts as 1/π points.
results:
  url: link to Google Sheets
```
Most of it should be self-explanatory except for the following:

The quiz will have a block of `topics_per_block` topics (e.g. 2), then a there will be a slide with a timer with `countdown_duration_minutes` to allow the teams to finish up. Once the time is up, it will change to a break slide, so that the organizers have time to "grade" the quizzes. The correct answer will be included after the break.

If the `results.url` field is not empty, results will be shown before the next round of questions. To find the URL of a Google Sheets table with the results, click (File > Share > Publish to web).

### Topics & Questions
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
Currently, four question types are defined:
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
To configure a musical question, you can either supply a file yourself:
```yaml
type: musical
text: Question text that will be shown.
answer: The correct answer.
audio_file: assets/music/audio_file.mp3
answer_audio_file: path to another file; if missing, `audio_file` will be used
question_img_src: Image to be shown alongside the question.
answer_img_src: Image to be shown alongside the question. If not provided, the question image will be shown.
```
or you can supply a YouTube link and start/end time and the audio will be downloaded *automagically*. Note that you will need [ffmpeg](https://ffmpeg.org/download.html) installed on your local machine for this.
```yaml
type: musical
text: Question text that will be shown.
answer: The correct answer.
question_img_src: Image to be shown alongside the question.
answer_img_src: Image to be shown alongside the question. If not provided, the question image will be shown.
youtube: 
  url: https://www.youtube.com/watch?v=rFMgixWg9-U
  start_time: 29 # [s]
  end_time: 50 # [s]
```

In the sort question, note that the order must be correct in both the `choices` and the `answers` field. This is to allow you to include additional info in the answer.
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
