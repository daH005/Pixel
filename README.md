About project
-------------

`Pixel` is 2D platformer. We play as a red-haired boy and complete the levels!:)
I use pygame.

How to run
----------

1. Pull
2. Provide the virtualenv
3. Run `pip install -r requirements.txt` from root directory
4. Run `python3 main.py` from `game` directory (don't forgot about `PYTHONPATH` - add path over `game` and `editor` directories)
- Also you can to run `python3 editor/main.py`
- For levels reset run `python3 editor/reset_all.py`

For exe building (10.01.2023 - only Windows)
--------------------------------------------

1. Run `pip install pyinstaller`
2. Run `building/exe/game/make.bat`
3. Run `building/exe/editor/make.bat`
