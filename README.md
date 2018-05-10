# The project

Explaining blog posts:
* [Project description][blog1]
* [Math][blog2]
* [First rendering][blog3]
* [Video demonstration][blog4]

[blog1]: https://nezedrd.github.io/python/interference/2018/04/20/interference-project.html
[blog2]: https://nezedrd.github.io/python/interference/2018/04/27/interference-math.html
[blog3]: https://nezedrd.github.io/python/interference/2018/05/01/interference-rendering.html
[blog4]: https://nezedrd.github.io/python/interference/2018/05/10/interference-demo.html

# Workplace setup

With [virtualenv][ve] and [virtualenvwrapper][vew].

```sh
~ λ PROJECT_NAME="interference"
~ λ PROJECT_PATH="/home/nezedrd/$PROJECT_NAME"
~ λ mkvirtualenv -a "$PROJECT_PATH" -p python3 "$PROJECT_NAME"
(interference) ~/interference λ pip install -r requirements.txt
```

[ve]:  https://virtualenv.pypa.io/en/stable/installation/
[vew]: http://virtualenvwrapper.readthedocs.io/en/latest/install.html

# Running a demo

You can show the main help, first.

```sh
(interference) ~/interference λ python -m young -h
```

Then, as an example, run the `pyplot` demo. This is the interactive one.

```sh
(interference) ~/interference λ python -m young pyplot
```

The `beforeafter` demo saves two pics. One with the default parameters (before)
and one after changing them to what you specify.

```sh
(interference) ~/interference λ python -m young beforeafter -w 650 -y 15 -d 3
```

The `movie` demo saves a video. You can look in the `demos/movie.py` code if
you want to change.

```sh
(interference) ~/interference λ python -m young movie -q lld -o video.mp4
```
