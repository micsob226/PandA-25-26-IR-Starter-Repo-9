# Part 9 — Starter

This part builds on your Part 8 solution. The key goal is to restructure the code. We move code from ``app.py`` and ``models.py``
to a new module, ``file_utilities.py``. See ToDos for details.

Also, be introduce a new setting, ``:hl-mode``, which lets the user choose between two differnt ways of highlight the search results.

## Run the app

```bash
python -m part9.app
```

## What to implement (ToDos)

Your todos are located in `part9/app.py` and `part9/models.py`

0. **Copy/Redo** your implementation from part 8.
   1. Move ``combine_results`` to ``SearchResult`` and rename it to ``combine_with``. Adapt all calls accordingly.
   2. Move printing of one ``SearchResult`` to a method ``print`` in class ``SearchResult``. Move ``ansi_highlight`` along with it.
   3. Move ``search_sonnet`` to ``Sonnet`` and rename it to ``search_for``. Move ``find_spans`` also to make this work.
1. You realize that ``models.py`` is starting to get too big. You decide to move all functionality that has to do with files to a 
new module, ``file_utilities.py``. In this module you gather the ``Configuration`` class and the following functions from ``app.py``: 
``load_config``, ``save_config``, ``fetch_sonnets_from_api``, and ``load_sonnets``. You need to move other things in your code to 
make this work. For example, it makes sense, that the constants ``POETRYDB_URL`` and ``CACHE_FILENAME`` also are in this module.
In addition, you need to move ``module_relative_path``, because the file operations need it. Some of the imports will also be 
necessary in the new module.
2. You are not happy with the way, in which search results are shown. You would like the user to have the choice between using
_yellow background, black text_, which is the current implementation, but you also want a second choice, _bold light green text_.
You inspect the code and find that this can be accomplished by replacing the control string ``"\033[43m\033[30m"`` in the static
method ``ansi_highlight`` with another control string: ``"\033[1;92m"``. 

    You want the user to be able to switch between those two highlight modes using a new command, ``:hl-mode`` with either the 
value ``DEFAULT`` (which is the yellow background variant) or ``GREEN`` (the new one). Add this new configuration to the app, 
save the current value to the ``config.json`` file, so that users can permanently change their highlighting mode.


