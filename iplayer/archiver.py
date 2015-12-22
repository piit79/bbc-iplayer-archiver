import downloader
import episodedb
import json
import lxml.html
import os
import urllib


class IPlayerArchiver:

    EPISODES_URL = u'http://www.bbc.co.uk/programmes/{0:s}/episodes/player'

    def __init__(self, json_database, storage_root, programmes):
        self.db = episodedb.EpisodeDatabase(json_database)
        self.storage_root = storage_root
        self.programmes = programmes

    def get_episodes(self, programme_pid):
        url = IPlayerArchiver.EPISODES_URL.format(programme_pid)
        root = lxml.html.parse(url)
        programme_name = ''
        for el in root.findall(u".//a[@href='/programmes/{0:s}']".format(programme_pid)):
            programme_name = el.get('title')
            break
        episodes = []
        for div in root.findall('.//div/ol/li/div'):
            episode_pid = div.get('data-pid')
            episode_url = div.get('resource')
            # skip "podcast" episodes (pid starts with a 'p')
            if episode_pid[0] == 'p':
                continue
            episode = {
                'pid': episode_pid,
                'url': episode_url,
                'programmeName': programme_name,
            }
            metas = div.findall('.//div/div/div/a/meta')
            for meta in metas:
                prop = meta.get('property')
                content = meta.get('content')
                episode[prop] = content
            date_published = self.get_date_published(episode_url)
            episode['datePublished'] = date_published
            episode['programmePid'] = programme_pid
            episodes.append(episode)

        return sorted(episodes, key=lambda ep: ep['datePublished'])

    @staticmethod
    def get_date_published(url):
        root = lxml.html.parse(url)
        for div in root.findall('.//div[@property="datePublished"]'):
            date_published = div.get('content', False)
            return date_published
        return False

    def download_episode(self, episode):
        print u"Downloading episode {0:s}".format(episode['pid'])
        destdir = os.path.join(self.storage_root, episode['programmePid'])
        raw_path = downloader.download_hls(episode['pid'], destdir)
        if not raw_path:
            print u"Problem downloading episode {0:s}!".format(episode['pid'])
            return False
        m4a_path = downloader.remux_to_m4a(raw_path)
        if not m4a_path:
            print u"Problem converting episode {0:s} to m4a!".format(episode['pid'])
            return False
        # download the thumbnail
        thumbnail_ext = episode['thumbnailUrl'].split('.')[-1]
        thumbnail_path = os.path.join(destdir, episode['pid'] + '.' + thumbnail_ext)
        urllib.urlretrieve(episode['thumbnailUrl'], thumbnail_path)
        # write the info json file
        info_path = os.path.join(destdir, episode['pid'] + '.json')
        try:
            with open(info_path, 'w') as fp:
                json.dump(episode, fp, indent=4)
        except IOError as ex:
            print u"Cannot write info file {0:s}: {1:s}".format(info_path, ex)
            return False
        # update the episode database
        self.db.add_episode(episode)

    def run(self):
        for programme in self.programmes:
            print u"Getting episodes for programme {0:s}...".format(programme)
            episodes = self.get_episodes(programme)
            if len(episodes) < 1:
                print "No episodes found."
                continue
            print u"{0:s}: {1:d} episodes found".format(episodes[0]['programmeName'], len(episodes))
            for episode in episodes:
                if not self.db.has_episode(episode):
                    self.download_episode(episode)
                else:
                    print u"Episode {0:s} - {1:s} already downloaded".format(episode['pid'], episode['name'])
