import downloader
import episodedb
import json
import lxml.html
import os
import urllib


class IPlayerArchiver:

    EPISODES_URL = 'http://www.bbc.co.uk/programmes/%s/episodes/player'

    def __init__(self, json_database, storage_root, programmes):
        self.db = episodedb.EpisodeDatabase(json_database)
        self.storage_root = storage_root
        self.programmes = programmes

    def get_episodes(self, programme_pid):
        url = IPlayerArchiver.EPISODES_URL % programme_pid
        root = lxml.html.parse(url)
        programme_name = ''
        for el in root.findall(".//a[@href='/programmes/%s']" % programme_pid):
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

    def get_date_published(self, url):
        root = lxml.html.parse(url)
        for div in root.findall('.//div[@property="datePublished"]'):
            date_published = div.get('content', False)
            return date_published
        return False

    def download_episode(self, episode):
        print "Downloading episode %s" % episode['pid']
        destdir = os.path.join(self.storage_root, episode['programmePid'])
        flv_path = downloader.download(episode['pid'], destdir)
        if not flv_path:
            print "Problem downloading episode %s!" % episode['pid']
            return False
        m4a_filename = downloader.flv2m4a(flv_path)
        if not m4a_filename:
            print "Problem converting episode %s to m4a!" % episode['pid']
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
            print "Cannot write info file %s: %s" % (info_path, ex)
            return False
        # update the episode database
        self.db.add_episode(episode)

    def run(self):
        for programme in self.programmes:
            print "Getting episodes for programme %s..." % programme
            episodes = self.get_episodes(programme)
            if len(episodes) < 1:
                print "No episodes found."
                continue
            print "%s: %d episodes found" % (episodes[0]['programmeName'], len(episodes))
            for episode in episodes:
                if not self.db.has_episode(episode):
                    self.download_episode(episode)
