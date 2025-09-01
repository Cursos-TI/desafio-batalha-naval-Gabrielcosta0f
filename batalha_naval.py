from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set, Dict, Any
import json
import random
import string
import os

Coord = Tuple[int, int]  # (linha, coluna) 0-index

BOARD_SIZE = 10
FLEET = {
    "Porta-avioes": 5,
    "Encouracado": 4,
    "Cruzador A": 3,
    "Cruzador B": 3,
    "Destroyer": 2,
}

LETTERS = string.ascii_uppercase[:BOARD_SIZE]  # 'A'..'J'


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def parse_coord(text: str) -> Optional[Coord]:
    """Converte 'A1'..'J10' em (linha,coluna). Retorna None se inválido."""
    text = text.strip().upper()
    if text in {"SAIR", "SALVAR"} or text.startswith("SALVAR "):
        return None
    if len(text) < 2 or len(text) > 3:
        return None
    row_letter = text[0]
    if row_letter not in LETTERS:
        return None
    try:
        col_num = int(text[1:])
    except ValueError:
        return None
    if not (1 <= col_num <= BOARD_SIZE):
        return None
    return (LETTERS.index(row_letter), col_num - 1)


def neighbors8(r: int, c: int) -> List[Coord]:
    res = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if in_bounds(rr, cc):
                res.append((rr, cc))
    return res


@dataclass
class Ship:
    name: str
    size: int
    cells: List[Coord]
    hits: Set[Coord]

    @classmethod
    def placed(cls, name: str, size: int, start: Coord, horizontal: bool) -> "Ship":
        r, c = start
        cells = [(r, c + i) if horizontal else (r + i, c) for i in range(size)]
        return cls(name, size, cells, set())

    def register_hit(self, coord: Coord) -> None:
        if coord in self.cells:
            self.hits.add(coord)

    @property
    def sunk(self) -> bool:
        return len(self.hits) == self.size

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "size": self.size, "cells": list(self.cells), "hits": list(self.hits)}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Ship":
        return cls(d["name"], d["size"], [tuple(x) for x in d["cells"]], set(tuple(x) for x in d["hits"]))


