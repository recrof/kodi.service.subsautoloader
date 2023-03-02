import xbmc, xbmcvfs, os, json

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

def getSubFilePath(videoPath):
	videoFile = os.path.basename(videoPath)
	rootPath = os.path.dirname(videoPath)
	subVideoName = '.'.join(videoFile.split('.')[0:-1])
	subPath = rootPath + '/Subs/' + subVideoName

	subLanguages = execRPC('Settings.GetSettingValue', { 'setting': 'subtitles.languages' })['value']
	debug('using subtitle language: ' + subLanguages[0])

	dirs, files = xbmcvfs.listdir(subPath)

	for subFile in files[::-1]:
		if subLanguages[0].lower() in subFile.lower():
			return subPath + '/' + subFile

	return ''

class Player(xbmc.Player):
	def onAVStarted(self):
		if not self.isPlayingVideo():
			return
		subtitles = self.getAvailableSubtitleStreams()
		if subtitles:
			return

		subFilePath = getSubFilePath(self.getPlayingFile())
		if subFilePath:
			debug('loading subtitle: ' + subFilePath)
			self.setSubtitles(subFilePath)

player = Player()
monitor = xbmc.Monitor()

while not monitor.abortRequested():
	monitor.waitForAbort(10)