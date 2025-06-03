from collections import Counter

def is_balanced_distribution(dist):
    balance_patterns = [
        [4, 4, 3, 2],
        [4, 3, 3, 3],
        [5, 3, 3, 2]
    ]
    dist_counter = Counter(dist)
    for pattern in balance_patterns:
        if Counter(pattern) == dist_counter:
            return True
    return False

def openingBridgeHand(hand):
    # Deck of Card
    ranks = []
    suits = []

    # Opening in Bridge
    possibleBids = []

    # Define HCP values for each rank
    hcp_values = {"A": 4, "K": 3, "Q": 2, "J": 1}

    # Create Deck of Card and calculate HCP
    total_hcp = 0

    # Initialize suit counts
    suit_counts = {"S": 0, "H": 0, "D": 0, "C": 0}  

    # Separate rank and suit
    for card in hand:
        if len(card) == 2:
            rank = card[0]
            suit = card[1]
        else:
            rank = card[0:2]
            suit = card[2]
        
        ranks.append(rank)
        suits.append(suit)
        
        # Calculate HCP for the current card and add to the total
        hcp = hcp_values.get(rank, 0)
        total_hcp += hcp
        
        # Increment the suit count for the current suit
        if suit in suit_counts:
            suit_counts[suit] += 1
        
    # Create shdc list (S, H, D, C)
    shdc = [suit_counts["S"], suit_counts["H"], suit_counts["D"], suit_counts["C"]] # 3433
    dist = sorted(shdc, reverse=True) # 4333

    # function no five card major suit
    def no_five_card_major(suit_counts):
        return suit_counts["S"] < 5 and suit_counts["H"] < 5
    
    # Determine the contract based on HCP and suit counts
    # 1NT
    if 15 <= total_hcp <= 17 and is_balanced_distribution(dist) and no_five_card_major(suit_counts):
        possibleBids.append(5)
    # 1C and 2D
    if total_hcp >= 16:
        if 22 <= total_hcp <=23 and is_balanced_distribution(dist):
            possibleBids.append(7)
        else:
            possibleBids.append(1)
    # 1D, 1H, 1S, 2C
    if 11 <= total_hcp <= 15:
        if suit_counts["S"] >= 5:
            possibleBids.append(4)
        elif suit_counts["H"] >= 5:
            possibleBids.append(3)
        elif suit_counts["C"] >= 6 or (suit_counts["C"] == 5 and (suit_counts["S"] == 4 or suit_counts["H"] == 4)):
            possibleBids.append(6)
        else:
            possibleBids.append(2)
    # 2D, 2H, 2S, 2NT, 3C, 3D, 3H, 3S
    if 6 <= total_hcp <= 10:
        if suit_counts["S"] == 6 or suit_counts["H"] == 6:
            possibleBids.append(7)
        elif suit_counts["H"] >= 5 and (suit_counts["D"] >= 5 or suit_counts["C"] >= 5):
            possibleBids.append(8)
        elif suit_counts["S"] >= 5 and (suit_counts["H"] >= 5 or suit_counts["D"] >= 5 or suit_counts["C"] >= 5):
            possibleBids.append(9)
        elif suit_counts["D"] >= 5 and suit_counts["C"] >= 5:
            possibleBids.append(10)
        elif suit_counts["C"] >= 7:
            possibleBids.append(11)
        elif suit_counts["D"] >= 7:
            possibleBids.append(12)
        elif suit_counts["H"] >= 7:
            possibleBids.append(13)
        elif suit_counts["S"] >= 7:
            possibleBids.append(14)
    # pass
    if not possibleBids:
        possibleBids.append(0)
        
    # Dictionary Opening in Bridge
    bridgeHandOpenings = {1:"Opening 1C", 2:"Opening 1D", 3:"Opening 1H", 4:"Opening 1S", 
                          5:"Opening 1NT", 6:"Opening 2C", 7:"Opening 2D", 8:"Opening 2H", 
                          9:"Opening 2S", 10:"Opening 2NT", 11:"Opening 3C", 12:"Opening 3D",
                            13:"Opening 3H", 14:"Opening 3S", 0:"Pass"}

    # Output
    output = bridgeHandOpenings[max(possibleBids)]
    # print("Hand's Card:", hand)
    print("HCP:", total_hcp)
    print("SHDC:", shdc)
    print(output)
    return output