class Board:
    def __init__(self) -> None:
        self.ships: List[Ship] = []
        self.shots: Set[Coord] = set()  # tiros recebidos

    def _can_place(self, size: int, start: Coord, horizontal: bool) -> bool:
        r, c = start
        cells = [(r, c + i) if horizontal else (r + i, c) for i in range(size)]
        if any(not in_bounds(rr, cc) for rr, cc in cells):
            return False
        occupied = {cell for ship in self.ships for cell in ship.cells}
        for rr, cc in cells:
            if (rr, cc) in occupied:
                return False
            if any(n in occupied for n in neighbors8(rr, cc)):
                return False
        return True

    def place_random_fleet(self) -> None:
        for name, size in FLEET.items():
            placed = False
            for _ in range(500):
                horizontal = bool(random.getrandbits(1))
                if horizontal:
                    r = random.randrange(BOARD_SIZE)
                    c = random.randrange(BOARD_SIZE - size + 1)
                else:
                    r = random.randrange(BOARD_SIZE - size + 1)
                    c = random.randrange(BOARD_SIZE)
                if self._can_place(size, (r, c), horizontal):
                    self.ships.append(Ship.placed(name, size, (r, c), horizontal))
                    placed = True
                    break
            if not placed:
                raise RuntimeError("Falha ao posicionar frota.")

    def receive_shot(self, coord: Coord) -> Tuple[str, Optional[str]]:
        """Registra tiro; retorna (resultado, nome_do_navio_ou_None).
        resultado ∈ {"repetido", "agua", "acertou", "afundou"}
        """
        if coord in self.shots:
            return ("repetido", None)
        self.shots.add(coord)
        for ship in self.ships:
            if coord in ship.cells:
                ship.register_hit(coord)
                if ship.sunk:
                    return ("afundou", ship.name)
                return ("acertou", ship.name)
        return ("agua", None)

    @property
    def all_sunk(self) -> bool:
        return all(s.sunk for s in self.ships)

    def render(self, reveal: bool = False) -> str:
        grid = [["·" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        occupied = {cell: ship for ship in self.ships for cell in ship.cells}
        for r, c in self.shots:
            grid[r][c] = "X" if (r, c) in occupied else "o"
        if reveal:
            for ship in self.ships:
                for r, c in ship.cells:
                    if grid[r][c] == "·":
                        grid[r][c] = "#"
        header = "   " + " ".join(f"{i:>2}" for i in range(1, BOARD_SIZE + 1))
        lines = [header]
        for i, row in enumerate(grid):
            lines.append(f"{LETTERS[i]}  " + "  ".join(row))
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {"ships": [s.to_dict() for s in self.ships], "shots": list(self.shots)}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Board":
        b = cls()
        b.ships = [Ship.from_dict(sd) for sd in d["ships"]]
        b.shots = set(tuple(x) for x in d["shots"])  # type: ignore
        return b


class HuntAI:
    """IA simples: atira aleatoriamente até acertar; depois caça adjacentes."""

    def __init__(self) -> None:
        self.candidates: List[Coord] = []
        self.seen: Set[Coord] = set()

    def next_shot(self) -> Coord:
        while self.candidates:
            r, c = self.candidates.pop()
            if (r, c) not in self.seen:
                self.seen.add((r, c))
                return (r, c)
        cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if (r + c) % 2 == 0]
        random.shuffle(cells)
        for r, c in cells:
            if (r, c) not in self.seen:
                self.seen.add((r, c))
                return (r, c)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if (r, c) not in self.seen:
                    self.seen.add((r, c))
                    return (r, c)
        return (0, 0)

    def feedback(self, coord: Coord, result: str) -> None:
        if result in ("acertou", "afundou"):
            r, c = coord
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                rr, cc = r + dr, c + dc
                if in_bounds(rr, cc):
                    self.candidates.append((rr, cc))

    def to_dict(self) -> Dict[str, Any]:
        return {"candidates": list(self.candidates), "seen": list(self.seen)}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "HuntAI":
        ai = cls()
        ai.candidates = [tuple(x) for x in d.get("candidates", [])]  # type: ignore
        ai.seen = set(tuple(x) for x in d.get("seen", []))  # type: ignore
        return ai


class Game:
    def __init__(self) -> None:
        self.mode: str = "pvc"  # pvc | pvp
        self.turn: int = 1  # 1 ou 2/CPU
        self.p1 = Board()
        self.p2 = Board()
        self.ai: Optional[HuntAI] = None

    # ===== Persistência =====
    def save(self, path: str = "save.json") -> None:
        data = {
            "mode": self.mode,
            "turn": self.turn,
            "p1": self.p1.to_dict(),
            "p2": self.p2.to_dict(),
            "ai": self.ai.to_dict() if self.ai else None,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        print(f"Partida salva em '{path}'.")

    @classmethod
    def load(cls, path: str) -> "Game":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        g = cls()
        g.mode = data["mode"]
        g.turn = data["turn"]
        g.p1 = Board.from_dict(data["p1"])
        g.p2 = Board.from_dict(data["p2"])
        g.ai = HuntAI.from_dict(data["ai"]) if data.get("ai") else None
        return g

    # ===== Setup =====
    def setup_new(self, mode: str) -> None:
        self.mode = mode
        self.turn = 1
        self.p1.place_random_fleet()
        self.p2.place_random_fleet()
        self.ai = HuntAI() if mode == "pvc" else None

    # ===== Loop =====
    def play(self) -> None:
        print("=== BATALHA NAVAL — Estácio ===")
        choice = input("[1] Jogador x CPU  [2] 2 Jogadores  [C] Carregar: ").strip().lower()
        if choice == "c":
            path = input("Arquivo .json para carregar: ").strip()
            if not os.path.exists(path):
                print("Arquivo não encontrado. Iniciando novo jogo x CPU.")
                self.setup_new("pvc")
            else:
                loaded = Game.load(path)
                self.__dict__.update(loaded.__dict__)
        elif choice == "2":
            self.setup_new("pvp")
        else:
            self.setup_new("pvc")

        while True:
            if self.mode == "pvc":
                if self.turn == 1:
                    if self._human_turn(player=1):
                        return
                else:
                    self._cpu_turn()
                if self.p2.all_sunk:
                    print("\nParabéns! Você venceu. Todas as embarcações inimigas foram afundadas.")
                    return
                if self.p1.all_sunk:
                    print("\nFim de jogo. A CPU venceu desta vez.")
                    return
            else:  # pvp
                if self._human_turn(player=self.turn):
                    return
                if self.p2.all_sunk:
                    print("\nJogador 1 venceu!")
                    return
                if self.p1.all_sunk:
                    print("\nJogador 2 venceu!")
                    return

    # ===== Turnos =====
    def _human_turn(self, player: int) -> bool:
        board_enemy = self.p2 if player == 1 else self.p1
        board_self = self.p1 if player == 1 else self.p2

        print("\n" + ("Seu tabuleiro:" if self.mode == "pvc" and player == 1 else f"Tabuleiro do Jogador {player}:"))
        print(board_self.render(reveal=True))
        print("\nAlvos atacados no inimigo (X=acerto, o=água):")
        print(board_enemy.render(reveal=False))

        prompt = "Sua jogada (ex: A5), 'salvar [nome].json' ou 'sair': "
        if self.mode == "pvp":
            print("\n>>> Passe o teclado ao **Jogador {0}**. Não olhe a tela do adversário!".format(player))
        while True:
            raw = input("\n" + prompt).strip()
            if raw.lower().startswith("salvar"):
                parts = raw.split(maxsplit=1)
                path = parts[1] if len(parts) == 2 else "save.json"
                try:
                    self.save(path)
                except Exception as e:
                    print("Falha ao salvar:", e)
                continue
            if raw.lower() == "sair":
                print("Até a próxima!")
                return True
            coord = parse_coord(raw)
            if coord is None:
                print("Entrada inválida. Use formato A1..J10 ou comandos 'salvar'/'sair'.")
                continue
            res, name = board_enemy.receive_shot(coord)
            if res == "repetido":
                print("Você já atirou ali.")
                continue
            if res == "agua":
                print("Água!")
            elif res == "acertou":
                print(f"Acertou um {name}!")
            else:
                print(f"Afundou o {name}!")
            self.turn = 2 if (self.mode == "pvc" and self.turn == 1) or (self.mode == "pvp" and player == 1) else 1
            return False

    def _cpu_turn(self) -> None:
        assert self.ai is not None
        cpu_coord = self.ai.next_shot()
        res, name = self.p1.receive_shot(cpu_coord)
        self.ai.feedback(cpu_coord, res)
        row = LETTERS[cpu_coord[0]]
        col = cpu_coord[1] + 1
        if res == "agua":
            print(f"CPU atirou em {row}{col}: Água.")
        elif res == "acertou":
            print(f"CPU acertou seu {name} em {row}{col}!")
        else:
            print(f"CPU afundou seu {name} em {row}{col}!")
        self.turn = 1


if __name__ == "__main__":
    Game().play()