from core.Config import conf


class Defects4j(object):
    def __init__(self):
        pass

    def getBinPath(self):
        return conf.defects4jRoot + '/framework/bin'
