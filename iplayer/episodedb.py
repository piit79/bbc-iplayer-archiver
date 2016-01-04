import json


class EpisodeDatabase:
    """
    :type filename: string
    :type data: dict
    """
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        self.load()

    def has_programme(self, programme_pid):
        """
        Return True if the specified programme exists in the database
        :type programme_pid: str or unicode
        :rtype: boolean
        """
        return programme_pid in self.data

    def has_episode(self, episode):
        """
        Return True if the spedified episode exists in the database
        :type episode: dict
        :rtype: boolean
        """
        programme_pid = episode['programmePid']
        episode_pid = episode['pid']
        if programme_pid not in self.data:
            return False
        return episode_pid in self.data[programme_pid]

    def add_episode(self, episode, autosave=True):
        """
        Add episode into the database
        :type episode: dict
        :type autosave: boolean
        """
        programme_pid = episode['programmePid']
        episode_pid = episode['pid']
        # add programme if it doesn't exist yet
        if not self.has_programme(programme_pid):
            self.data[programme_pid] = {}
        self.data[programme_pid][episode_pid] = episode
        if autosave:
            self.save()

    def load(self):
        """
        Load the database from a json file
        :returns: True if loaded successfully, False otherwise
        :rtype: boolean
        """
        try:
            with open(self.filename, 'r') as fp:
                self.data = json.load(fp)
        except IOError:
            return False
        return True

    def get(self):
        """
        :returns: dictionary representing the decoded JSON data
        :rtype: dict
        """
        return self.data

    def set(self, data):
        self.data = data

    def save(self, data=None):
        """
        Save the database into a json file
        :type data: dict
        :returns: True if saved successfully, False otherwise
        :rtype: boolean
        """
        if data is not None:
            self.set(data)
        try:
            with open(self.filename, 'w') as fp:
                json.dump(self.data, fp)
        except IOError:
            return False
        return True
