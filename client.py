import lxml.html
from pprint import pprint
import iplayerconverter as ipc


# pid = 'b00ptsjd'
pid = 'b03qkfxh'
EPISODES_URL = 'http://www.bbc.co.uk/programmes/%s/episodes/player'


def get_episodes(pid):
    url = EPISODES_URL % pid
    root = lxml.html.parse(url)
    episodes = []

    for div in root.findall('.//div/ol/li/div'):
        episode = {}
        episode['pid'] = div.get('data-pid')
        episode['url'] = div.get('resource')
        # span = div.findall('.//div/h4/a/span/span')[0]
        # prog_name = span.text
        metas = div.findall('.//div/div/div/a/meta')
        for meta in metas:
            prop = meta.get('property')
            content = meta.get('content')
            episode[prop] = content
        pprint(episode)
        episodes.append(episode)

    return episodes


eps = get_episodes(pid)

for ep in eps:
    rtmpcmd = ipc.pid2rtmpdump(ep['pid'])
    print rtmpcmd
