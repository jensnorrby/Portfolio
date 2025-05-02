import os.path as path
import csv
import argparse
import sys
from operator import itemgetter, attrgetter
SCORE_TTL = "Score"
YEAR_TTL = "Year"
TITLE_TTL = "Title"
ACTORS_TTL = "Actors"


def read(filepath: str) -> list[dict]:
    def read(filepath: str) -> list[dict]:
        """Takes filepath as input and returns a list of dictionaries, where each item represents a movie.
        
        Args:
            filepath (str): path to csv file
        
        Returns:
            list_of_dicts (list[dict]): list of dictionaries representing movies
        """
    #I begin with opening the file as a csv file
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        #I create to empty lists for later use. The first is the list of dictionaries that will be returned by the read() and the second i the list of headings that will be used to create the dictionaries.
        list_of_dicts = []
        headings = []
    
        
        for row in csvreader:
            #First, we need to assign the values of the first row in csvreader as the values of the headings. The if statement is only meant to prevent subsequent iterations to take this action.
            if len(headings) < 3:
                headings.extend(row)
            #When the values of the first row are assigned to headings (which now has a len() >3), the subsequent rows are zipped to that list as a dictionary and then appended as an additional item to the list_of_dicts.
            else:
                movie_dict = dict(zip(headings, row))
                list_of_dicts.append(movie_dict)
    
        return list_of_dicts
    pass

# the enrich_data function simply applies the add_actors and add_year functions to the list.
def enrich_data(movies: list[dict]) -> list[dict]:
    semi_enriched_movies = add_actor(movies)
    enriched_movies = add_year(semi_enriched_movies)
    return enriched_movies   
    pass

#To print the movies nicely, I use itemgetter to pull the values from the corresponding keys. The length of the first
#two categories are set for esthetic reasons. Only but a few titles are longer than 55s and then the 49s are set for 
#actors just to fill out the line without causing a line break.
def print_movies(data: list[dict]):
    print("""
--------------------------------------------------------------------------------------------------------------------------
Score  Year     Title                                                   Actors
--------------------------------------------------------------------------------------------------------------------------
          """)
    for movie in data:         
        print(f"{itemgetter("score")(movie):<7s}{itemgetter("year")(movie):<8d} {itemgetter("names")(movie):.<55s} {itemgetter("actors")(movie):.49s}")
    print("---------------------------------------------------------------------------------------------------------------------------")
    print("The len is", len(data))
    pass


def add_year(movies: list[dict]) -> list[dict]:
    """Takes a list of dictionaries and adds the key_value "year" with information from "date_x"

    Args:
        movies (list[dict]): A list of dictionaries, including the key "date_x" as the second key listed.

    Returns:
        movies (list[dict]): A list of movie information including "date_x" and the subcategory year (int).
    """
    #For every movie in the list, the itemgetter pulls the value corresponding to date and splits it into a list of
    # "dd", "mo", "year".    
    for movie in movies:
        time_entities = (itemgetter("date_x")(movie)).split("/")
     #From that list, the year element is stored as an int.       
        movie_year = int(time_entities[2])
        #The year value (int) is then added to the dictionary, which is part of the list that is returned at the end.
        movie["year"] = movie_year
    return movies
    pass


def add_actor(movies: list[dict]) -> list[dict]:
    """Takes a list of dictionaries and adds the key_value "actors" with information from "crew"

    Args:
        movies (list[dict]): A list of dictionaries, including the key_value "crew".

    Returns:
        movies (list[dict]): A list of movie information including "crew" and the subcategory "actors", where the names of the characters are removed.
    """
    #The function pulls the value corresponding to the key "crew" and splits it into a list.
    for movie in movies:
        crew_list = (itemgetter("crew")(movie)).split(",")
        #The actor_list then pulls every other element, ignoring the character names.
        actor_list = crew_list[::2]
      
        #The actor list is converted to a string and then added as a tuple to the end of the movie dictionary.
        movie_actors = ", ".join(actor_list)
        movie["actors"] = movie_actors
    return movies
    pass


