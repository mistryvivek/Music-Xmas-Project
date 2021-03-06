import os
from typing import Type
#Install v1.2.2 due to bug on other version.
#This has been tested on this library and works.
from playsound import playsound
import random

class EmptyPlaylistError(Exception):
    pass

#To focus on audio playback.
class player:
    def __init__(self, playlist, shuffle, repeat):
        """Sets up music ready for playback.

        Args:
            playlist (list): contains the tracks that will be played.
            shuffle (boolean): whether shuffle has been enabled.
            repeat (list): each index corrosponds to whether each song
               needs to be repeated.

        Raises:
            TypeError: Playlist has to be a list.
            EmptyPlaylistError: Playlist must contain at least one 
               object.
            TypeError: Shuffle must have a boolean value.
            TypeError: Repeat must be a list.
            IndexError: Each index in repeat must corrospond to a 
               index in the playlist.
        """
        #Verification of the playlist entered as a parameter.
        #Need to contain something to prevent playback errors
        #which could be caused by this.
        if isinstance(playlist, list) == False:
            raise TypeError("Playlist must be a list.")
        elif playlist == []:
            raise EmptyPlaylistError("Playlist can not be empty.")
        else:
            self._playlist = playlist
        #Repeat must be a list as user is going to pick which
        #audio files to playback according to the index of the 
        #list.
        if isinstance(repeat, list) == False:
            raise TypeError("This must be a list.")
        elif repeat == []:
            self._repeat = [0 for x in range(len(playlist))]        
        #Length must be same as queue so the indexs match up.
        elif not len(repeat) == len(playlist):
            raise IndexError("Each index in the repeat parameter list \
                  must correspond to an item in a list.")
        else:
            self._repeat = repeat
        #Keep track of track we are on.
        #Don't want to delete items from list so we can implement 
        #forwards/backwards.
        self._current = 0   
        #Shuffle can only be a boolean value so we know whether 
        #to do it or not.
        if isinstance(shuffle, bool) == False:
            raise TypeError("Shuffle parameter can only contain \
                  a True or False value.")
        else:
            self._shuffle = shuffle
    
    def __str__(self):
        """Tells user the position in the queue.

        Returns:
            string: message displaying the index in the queue.
        """
        return (f"Current position in queue is: {self._current}")

    #Convience function for checking if item needs to
    #be repeated.
    def repeat_checker(self):
        playsound(str(self._playlist[self._current]))
        #If the repeat tracker is at 0 , you can 
        #move on to the next track.
        if self._repeat_tracker[self._current] == 0:
            return False
        else:
            self._repeat_tracker[self._current] -= 1

    def shuffle_setup(self):
        #Convience function.
        #Using a dico to store repeat index as the playlist will 
        #become reordered.
        repeat_dico = {}
        for x in range(len(self._playlist)):
            repeat_dico[self._playlist[x]] = self._repeat[x]
        random.shuffle(self._playlist)
        #Remakes the repeat list in the correct order as each
        #path is a unique key in the dictonary.
        self._repeat = []
        for item in self._playlist:
            self._repeat.append(repeat_dico[item])
        #Avoids this function from being repeated again.
        self._shuffle = False

    def play(self):  
        """Plays the tracks in based upon the queue and user
        selection.
        """
        if self._shuffle == True:
            self.shuffle_setup()                             
        #Use this to keep track of repeats 
        #without effecting the other list.
        self._repeat_tracker = self._repeat.copy()
        while self._current < len(self._playlist):
            if self.repeat_checker() == False:
                self._current += 1
    
    def forward(self, spaces=1):
        """Skips tracks in the queue. (positive direction)

        Args:
            spaces (int, optional): User can specify how many positions 
            in the queue to skip. Defaults to 1.
        """
        if isinstance(spaces, int):
            raise(TypeError, "Parameter must be a whole number")
        elif spaces < 0:
            raise(ValueError, "Parameter must be 1 or more")
        else:
            self._current += spaces % len(self._current)
            self.play()

    def backwards(self, spaces=1):
        """Skips tracks in the queue. (negative direction)

        Args:
            spaces (int, optional): User can specify how many positions 
            in the queue to skip. Defaults to 1.
        """
        if isinstance(spaces, int):
            raise(TypeError, "Parameter must be a whole number")
        elif spaces < 0:
            raise(ValueError, "Parameter must be 1 or more")
        else:
            self._current -= spaces % len(self._current)
            self.play()


