import csv

from dataclasses import dataclass

@dataclass
class Move:
    name: str
    move_type: str  # e.g., "Electric", "Water"
    power: int      # e.g., 90
    accuracy: int   # 0-100
    category: str   # "Physical", "Special", "Status"
    pp: int
    effect: str


def get_moves_db():
    moves_db = {}

    with open('moves.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            move = Move(
                name=row['name'],
                move_type=row['type'],
                power=int(row['power']),
                accuracy=int(row['accuracy']),
                category=row['category'],
                pp=int(row['pp']),
                effect=row['effect']
            )
            moves_db[move.name] = move
            
    return moves_db