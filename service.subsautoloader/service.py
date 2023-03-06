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

def findSub(path, language):
	dirs, files = xbmcvfs.listdir(path)

	if len(files) == 0:
		return ''

	for subFile in files[::-1]:
		if language.lower() in subFile.lower():
			return subFile
	return ''

def getSubFilePath(videoPath):
	videoFile = os.path.basename(videoPath)
	rootPath = os.path.dirname(videoPath)
	subVideoName = '.'.join(videoFile.split('.')[0:-1])
	subPath = rootPath + '/Subs'

	subLanguages = execRPC('Settings.GetSettingValue', { 'setting': 'subtitles.languages' })['value']
	debug('using subtitle language: ' + subLanguages[0])

	for path in [subPath, subPath + '/' + subVideoName]:
		foundSub = findSub(path, subLanguages[0])
		if foundSub:
			return path + '/' + foundSub

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