import xbmc, xbmcvfs, os, json, xbmcgui, xbmcaddon

addon = xbmcaddon.Addon()

def debug(msg):
    xbmc.log('[service.subsautoloader] ' + msg, xbmc.LOGINFO)

def execRPC(method, params):
    rpcCallObject = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': 1
    }
    resObject = json.loads(xbmc.executeJSONRPC(json.dumps(rpcCallObject)))
    return resObject['result']

# Load user-configured language mappings
language_mapping = {}

# Loop through possible language slots in settings.xml
for i in range(1, 8):  # Assuming you have 7 slots, adjust as needed
    lang = addon.getSetting(f'language{i}').lower()
    lang_code = addon.getSetting(f'langcode{i}').lower()
    if lang and lang_code:  # Only add if both fields are not empty
        language_mapping[lang] = [lang_code]

debug(f'Loaded language mapping from settings: {language_mapping}')

def find_subs_folder(rootPath):
    # Check default folder first
    defaultsubsdir = addon.getSetting('defaultsubsdir')
    debug(f'Checking for default subs folder: {defaultsubsdir}')
    if defaultsubsdir and xbmcvfs.exists(os.path.join(rootPath, defaultsubsdir)):
        return os.path.join(rootPath, defaultsubsdir)
    # Check other possible folders
    possible_folders = {'Subs', 'Sub', 'Subtitles', 'subs', 'sub', 'subtitles'}
    for folder in xbmcvfs.listdir(rootPath)[0]:
        if folder in possible_folders:
            return os.path.join(rootPath, folder)
    # Return None if none of the folders exist
    return None
        
def getSubFilePaths(videoPath):
    # Extract the video file name from the video path
    videoFile = os.path.basename(videoPath)
    # Extract the root path from the video path
    rootPath = os.path.dirname(videoPath)
    # Construct the subtitle path using the root path
    subPath = find_subs_folder(rootPath)
    if subPath is None:
        return None
    debug(f'Checking for subtitles in: {subPath}')
    # Get the user-configured subtitle language from Kodi settings
    subLanguage = execRPC('Settings.GetSettingValue', {'setting': 'subtitles.languages'})['value'][0].lower()
    # Print the subtitle language used
    debug(f'Using subtitle language: {subLanguage}')
    # Get the possible subtitle codes for the language
    possible_sub_codes = language_mapping.get(subLanguage, [subLanguage])
    # Initialize lists to store main and other subtitles
    main_subs, other_subs = [], []

    # Loop through two possible subtitle paths
    for path in [subPath, os.path.join(subPath, os.path.splitext(videoFile)[0])]:
        try:
            # List the files in the subtitle path
            for subFile in xbmcvfs.listdir(path)[1]:
                # Convert the subtitle file name to lowercase
                subFileLower = subFile.lower()
                # Check if the subtitle file name contains any of the possible subtitle codes
                if any(subCode.lower() in subFileLower for subCode in possible_sub_codes):
                    # If it does, add it to the main subtitle list
                    main_subs.append(os.path.join(path, subFile))
                else:
                    # Loop through the language mappings
                    for lang, codes in language_mapping.items():
                        # Skip the language that was already checked
                        if lang == subLanguage:
                            continue
                        # Check if the subtitle file name contains any of the codes for the language
                        if any(subCode.lower() in subFileLower for subCode in codes):
                            # If it does, add it to the other subtitle list and break the loop
                            other_subs.append(os.path.join(path, subFile))
                            break
        # If an error occurs while listing the files or searching for subtitles, print the error
        except Exception as e:
            debug(f"Error while searching for subtitles: {str(e)}")
            pass

    # Return the concatenated lists of main and other subtitles
    return main_subs + other_subs

class Player(xbmc.Player):

    # def onPlayBackStarted(self):
        # """Called when playback starts."""
    def onAVStarted(self):
        """
        Called when video is ready for playback.
        Checks if subtitles are already available.
        If not, it retrieves the video path and searches for subtitles.
        If subtitles are found, it creates a new ListItem with the video path and sets the subtitles.
        Then it restarts playback with the new ListItem and video path.
        """
        # Check if the current playback is for a video
        if not self.isPlayingVideo():
            return
        
        # Check if subtitles are already available
        subtitles = self.getAvailableSubtitleStreams()
        if subtitles:
            # Print the available subtitles
            debug(f'Subtitle streams already available: {subtitles}')
            return
        
        # Get the path of the currently playing video
        video_path = self.getPlayingFile()
        
        # Search for subtitles based on the video path
        subFilePaths = getSubFilePaths(video_path)
        
        if subFilePaths:
            # Print the found subtitles
            debug('Found subtitles: ' + ', '.join(subFilePaths))
            
            # Create a new ListItem with the video path
            list_item = xbmcgui.ListItem(path=video_path)
            
            # Set the subtitles for the ListItem
            list_item.setSubtitles(subFilePaths)
            
            # Print the subtitles set for the ListItem
            debug(f'Subtitles set for ListItem before playback: {subFilePaths}')
            
            # Restart playback with the new ListItem and video path
            self.play(video_path, list_item)
        else:
            # Print if no matching subtitles were found
            debug('No matching subtitles found.')

player = Player()
monitor = xbmc.Monitor()

while not monitor.abortRequested():
    monitor.waitForAbort(10)
