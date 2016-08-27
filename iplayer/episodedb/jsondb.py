import json
from abstractdb import EpisodeDatabaseAbstract


class EpisodeDatabaseJson(EpisodeDatabaseAbstract):
    """
    Episode database implementation backed by a JSON file
    :type filename: string
    :type data: dict
    """
    filename = None
    data = None

    def __init__(self, filename):
        super(EpisodeDatabaseJson, self).__init__()
        self.filename = filename
        self.data = {}
        self.load()

    def has_episode(self, episode):
        """
        Return True if the specified episode exists in the database
        :type episode: dict
        :rtype: boolean
        """
        programme_pid = episode['programmePid']
        episode_pid = episode['pid']
        if programme_pid not in self.data:
            return False
        return episode_pid in self.data[programme_pid]

    def get_episode(self, episode_pid):
        """
        Get episode
        :type episode_pid: str or unicode
        :return: dictionary with episode data
        :rtype: dict
        """
        pass

    def add_episode(self, episode):
        """
        Add episode into the database
        :type episode: dict
        :returns: True if on success, False on failure
        :rtype: bool
        """
        programme_pid = episode['programmePid']
        episode_pid = episode['pid']
        # add programme if it doesn't exist yet
        if not self.has_programme(programme_pid):
            self.data[programme_pid] = {}
        self.data[programme_pid][episode_pid] = episode
        return self.save()

    def load(self):
        """
        Load the database from a json file
        :return: True if loaded successfully, False otherwise
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
        :return: dictionary with database data
        :rtype: dict
        """
        return self.data

    def set(self, data):
        self.data = data

    def save(self, data=None):
        """
        Save the database into a json file
        :type data: dict
        :return: True if saved successfully, False otherwise
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
