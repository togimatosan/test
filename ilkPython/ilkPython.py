#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sayı Bulmaca (Emoji'siz Console Versiyonu)
- Zorluk seçimi (Kolay/Orta/Zor/Çılgın)
- Belirli deneme hakkı
- Akıllı ipuçları: yüksek/düşük, 'çok yakın', yakınlık karşılaştırması
- Hatalı giriş/taşan aralık kontrolü
- Oyun bittiğinde tekrar oynama
"""

from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass(frozen=True)
class Difficulty:
    name: str
    low: int
    high: int
    attempts: int

DIFFICULTIES = {
    "1": Difficulty("Kolay", 1, 50, 8),
    "2": Difficulty("Orta", 1, 100, 10),
    "3": Difficulty("Zor", 1, 500, 12),
    "4": Difficulty("Çılgın", -999, 999, 14),
}

def pick_difficulty() -> Difficulty:
    print("\n=== SAYI BULMACA ===")
    print("Bir zorluk seç:")
    for key, diff in DIFFICULTIES.items():
        print(f"  {key}) {diff.name}  [{diff.low}..{diff.high}]  Deneme: {diff.attempts}")
    while True:
        choice = input("Seçimin (1-4): ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("Geçersiz seçim. 1-4 arası bir değer gir.")

def read_guess(prompt: str, low: int, high: int) -> Optional[int]:
    raw = input(prompt).strip().lower()
    if raw in {"q", "quit", "exit"}:
        return None
    try:
        val = int(raw)
    except ValueError:
        print("⚠ Lütfen tam sayı gir (veya çıkmak için q).")
        return read_guess(prompt, low, high)
    if val < low or val > high:
        print(f"⚠ Aralık dışında! {low} ile {high} arasında bir sayı gir.")
        return read_guess(prompt, low, high)
    return val

def proximity_hint(secret: int, guess: int) -> str:
    diff = abs(secret - guess)
    if diff == 0:
        return "Tam isabet!"
    if diff <= 2:
        return "Çok çok yakın!"
    if diff <= 5:
        return "Çok yakın!"
    if diff <= 10:
        return "Yakın."
    if diff <= 25:
        return "Uzak sayılmaz."
    return "Uzak."

def temp_hint(secret: int, guess: int, prev_guess: Optional[int]) -> str:
    if prev_guess is None:
        return ""
    prev_diff = abs(secret - prev_guess)
    now_diff = abs(secret - guess)
    if now_diff < prev_diff:
        return "(Daha yaklaştın)"
    if now_diff > prev_diff:
        return "(Uzaklaştın)"
    return "(Aynı uzaklık)"

def play_round(diff: Difficulty) -> Tuple[bool, int]:
    secret = random.randint(diff.low, diff.high)
    attempts_left = diff.attempts
    prev_guess: Optional[int] = None

    print(f"\n{diff.name} modundasın. {diff.low} ile {diff.high} arasında bir sayı tuttum.")
    print(f"{attempts_left} deneme hakkın var. Çıkmak için 'q' yazabilirsin.\n")

    while attempts_left > 0:
        print(f"Kalan deneme: {attempts_left}")
        guess = read_guess("Tahminin: ", diff.low, diff.high)
        if guess is None:
            print("Oyundan çıkıldı.")
            return False, diff.attempts - attempts_left

        attempts_left -= 1

        if guess == secret:
            used = diff.attempts - attempts_left
            print(f"Tebrikler! Sayı {secret} idi. {used} denemede buldun.")
            return True, used

        hint_dir = "Yüksek!" if guess > secret else "Düşük!"
        print(f"{hint_dir} {proximity_hint(secret, guess)} {temp_hint(secret, guess, prev_guess)}\n")
        prev_guess = guess

    print(f"Deneme hakkın bitti. Doğru sayı: {secret}")
    return False, diff.attempts

def ask_replay() -> bool:
    ans = input("\nTekrar oyna? (e/h): ").strip().lower()
    return ans.startswith("e")

def main() -> None:
    while True:
        diff = pick_difficulty()
        win, used = play_round(diff)
        score = max(0, (diff.attempts - used + 1) * (1 if win else 0))
        if win:
            print(f"Skorun: {score}")
        if not ask_replay():
            print("Görüşürüz!")
            break

if __name__ == "__main__":
    main()
