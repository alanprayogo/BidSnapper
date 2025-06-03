from collections import Counter

def sum_hcp(hand1, hand2):
    hcp_values = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}
    return sum(hcp_values.get(card[0], 0) for card in hand1 + hand2)

def count_suits(hand):
    suits = [card[-1] for card in hand]
    return Counter(suits)

def find_fit_suit_from_two_hands(hand1, hand2):
    combined_hand = hand1 + hand2
    suit_counts = count_suits(combined_hand)
    fit_suits = [suit for suit, count in suit_counts.items() if count >= 8]
    return suit_counts, fit_suits

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

def get_contract(hcp, fit_suits, x1, x2, y1, y2):
    major_fits = [s for s in fit_suits if s in ['S', 'H']]
    minor_fits = [s for s in fit_suits if s in ['C', 'D']]

    if major_fits:
        strain = major_fits[0]
        level = 4 if hcp >= 25 else 1
    elif x1 + x2 >= 2 and y1 + y2 >= 2:
        strain = 'NT'
        level = 3 if hcp >= 25 else 1
    elif minor_fits:
        strain = minor_fits[0]
        level = 5 if hcp >= 25 else 1
    else:
        strain = 'NT'
        level = 1

    return strain, level

def analyze_combined_hand(hand1, hand2):
    hcp = sum_hcp(hand1, hand2)
    suit_counts, fit_suits = find_fit_suit_from_two_hands(hand1, hand2)
    x1 = suit_stopper_score_individual(hand1, 'S')
    x2 = suit_stopper_score_individual(hand2, 'S')
    y1 = suit_stopper_score_individual(hand1, 'H')
    y2 = suit_stopper_score_individual(hand2, 'H')
    strain, level = get_contract(hcp, fit_suits, x1, x2, y1, y2)
    return strain, level
