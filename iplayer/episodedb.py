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
        programme_pid = episode['programmePid']
        episode_pid = episode['pid']
        if programme_pid not in self.data:
            return False
        return episode_pid in self.data[programme_pid]

    def add_episode(self, episode, autosave=True):
        programme_pid = episode['programmePid']
        episode_pid = episode['pid']
        # add programme if it doesn't exist yet
        if not self.has_programme(programme_pid):
            self.data[programme_pid] = {}
        self.data[programme_pid][episode_pid] = episode
        if autosave:
            self.save()

    def load(self):
        try:
            with open(self.filename, 'r') as fp:
                self.data = json.load(fp)
        except IOError:
            pass

    def get(self):
        """
        :return: dictionary representing the decoded JSON data
        """
        return self.data

    def set(self, data):
        self.data = data

    def save(self, data=None):
        if data is not None:
            self.set(data)
        try:
            with open(self.filename, 'w') as fp:
                json.dump(self.data, fp)
        except IOError:
            pass
