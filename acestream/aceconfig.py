'''
AceProxy configuration script
'''
import logging
import platform
from aceclient.acemessages import AceConst


class AceConfig(object):
    # ----------------------------------------------------
    # Ace Stream Engine configuration
    # ----------------------------------------------------
    #
    # Ace Stream API key (None uses remote key generator)
    # You probably shouldn't touch this
    acekey = None
    # Ace Stream Engine host
    # Change this if you use remote Ace Stream Engine
    # Remember that by default Ace Stream Engine listens only
    # Local host, so start it with --bind-all parameter
    acehost = '127.0.0.1'
    # Ace Stream Engine port (autodetect for Windows)
    aceport = 62062
    # Ace Stream age parameter (LT_13, 13_17, 18_24, 25_34, 35_44, 45_54,
    # 55_64, GT_65)
    aceage = AceConst.AGE_18_24
    # Ace Stream sex parameter (MALE or FEMALE)
    acesex = AceConst.SEX_MALE
    # Ace Stream Engine connection timeout
    aceconntimeout = 5
    # Ace Stream Engine authentication result timeout
    aceresulttimeout = 10
    # Message level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    debug = logging.DEBUG
    #
    # ----------------------------------------------------
    # AceProxy configuration
    # ----------------------------------------------------
    #
    # HTTP Server host
    httphost = '0.0.0.0'
    # HTTP Server port
    httpport = 8000
    # Maximum concurrent connections (video clients)
    maxconns = 10
    # Logging to a file
    loggingtoafile = False
    # Path for logs, default is current directory. For example '/tmp/'
    logpath = ''
    # Use VideoLAN VLC Media Player
    # I strongly recommend to use VLC, because it lags a lot without it
    # And multiple clients can't watch one stream without it.
    # That's Ace Stream Engine fault.
    # To use this, you should install VLC first
    # And run it with:
    # vlc -I telnet --clock-jitter 0 --network-caching 500 --telnet-pass admin
    vlcuse = True
    # VLC host
    vlchost = '127.0.0.1'
    # VLC telnet interface port
    vlcport = 4212
    # VLC streaming port (you shouldn't set it in VLC itself)
    vlcoutport = 8081
    # VLC telnet interface password
    vlcpass = 'acestream'
    # Pre-access (HTTP) VLC parameters
    # You can add transcode options here
    # Something like #transcode{acodec=mpga,ab=128,channels=2,samplerate=44100}
    vlcpreaccess = ''
    # VLC muxer. You probably want one of these streamable muxers:
    # ts, asf, flv, ogg, mkv
    # You can use ffmpeg muxers too, if your VLC is built with it
    # ffmpeg{mux=NAME} (i.e. ffmpeg{mux=mpegts})
    # VLC's ts muxer sometimes can work badly, but that's the best choice for
    # now.
    vlcmux = 'ts'
    # Force ffmpeg INPUT demuxer in VLC. Sometimes can help.
    vlcforceffmpeg = False
    # Stream start delay for dumb players (in seconds)
    # !!!
    # PLEASE set this to 0 if you use VLC
    # !!!
    videodelay = 0
    # Obey PAUSE and RESUME commands from Engine
    # (stops sending data to client, should prevent annoying buffering)
    # !!!
    # PLEASE set this to False if you use VLC
    # !!!
    videoobey = False
    # Stream send delay after PAUSE/RESUME commands (works only if option
    # above is enabled)
    # !!!
    # PLEASE set this to 0 if you use VLC
    # !!!
    videopausedelay = 0
    # Delay before closing Ace Stream connection when client disconnects
    # In seconds.
    videodestroydelay = 3
    # Pre-buffering timeout. In seconds.
    videotimeout = 40
    #
    # Some video players (mostly STBs and Smart TVs) can generate dummy requests
    # to detect MIME-type or something before playing which Ace Stream handles badly.
    # We send them 200 OK and do nothing.
    # We add their User-Agents here
    fakeuas = ('Mozilla/5.0 IMC plugin Macintosh', )
    #
    # Some video players have very short timeout and can disconnect from the proxy
    # before the headers sent.
    # We send them 200 OK and MPEG MIME-type right after connection has been initiated
    fakeheaderuas = ('HLS Client/2.0 (compatible; LG NetCast.TV-2012)',
                     'Mozilla/5.0 (DirectFB; Linux armv7l) AppleWebKit/534.26+ (KHTML, like Gecko) Version/5.0 Safari/534.26+ LG Browser/5.00.00(+mouse+3D+SCREEN+TUNER; LGE; 42LM670T-ZA; 04.41.03; 0x00000001;); LG NetCast.TV-2012 0'
                     )

    '''
    Run Ace Stream Engine if not running and get API port
    Only for Windows
    Do not touch this
    '''
    if platform.system() == 'Windows':
        import _winreg
        import os.path
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
        key = _winreg.OpenKey(reg, 'Software\AceStream')
        value = _winreg.QueryValueEx(key, 'EnginePath')
        dirpath = os.path.dirname(value[0])
        try:
            aceport = int(open(dirpath + '\\acestream.port', 'r').read())
        except IOError:
            # Ace Stream is not running, start it
            import subprocess
            import time
            subprocess.Popen([value[0]])
            _started = False
            for i in xrange(10):
                time.sleep(1)
                try:
                    aceport = int(
                        open(dirpath + '\\acestream.port', 'r').read())
                    _started = True
                    break
                except IOError:
                    _started = False
            if not _started:
                print "Can't start engine!"
                quit()
    '''
    Do not touch this
    '''
