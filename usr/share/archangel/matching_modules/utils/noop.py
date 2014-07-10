# noop method: do nothing
# We will use this, for example, in phrase

class NoOp:
    def __init__(self, blockUrl):
        self.blockUrl = blockUrl
    def handleRequest(self, req, data):
        return
    def handleResponse(self, res, data):
        return

