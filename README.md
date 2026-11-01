# Electronics Study Notebook

A self-contained study notebook on electronics, sensors and robotics, written for a young beginner working with an adult guide.

## Using it

- **Offline:** open `index.html` in a browser. Everything works without installing anything. With no internet, the page uses fallback fonts.
- **Printing:** use the **Print this page** button. Practice-question answers print expanded.
- **Installing as an app:** this needs the folder to be served over `https` or `localhost`, for example with `python -m http.server` from this folder. Then choose Install in the browser.
- **Saved work:** Lab edits, the Build Log and reading progress stay in that one browser. Use **Copy my results** in the Build Log to keep a copy.

## Changing it

Edit the files in `source/`, then run:

```
python source/build.py
```

This rebuilds `index.html` and `sw.js` here, and writes `source/electronics-study-notebook.html`, the same notebook without the install and print additions. Don't edit `index.html` directly, because a rebuild replaces it.

To update the [live site](https://leojai23.github.io/electronics-notebook/), run these from this folder, then allow about a minute:

```
git add -A
git commit -m "Describe your change"
git push
```

| File | What it holds |
| --- | --- |
| `build.py` | Page layout, styles, navigation and the build |
| `intro.py` | The Introduction page |
| `content_a.py`, `content_b.py` | The 9 topics, quiz, assignments and case study |
| `figures.py` | Drawings for the 9 topics |
| `sensors.py`, `sensor_art.py` | The 22 sensors and their drawings |
| `robots.py` | The 25 robot exercises and their drawings |
| `lab_engine.js` | Arduino-code runner and circuit solver |
| `lab_examples.js` | The 28 Practical Lab examples and their checks |
| `lab_ui.js` | The Practical Lab bench |
| `robot_engine.js`, `robot_ui.js` | The robot simulator, its checks and the Build Log |
| `extras.py` | The sensor and robot quizzes, robot flashcards and the Fix It Guide |
| `search.js` | Notebook search |
| `blocks.js` | Block coding and the ready-made block programs |
| `unit2.py` | Unit II topics, drawings and quiz |
| `course.py`, `course.js` | The Arduino coding course and its runner |
| `handbook.py` | The guide's handbook, answer keys and shopping list |

The block editor is [Blockly](https://github.com/google/blockly) 10.4.3, under the Apache 2.0 licence. A copy is in `vendor/`.

## Testing

From `source/`, with Node installed:

```
node test_lab.js
python dump_robots.py && node test_robots.js && node test_robot_sim.js
python test_sensors.py && node test_sensors.js
```

These test the simulators and that all the sketches compile. They don't replace trying the circuits on real parts, so record real builds in the Build Log.
