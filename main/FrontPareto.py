import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import Counter

# === Input tangan ===
# Kontrak 1D
hand1 = ['9S', 'JS', '10S', 'KH', 'JH', '10H', '9H', '8H', 'QC', '8C', '2C', 'KD', 'JD']
hand2 = ['3S', '10H', '6H', 'AC', 'KC', 'JC', '9C', 'AD', '10D', '8D', '5D', '4D', '3D']
# Kontrak 5D
# hand1 = ['QS', 'JS', '10S', 'KH', 'JH', '10H', '9H', '8H', 'QC', '8C', '2C', 'KD', 'JD']
# hand2 = ['3S', 'QH', '6H', 'AC', 'KC', 'JC', '9C', 'AD', '10D', '8D', '5D', '4D', '3D']
# Kontrak 1NT
# hand1 = ['AS', 'KS', '8S', 'AH', '6H', '4H', '10D', '9D', '4D', 'JC', '10C', '7C', '6C']
# hand2 = ['6S', '5H', '2S', '8H', '7H', '3H', 'AD', 'KD', '8D', '2D', 'QC', '9C', '8C']
# Kontrak 3NT
# hand1 = ['AS', 'KS', '8S', 'AH', '6H', '4H', '10D', '9D', '4D', 'JC', '10C', '7C', '6C']
# hand2 = ['8C', '5H', '2S', '8H', '7H', '3H', 'AD', 'KD', '8D', '2D', 'AS', 'QC', '9C']
# Kontrak 4S
# hand1 = ['AS', 'KS', '8S', '6S', '5S', 'KH', 'QH', '10H', '10D', '9D', 'QC', '4C', '2C']
# hand2 = ['QS', 'JS', '10S', '6H', '5H', '4H', '3H', '2H', 'AD', 'KD', 'JD', 'JC', '10C']
# Kontrak 1S
# hand1 = ['2S', 'KS', '8S', '6S', '5S', 'KH', 'QH', '10H', '10D', '9D', 'QC', '4C', '2C']
# hand2 = ['QS', 'JS', '10S', '6H', '5H', '4H', '3H', '2H', 'AD', 'KD', 'JD', 'JC', '10C']

# === Fungsi HCP ===
def sum_hcp(hand1, hand2):
    hcp_values = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}
    return sum(hcp_values.get(card[0], 0) for card in hand1 + hand2)

# === Fungsi count suit ===
def count_suits(hand):
    suits = [card[-1] for card in hand]
    return Counter(suits)

# === Fungsi mencari fit suit (>= 8 kartu) ===
def find_fit_suit_from_two_hands(hand1, hand2):
    combined_hand = hand1 + hand2
    suit_counts = count_suits(combined_hand)
    fit_suits = [suit for suit, count in suit_counts.items() if count >= 8]
    return suit_counts, fit_suits

# === Fungsi pembobotan stoper (individual hand) ===
def suit_stopper_score_individual(hand, suit):
    cards_in_suit = [card for card in hand if card.endswith(suit)]
    ranks = [card[0] for card in cards_in_suit]
    count = len(cards_in_suit)

    score = 0
    if 'A' in ranks:
        score += 3
    elif 'K' in ranks and count >= 2:
        score += 2

    if 'Q' in ranks:
        if 'J' in ranks or count >= 3:
            score += 1.5
        else:
            score += 0.5

    if count >= 5 and not any(h in ranks for h in ['A', 'K', 'Q']):
        score += 0.5

    return round(score, 2)

# === Fungsi menentukan kontrak ===
def get_contract(hcp, fit_suits, x1, x2, y1, y2):
    major_fits = [s for s in fit_suits if s in ['S', 'H']]
    minor_fits = [s for s in fit_suits if s in ['C', 'D']]

    # 1. Prioritaskan Major jika ada fit
    if major_fits:
        strain = major_fits[0]
        level = 4 if hcp >= 25 else 1
    # 2. Jika tidak ada Major fit, coba NT jika ada stoper cukup
    elif x1 + x2 >= 2 and y1 + y2 >= 2:
        strain = 'NT'
        level = 3 if hcp >= 25 else 1
    # 3. Jika tidak bisa NT, cek minor fit
    elif minor_fits:
        strain = minor_fits[0]
        level = 5 if hcp >= 25 else 1
    else:
        strain = 'NT'
        level = 1

    return strain, level

# === Eksekusi ===
hcp = sum_hcp(hand1, hand2)
suit_counts, fit_suits = find_fit_suit_from_two_hands(hand1, hand2)
x1 = suit_stopper_score_individual(hand1, 'S')
x2 = suit_stopper_score_individual(hand2, 'S')
y1 = suit_stopper_score_individual(hand1, 'H')
y2 = suit_stopper_score_individual(hand2, 'H')
strain, level = get_contract(hcp, fit_suits, x1, x2, y1, y2)

x_total = x1 + x2
y_total = y1 + y2

# === Output ke terminal ===
print("Total HCP:", hcp)
print("Suit Counts Gabungan:", suit_counts)
print("Fit Suits (>=8 kartu):", fit_suits)
print(f"Stoper Spade Hand1 (x1): {x1}, Hand2 (x2): {x2}")
print(f"Stoper Heart Hand1 (y1): {y1}, Hand2 (y2): {y2}")
print(f"Rekomendasi Kontrak: {level}{strain}")

# === Visualisasi ===
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(7, 7))

colors = {
    'NT': '#4a90e2',
    'Minor': '#7ed957',
}

for x in range(5):
    for y in range(5):
        label = 'NT' if x >= 2 and y >= 2 else 'Minor'
        rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='gray',
                                 linestyle='--', facecolor=colors[label], alpha=0.8)
        ax.add_patch(rect)
        ax.text(x + 0.5, y + 0.5, label, ha='center', va='center', fontsize=9, color='black')

# Titik kombinasi
if strain not in ['S', 'H']:
    ax.plot(x_total, y_total, 'o', color='black', markersize=8, label='Titik Gabungan')
    ax.text(x_total + 0.1, y_total + 0.1, f'({x_total}, {y_total})', fontsize=9, fontweight='bold')

# Teks penjelas tambahan
info_text = (
    f"Total HCP: {hcp}\n"
    f"Fit Suits: {fit_suits}\n"
    f"x1: {x1}, x2: {x2} → x_total: {x_total}\n"
    f"y1: {y1}, y2: {y2} → y_total: {y_total}\n"
    f"Rekomendasi: {level}{strain}"
)
ax.text(5.2, 4.5, info_text, fontsize=9, va='top', bbox=dict(facecolor='white', edgecolor='black'))

ax.set_xlim(0, 7)
ax.set_ylim(0, 5.5)
ax.set_xticks(range(6))
ax.set_yticks(range(6))
ax.set_xticks([i + 0.5 for i in range(5)], minor=True)
ax.set_yticks([i + 0.5 for i in range(5)], minor=True)
ax.grid(which='minor', linestyle='--', color='gray', linewidth=0.5)
ax.set_xlabel('x_total (Spade stopper)')
ax.set_ylabel('y_total (Heart stopper)')
ax.set_title('Visualisasi Area Kontrak dan Posisi Stoper')

plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.show()
