import converter
import cookielib
import os
import subprocess
import sys
import urllib2


def download_rtmp(pid, directory=''):
    """
    Download an iPlayer episode using rtmpdump to a specified directory.
    :param pid: string
    :param directory: string
    :rtype: string|False
    """
    rtmp_cmd_str = converter.get_rtmpdump_cmd(pid)
    if not rtmp_cmd_str:
        return False
    # remove the quotes around the command line parameters
    rtmp_cmd_str = rtmp_cmd_str.translate(None, '"')
    rtmp_cmd = rtmp_cmd_str.split(' ')
    # prepend the directory to the output filename
    filename = rtmp_cmd[-1]
    file_path = os.path.join(directory, filename)
    rtmp_cmd[-1] = file_path
    # create the directory if needed
    if directory != '' and not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except OSError as ex:
            print u"Could not create directory {0:s}: {1:s}".format(directory, ex)
            return False
    # launch the rtmpdump command
    retcode = subprocess.call(rtmp_cmd)
    # remove the file if the command failed
    if retcode > 0:
        os.remove(file_path)
        return False
    return file_path


def download_hls(pid, directory='', progress=False):
    """
    Download an iPlayer episode from a HLS stream to a specified directory
    :param pid: string
    :param directory: string
    :param progress: boolean show a download progress
    :rtype: string|false output file path
    """
    playlist_url = converter.get_pid_info(pid).get('hls', False)
    if not playlist_url:
        return False

    # create the directory if needed
    if directory != '' and not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except OSError as ex:
            print u"Could not create directory {0:s}: {1:s}".format(directory, ex)
            return False

    # open the output file
    filename = pid + '.ts'
    file_path = os.path.join(directory, filename)
    try:
        ts_fp = open(file_path, 'w')
    except IOError as ex:
        print u"Could not create output file {0:s}: {1:s}".format(file_path, ex)
        return False

    # get the m3u playlist URL
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    res = opener.open(playlist_url)
    m3u_url = False
    for line in res:
        # skip comments
        if line.lstrip()[:1] == '#':
            continue
        # first non-comment line is the m3u URL
        m3u_url = line.strip()
        break
    if not m3u_url:
        return False

    # get the segment URLs from the M3U playlist using the same opener to send the required cookies
    res = opener.open(m3u_url)
    segments = []
    for line in res:
        if line.lstrip()[:1] == '#':
            continue
        segments.append(line.strip())

    # download the segments and write them into a single file
    step = 10
    cur_percent = -step
    cur_seg = 1
    num_seg = len(segments)
    for seg in segments:
        res = opener.open(seg)
        ts_fp.write(res.read())
        if 100.0 * cur_seg / num_seg >= cur_percent + step:
            cur_percent += step
            if progress:
                print "{0:d}%".format(cur_percent),
                sys.stdout.flush()
        cur_seg += 1
    if progress:
        if cur_percent < 100:
            print '100%'
        else:
            print ''
    return file_path


def remux_to_m4a(path, fix_aac=True):
    """
    Convert the given flv audio file to m4a.
    Only audio is converted, video is discarded.
    :param path: string input file name
    :param fix_aac: boolean whether to use a filter to fix the AAC bitstream
    :rtype: string|False output file path
    """
    # replace current extension with m4a
    filename = os.path.basename(path)
    dirname = os.path.dirname(path)
    fileparts = filename.rsplit('.', 1)
    fileparts[-1] = "m4a"
    filename_out = '.'.join(fileparts)
    # build the ffmpeg command line
    path_out = os.path.join(dirname, filename_out)
    ffmpeg_cmd = ["ffmpeg", "-v", "error", "-i", path, "-vn", "-acodec", "copy"]
    # add filter parameter to fix aac bitstream
    if fix_aac:
        ffmpeg_cmd.extend(["-bsf:a", "aac_adtstoasc"])
    ffmpeg_cmd.append(path_out)
    retcode = subprocess.call(ffmpeg_cmd)
    # remove the file if the command failed
    if retcode > 0:
        os.remove(path_out)
        return False
    return filename_out
