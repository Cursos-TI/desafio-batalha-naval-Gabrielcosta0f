import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from batalha_naval import Board, FLEET, in_bounds

def test_in_bounds():
    assert in_bounds(0, 0)
    assert not in_bounds(-1, 0)
    assert not in_bounds(10, 10)

def test_place_random_fleet_and_shoot():
    b = Board()
    b.place_random_fleet()
    hits = 0
    for r in range(10):
        for c in range(10):
            res, _ = b.receive_shot((r, c))
            if res in ("acertou", "afundou"):
                hits += 1
    assert hits > 0
    assert b.all_sunk  # após cobrir todo o tabuleiro, toda a frota deve estar afundada
