from abc import abstractmethod


class EpisodeDatabaseAbstract(object):
    """
    Abstract episode database class
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def has_programme(self, programme_pid):
        """
        Return True if the specified programme exists in the database
        :type programme_pid: str or unicode
        :rtype: boolean
        """
        pass

    @abstractmethod
    def has_episode(self, episode):
        """
        Return True if the specified episode exists in the database
        :type episode: dict
        :rtype: boolean
        """
        pass

    @abstractmethod
    def get_programme(self, programme_pid):
        """
        Get programme
        :param programme_pid: programme pid
        :type programme_pid: str or unicode
        :return: dictionary with programme data
        :rtype: dict
        """
        pass

    @abstractmethod
    def get_episode(self, episode):
        """
        Get episode
        :type episode: dict
        :return: dictionary with episode data
        :rtype: dict
        """
        pass

    @abstractmethod
    def add_programme(self, programme):
        """
        Add episode into the database
        :type programme: dict
        :return: True if on success, False on failure
        :rtype: bool
        """
        pass

    @abstractmethod
    def add_episode(self, episode):
        """
        Add episode into the database
        :type episode: dict
        :return: True if on success, False on failure
        :rtype: bool
        """
        pass