#To focus on selecting items before implementing the player.
class queue:
    def __init__(self, discovered):
        """Sets the default queue as everything that is discovered.

        Args:
            discovered (list): All .wav files found, as seen in the
            finder class.
        """
        self._user_queue = discovered
    
    def __str__(self):
        """Overwrite string function.

        Returns:
            string: shows all the audio files avaliable
        """
        temp_str = ""
        for item in self._user_queue:
            #Simple list without path and .wav extention.
            index1 = item.rfind("\\")
            index2 = item.rfind(".wav")
            temp_str = temp_str + (item[index1 + 2:index2]) + ","
        return temp_str[:-1]
    
    def delete(self, location):
        """Deletes item in a queue.

        Args:
            location (integer): index of the item that needs to
            be deleted.
        """
        del self._user_queue[location]
    
    def search(self, keyword):
        """To search for audio files already in the queue.

        Args:
            keyword (string): search term

        Returns:
            string: contains all matching items with the
            corrosponding index.
        """
        string = ""
        for x in range(len(self._user_queue)):
            if keyword in self._user_queue[x]:
                #Find the last one in the path to extract just 
                #the file name.
                word = self._user_queue[x][((self._user_queue[x]).rfind("\\") + 1): \
                                           ((self._user_queue[x]).rfind(".wav"))]
                #Lists the index of everything with the keyword so they can 
                #choose what to delete.
                string = f"{string} \n {x}:{word}"         
        return string   
    
    def load(self, shuffle=False, repeat=[]):
        """To load the playlist into the player class.

        Args:
            shuffle (bool, optional): play in the order specified or not. Defaults to False.
            repeat (list, optional): specifies what songs need to be repeated. Defaults to empty list.

        Returns:
            player: this gets the audio files ready to play within python.
        """
        return player(self._user_queue, shuffle, repeat)
        

class DirectoryNotFoundError(Exception):
    pass

#To focus on traversing file directories in order to find audio files.
class finder:
    def __init__(self):
        """Sets the default starting directory as the current folder.
           Creates a list to save items that have been found to.
        """
        self._working_dir = os.getcwd()
        self._discovered_items = []
    
    def __str__(self):
        return (f"Current working directory is {self._working_dir}.")
        
    def current_dir(self):
        """Tells the user which directory will be searched

        Returns:
            String: Path within the file system.
        """
        return self._working_dir

    def set_working_dir(self, path):
        """Changes the directory that will be searched. Checks if it
        is valid before saving.

        Args:
            path (string): Path within the file system.

        Raises:
            DirectoryNotFoundError: Raises if the string entered isn't a 
            valid path.
        """
        if os.path.isdir(path):
            self._working_dir = path.replace("/","\\")
        else:
            raise DirectoryNotFoundError("this path is not valid.")
    
    def full_path(self, items, dir_used):
        """Convience function provided to add the paths 
           to filenames.

        Args:
            search_queue (list): a list of filenames
            dir_used (string): the directory that needs to be attached.

        Returns:
            list: updated list which includes the filenames 
            with the directory.
        """
        for counter in range(len(items)):
            items[counter] = str(dir_used) + "\\" + \
                                    str(items[counter]) 
        return items

    def search(self):
        """Starts the directory set and looks for wav files.

        Returns:
            list: all .wav files found.
        """
        #This is need to ensure that all files, have paths 
        #attached so they can be accessed by anyone.
        search_queue = os.listdir(self._working_dir)
        search_queue = self.full_path(search_queue, self._working_dir)
        while len(search_queue) != 0:       
            for item in search_queue:
                filename, file_extention = os.path.splitext(item)
                if file_extention == ".wav":
                    self._discovered_items.append(item)
                elif os.path.isdir(item):
                    #If it is a folder, it adds everything to the queue while 
                    #displaying the full directory.
                    new_items_to_add = self.full_path(os.listdir(item), item)   
                    for item in new_items_to_add:
                        search_queue.append(item)       
                #Removes first item off the list as it has been checked.         
                search_queue = search_queue[1:]
        return queue(self._discovered_items)

f = finder()
q = f.search()
p = q.load(shuffle = True, repeat=[1,0,0])
p.play()