from typing import List, Tuple, Any

User = [
    'username',
    'created_at',
    'password',
    'org',
]

Org = [
    'slug',
    'created_at',
    'name',
]

Patient = [
    'id',
    'created_at',
    'phone',
    'name',
    'gender',
    'creator_user',
]


class Model:
    def __init__(self, mapper: List, row: Tuple[Any]):
        assert len(mapper) == len(row)
        self.map = {}

        for i, key in enumerate(mapper):
            self.map[key] = row[i]

    def __getattr__(self, item):
        return self.map[item]

    def __getitem__(self, item):
        return self.map[item]
