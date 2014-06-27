# Methods for allowing a page

class AllowPage:
    def __init__(self, blockUrl):
        self.blockUrl = blockUrl
    def handleRequest(self, req, data):
        req.set_icap_response(200)
        req.no_adaptation_required()
    def handleResponse(self, res, data):
        res.set_icap_response(200)
        res.no_adaptation_required()