def get_filtered_movies(
    movies: list[dict],
    actors: list[str] = None,
    genres: list[str] = None,
    years: list[int] = None,
    top: int = 0,
    sort_by: str = None,
    ascending: bool = False,
) -> list[dict]:
    """Takes in the data list and filters the movies based on the
    given parameters

    Args:
        movies (list[dict]): List of all the movies
        actors (list[str]): List of Actors that needs to be in the movies
        genres (list[str]): List of Genres to include in the filter
        years (list[int]): List of years movies were released in
        top (int): How many movies to return
        sort_by (str): What key to sort by, default 'score'
        asc (bool): Sort ascending (e.g. the lowest score is returned first)

    Returns:
        list[dict]: The filtered list of movies
    """
    #We add an empty list that will serve as the list returned by the function in the end.
    filtered_movies = []
    
    for movie in movies:
        #We begin with setting the three requirements as true, and then testing each of them in case a value is given.
        actor_requirement = True
        genre_requirement = True
        year_requirement = True
        
        if actors != None:
            #Since we are not pulling anything from the values in the filtering function, it is stored as a string.
            movie_actors = itemgetter("actors")(movie)
            #The listed actors in the given argument are then identified in the value string. If any of them is not
            #found, the whole requirement fails.
            for actor in actors:
                if movie_actors.find(actor) == -1:
                    actor_requirement = False
                    
                   
        if genres != None:
            #Since the genres requirement only needs a match, we cannot check its items individually. The value
            #corresponding to the "genre" key is split into a list and then stored as a set together with the argument.
            movie_genres = (itemgetter("genre")(movie)).split(",")
            genres_set = set(movie_genres)
            filtered_genres = set(genres)
           
           #The sets are then checked for intersection and only if no matching value is found, the requirement is set to false.
            if len(filtered_genres.intersection(genres_set)) < 1:
                genre_requirement = False

        #For the "year" requirement, the code is even simplier as any movie only carries a single "year" value.                    
        if years != None:
            movie_year = itemgetter("year")(movie)
            if movie_year not in years:
                year_requirement = False
                   
        #Then, if no requirement has been falsified, it is added to the list from the beginning.
        if actor_requirement == True and genre_requirement == True and year_requirement == True:
            filtered_movies.append(movie)
    
    #If a sort_by argument is given, the list is sorted by the corresponding values. Since reverse orders items
    #in a descending order, it is set to the negative of ascending.
    if sort_by != None:
        filtered_movies.sort(key=itemgetter(sort_by), reverse=not ascending)
    
    #The filtered_movies are returned, but if the "top" argument was given limited to that length.
    if top == 0:
        return filtered_movies
    else:
        return filtered_movies[:top]
    pass


def main():
    # path.join() is agnostic to operating system (Windows Vs Linux)
    data = read(path.join("data", "c:/users/xramje/bb1000/p1_jensnorr/data/imdb_movies.csv"))

    # -------------------------------------
    # Command line input parser
    # -------------------------------------
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--actors", nargs="+", action="extend")
    arg_parser.add_argument("--genres",nargs="+", action="extend")
    arg_parser.add_argument("--years", nargs="+", type=int, action="extend")
    arg_parser.add_argument("--top", type=int)
    arg_parser.add_argument("--sort", type=str)
    arg_parser.add_argument("--ascending", action="store_true")
    pass
    # -------------------------------------
    args = arg_parser.parse_args()
    # -------------------------------------

    # Add the additional fields to the raw data
    movies = enrich_data(data)

    # Run the filter function
    movies = get_filtered_movies(
        movies,
        args.actors,
        args.genres,
        args.years,
        args.top,
        args.sort,
        args.ascending,
    )
    # And finally print a nice table
    print_movies(movies)
    pass


if __name__ == "__main__":
    main()
