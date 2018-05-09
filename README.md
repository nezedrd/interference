# The project

Explaining blog posts:
* [Project description][blog1]
* [Math][blog2]
* [First rendering][blog3]

[blog1]: https://nezedrd.github.io/python/interference/2018/04/20/interference-project.html
[blog2]: https://nezedrd.github.io/python/interference/2018/04/27/interference-math.html
[blog3]: https://nezedrd.github.io/python/interference/2018/05/01/interference-rendering.html

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
