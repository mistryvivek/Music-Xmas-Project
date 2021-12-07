import os

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


