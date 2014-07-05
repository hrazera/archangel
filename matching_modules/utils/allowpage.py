# Methods for allowing a page

class AllowPage:
    def __init__(self, blockUrl):
        self.blockUrl = blockUrl
    def handleRequest(self, req, data):
        req.no_adaptation_required()
    def handleResponse(self, res, data):
        res.no_adaptation_required()

