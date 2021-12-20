import os
from typing import Type

class EmptyPlaylistError(Exception):
    pass

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
        #Shuffle can only be a boolean value so we know whether 
        #to do it or not.
        if isinstance(shuffle, bool) == False:
            raise TypeError("Shuffle parameter can only contain \
                  a True or False value.")
        #Repeat must be a list as user is going to pick which
        #audio files to playback according to the index of the 
        #list.
        if isinstance(repeat, list) == False:
            raise TypeError("This must be a list.")
        #Length must be same as queue so the indexs match up.
        elif not len(repeat) == len(playlist):
            raise IndexError("Each index in the repeat parameter list \
                  must correspond to an item in a list.")
        elif repeat == []:
            self._repeat = [None for x in range(len(playlist))]
        else:
            self._repeat = repeat
        #Keep track of track we are on.
        #Don't want to delete items from list so we can implement 
        #forwards/backwards.
        self._current = 0
        



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
    
    def load(self, playlist, shuffle=False, repeat=[]):
        """To load the playlist into the player class.

        Args:
            playlist (list): a list of all audio files
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
