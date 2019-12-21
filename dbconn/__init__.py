# -*- coding: utf-8 -*-

class DBResult:
    exists = False
    result = None
    error = None
    rows = None

    def index_of(self, index):
        if self.exists and isinstance(index, int) and index < self.rows and index >= -self.rows:
            return self.result[index]
        return None

    def get_first(self):
        return self.index_of(0)

    def get_last(self):
        return self.index_of(-1)

