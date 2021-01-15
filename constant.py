loljs = {}
YDL_OPTIONS = {'format': 'bestaudio/best',
               'restrictfilenames': True,
               'noplaylist': True,
               'nocheckcertificate': True,
               'ignoreerrors': True,
               'logtostderr': False,
               'quiet': True,
               'no_warnings': False,
               'default_search': 'auto',
               'source_address': '0.0.0.0'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}
