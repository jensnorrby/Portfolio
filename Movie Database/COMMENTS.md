

# Comments

- Submission: P1_jensnorr
- Final score: 27/30
- Date: 2024-10-04 07:02:01

## General comments
Your code does unfortunately not work on my computer, since the path was overwritten on line 188. It should work without changing the path.

Great to see docstrings and comments in the code. Remember to clean up `pass` statements.

## E1 : Read csv file
Impressive use of the `csv.reader` function. Starting by extracting the headings and then zipping them with the rest of the row.
The code could be simplified by using `csv.DictReader` instead of `csv.reader`, since it would extract the list of dictionaries directly.

## E2 : Enrich data
In `add_actor`, great use of `itemgetter` to get the `crew` value, and `split` to get the list of actors.
Also, great use of `[::2]` to get every other element from the `crew_split` list to extract the actors. Same goes in `add_year`, good use of `itemgetter` and `split`.

## E3 : Filter implementation
Clever to loop over the movies once, and set the requirements as False if not met. However, to simplify, you should rather `continue` to the next movie if the requirement is not met, so you do not check other filters if the first ones were not met. Good use of `set` to filter the movies. However the entire function is hard to read.

Could be simplified using list comprehensions and the `any` and `all` functions, e.g.:
```python
    # Filter by actors
    if actors:
        movies = [movie for movie in movies if all(actor in movie["actors"] for actor in actors)]
    
    # Filter by genres
    if genres:
        movies = [movie for movie in movies if any(genre.strip() in movie["genre"].split(',') for genre in genres)]
```

## E4 : Sorting implementation
Nice and clean implementation using `sort`. Clever use of `sort_by` directly together with `reverse = not ascending`.

## E5 : Print movies
Good use of `itemgetter` to pull the values from the corresponding keys. Good use of `f-string` formatting plus fillers to print the values. Very short and readable. The header could potentially be done using `f-strings` for even better readability.

## E6 : Handle arguments
Good use of `argparse`. Remember to add `help` to the arguments. Correct use of `nargs` and `type` parameters.
