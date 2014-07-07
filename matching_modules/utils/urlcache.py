class UrlCache:
    def __init__(self):
        self.paths = []
    def add(self, path):
        split = path.find('/')
        if split == -1:
            self.paths.append((path, None))
            return
        prefix = path[:split]
        suffix = path[split+1:]
        for i in range(0, len(self.paths)):
            p = self.paths[i]
            if p[0] == prefix:
                if p[1] == None:
                    self.paths[i] = (prefix, UrlCache())
                    p = self.paths[i]
                p[1].add(suffix)
                return
        # New path in url cache
        new_url_path = UrlCache()
        new_url_path.add(suffix)
        self.paths.append((prefix, new_url_path))
    def checkUrl(self, path):
        split = path.find('/')
        prefix = ''
        suffix = ''
        if split == -1:
            prefix = path
        else:
            prefix = path[:split]
            suffix = path[split+1:]
        for p in self.paths:
            if p[0] == prefix:
                if p[1] == None:
                    return True
                else:
                    return p[1].checkUrl(suffix)
        return False