if __name__ == "__main__":
    print("----------")
    openingBridgeHand(["QH","QC","10S","9C","AD","10S","AC",
                       "KS","AH","8C","7C","5H","AS"]) # 1C
    print("----------")
    openingBridgeHand(["QH","KH","10C","QC","10D","7D","9H",
                       "KS","KC","AH","JS","6D","10S"]) # 1NT
    print("----------")
    openingBridgeHand(["QH","KH","10C","JC","10D","7D","9H",
                       "KS","5C","AH","JS","6D","10S"]) # 1D
    print("----------")
    openingBridgeHand(["QH","KH","10C","JC","6H","7D","9H",
                       "KS","5C","AH","JS","6D","10S"]) # 1H
    print("----------")
    openingBridgeHand(["QH","KH","10C","JC","6H","7D","9H",
                       "KS","5C","AH","QS","6D","10S"]) # 1H
    print("----------")
    openingBridgeHand(["QS","KS","10C","JC","6S","7D","9S",
                       "KH","5C","AS","JH","6D","10H"]) # 1S
    print("----------")
    openingBridgeHand(["QS","KS","10C","JC","6S","7D","9S",
                       "KH","5C","AS","QH","6D","10H"]) # 1S
    print("----- -----")
    openingBridgeHand(["QH","KH","10C","QC","10D","7D","9H",
                       "KS","5C","AH","JS","6D","10S"]) # 1NT
    print("----------")
    openingBridgeHand(["QH","KH","10C","JC","10D","8C","9H",
                       "KS","5C","AH","JS","7C","9C"]) # 2C
    print("----------")
    openingBridgeHand(["QH","KH","10C","JC","10D","8C","9D",
                       "KS","5C","AH","JS","7C","7D"]) # 2C
    print("----------")
    openingBridgeHand(["QS","KS","10C","JC","10D","8C","9S",
                       "KH","5C","AS","JH","7C","7D"]) # 2C
    print("----------")
    openingBridgeHand(["QH","QC","10S","9C","AD","10D","AC",
                       "KS","AH","8C","7C","5H","AS"]) # 2D
    print("----------")
    openingBridgeHand(["4H","7C","JH","8H","4S","AD","5H",
                       "9C","6H","AC","7D","3D","10H"]) # 2D
    print("----------")
    openingBridgeHand(["4S","7C","JS","8S","4H","AD","5S",
                       "9C","6S","AC","7D","3D","10S"]) # 2D
    print("----------")
    openingBridgeHand(["4H","8D","JH","8H","4S","AD","5H",
                       "9D","5S","AC","7D","3D","10H"]) # 2H
    print("----------")
    openingBridgeHand(["4S","8D","JS","8S","4H","AD","5S",
                       "9D","5H","AC","7D","3D","10S"]) # 2S
    print("----- -----")
    openingBridgeHand(["4C","8D","JC","8C","4H","AD","5C",
                       "9D","5H","AS","7D","3D","10C"]) # 2NT
    print("----------")
    openingBridgeHand(["4C","8C","JC","2C","4H","AC","5C",
                       "9D","5H","AS","7D","3D","10C"]) # 3C
    print("----------")
    openingBridgeHand(["4D","8D","JD","2D","4H","AD","5D",
                       "9C","5H","AS","7C","3C","10D"]) # 3D
    print("----------")
    openingBridgeHand(["4H","8H","JH","2H","4D","AH","5H",
                       "9C","5D","AS","7C","3C","10H"]) # 3H
    print("----------")
    openingBridgeHand(["4S","8S","JS","2S","4H","AS","5S",
                       "9C","5H","AD","7C","3C","10S"]) # 3S
    print("----------")
    openingBridgeHand(["4D","8D","JD","2D","4H","AD","5D",
                       "9C","5H","AS","7C","3C","10S"]) # pass
    print("----------")
    openingBridgeHand(["JH", "10S", "AH", "6D", "4H", "10H",
                    "9C", "10D", "6H", "8H", "KH", "AS", "6S"]) # 1H
