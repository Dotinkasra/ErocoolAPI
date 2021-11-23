import dataclasses

@dataclasses.dataclass
class Result:
    _pagination: int
    _results: list

    @property
    def pagination(self):
        return self._pagination

    @property
    def results(self):
        return self._results