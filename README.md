# Music-Xmas-Project

When I first started attempting to create user interfaces using Python that required a library. I often had an issue with finding a suitable library for .wav files so i designed my 
own. 

Needed libraries for this project:
-Playsound (v1.2.2 is the only stable build for this)

How to use:
-Create a finder class.
-If all the audio files you need are in the same directory as the script , just run the find method.
-If not use the set_working_dir method, you can entered it in the following format:
    "C:/.../...."
-If you need to check the directory the script is in print the class.
-Make sure you assign a variable when running the find method.

-Running the finder.find method will return a queue class.
-To view the list of files, print this class.
-If you want to delete any items, you can use the delete function, passs the index as the parameter.
-If you need to find the index of any items, use the search function to search through the list, this will generate a list of matching items.

-Once this is complete, use the load method, which will put the items into a player class so you can play these back.
-The load parameter contain a boolean value for shuffle and a list if you want to play any track multiple times.
-.play() will just then play everything according to how the queue was set up.
-Can use forward and skip method with an optional parameter which indicates how many tracks to change by (defaults to 0).
-Can use print function with this class to find out current position in the queue.
