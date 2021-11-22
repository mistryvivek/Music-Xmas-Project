import os

#To focus on the control of audio playback.
class player:
    def __init__(self):
        pass

    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

#To focus on traversing file directories in order to find audio files.
class finder:
    def __init__(self):
        """Sets the default starting directory as the current folder.
           Creates a list to save items that have been found to.
        """
        self._working_dir = os.getcwd()
        self._discovered_items = []

    def current_dir(self):
        """Tells the user which directory will be searched

        Returns:
            String: Path within the file system.
        """
        return self._working_dir

    def set_working_dir(self, path):
        """Changes the directory that will be searched

        Args:
            path (string): Path within the file system.

        Raises:
            TypeError: A blank string would not be a valid path.
        """
        if path == None:
            raise TypeError("A valid path must be entered.")
        else:
            self._working_dir = path

    def search(self):
        pass

