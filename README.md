# Portfolio
My coding projects

The folders contains the best examples of my coding projects. Three of the projects (Movie, Graph, Stocks) were part of a python coding course at KTH (BB1000) and the last project (Geography) I have written as a tool for a short research project. As a result, all code is written by me and contains minimal instances of cut-and-paste. In all of these cases, it was crucial that I understood every piece of coding and how they fit together. Below you will find a short presentation of each project.

__KTH course projects__

-Movie Database-
The first examination was to create a imdb-style program that from a database of movie information allowed searching, sorting and filtering - presenting the results in a (somewhat) neat table. It was a great training in managing the various objects in Python and particularly dicts and their many functions.

-Graph Visualizer-
The second examination was a program that took a set of node data and visualized it in an approximation of the most pleasing graph. The 'data' folder contains a number of data sets that are named after the shape they are intended to produce when fed to the program. It was a great exercise in object-based coding and how to manage the interaction between several classes.

-Stocks-
The last examination was a program that read stocks data and analyzed it to produce assessments and predictions of the market. It continued the theme of object based coding but intensified the number of parameters treated within each class. While I made significant progress, I did get stuck at one juncture and as my schedule played out, I wasn't able to complete the assignment. In total, however, I did enough to pass the course and never found the time to return to it.

__Parliament Geography Research Project__

As part of a project funded by Åke Wibergs stiftelse, I have been studying the the places and locations mentioned in Swedish parliamentary discourse 1887-1914. I have set up two jupyter notebooks to implement a BERT model that The Royal Library has trained on Swedish data. 'Parliament NER analysis' takes the downloaded parliament records (vast number of .xml files) and uses Named Entity Recognition to pick out the locations. These are then grouped by year and stored in a dict that is written to a .txt file. The code also looks to manage these .txt files and present their most relevant information in a clear way. Having identified the most interesting locations mentioned, one can use the parliament debate digital database to identify the speeches in which the locations are refered and download them. The SA notebook will read these debates and sumarize the sentiment data for the relevant sentences by year. It is worth keeping in mind that none of these notebooks were intended for public consumtion and that my sole intention was to create the fastest and most straight-forward route to the relevant data, even if the execution could have been a lot neater.
