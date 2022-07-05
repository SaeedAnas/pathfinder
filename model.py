from dataclasses import dataclass
import json
import util

@dataclass
class PositionEntry:
    id: int
    position: str
    days: int

@dataclass
class Pathway:
    position: str
    avg_time: float
    count: int
    next: list

    def __init__(self, position, avg_time):
        self.position = position
        self.avg_time = avg_time
        self.count = 1
        self.next = []

    def update_avg(self):
        self.avg_time = self.avg_time / self.count
    
    def increment(self):
        self.count += 1
    
    def add_path(self, path):
        self.next.append(path)

    def __repr__(self) -> str:
       return f"[Position: '{self.position}', Avg Time: '{self.avg_time}', Count: '{self.count}', Next: '{self.next}']" 

    def serialize(self):
        d = {
            'position': self.position,
            'avg_time': util.days_to_duration(self.avg_time),
            'count': self.count
        }

        return d

class Pathways:
    pathways: dict

    def __init__(self, pathways):
        self.pathways = pathways

    def get_positions(self):
        return list(self.pathways.keys())

    def get(self, position):
        position = position.lower()
        for p in self.pathways:
            if p.lower() == position:
                return p
        return None

    def predict(self, current):
        next = self.pathways[current].next

        if len(next) < 1:
            return None

        max = self.pathways[next[0]]

        for position in next[1:]:
            pathway = self.pathways[position]

            if pathway.count > max.count:
                max = pathway

        return max

