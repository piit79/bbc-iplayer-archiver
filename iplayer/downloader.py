import converter
import os
import subprocess


def download(pid, directory=''):
    """
    Download an iPlayer episode to a specified directory.
    :param pid: string
    :param directory: string
    :rtype: string|False
    :return:
    """
    rtmp_cmd_str = converter.pid2rtmpdump(pid)
    if not rtmp_cmd_str:
        return False
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
            print "Could not create directory %s: %s" % (directory, ex)
            return False
    # launch the rtmpdump command
    retcode = subprocess.call(rtmp_cmd)
    # remove the file if the command failed
    if retcode > 0:
        os.remove(file_path)
        return False
    return filename


def flv2m4a(path):
    """
    Convert the given flv audio file to m4a.
    Only audio is converted, video is discarded.
    :param path: string
    :rtype: string|False
    """
    # replace the extension with m4a
    filename = os.path.basename(path)
    dirname = os.path.dirname(path)
    fileparts = filename.split('.')
    fileparts[-1] = "m4a"
    filename_out = '.'.join(fileparts)
    path_out = os.path.join(dirname, filename_out)
    ffmpeg_cmd = ["ffmpeg", "-i", path, "-vn", "-acodec", "copy", path_out]
    retcode = subprocess.call(ffmpeg_cmd)
    # remove the file if the command failed
    if retcode > 0:
        os.remove(path_out)
        return False
    return filename_out
