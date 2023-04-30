def findPokerHand(hand):
    ranks = []
    suits = []
    possibleRank= []


    for  card in hand:
        if len(card)== 2:
            rank = card[0]
            suit = card[1]

        else:
            rank = card[0:2]
            suit = card[2]

        if rank== 'A':
            rank = 14
        elif rank == 'K':
            rank = 13
        elif rank == 'Q':
            rank = 12
        elif rank == 'J':
            rank = 11

        #changing to int for assigning to sorted function
        ranks.append(int(rank))
        suits.append(suit)
    sortedRanks = sorted(ranks)

    #print(f"Ranks are  {ranks}.")
    #print(f"Suits are {suits}.")
    #print(sortedRanks)

    #Royal Flush and Straight Flush and Flush
    if(suits.count(suits[0] )== 5): # check fpr flash
        if 14 in sortedRanks and 13 in sortedRanks and 12 in sortedRanks and 11 in sortedRanks and 10 in sortedRanks:
            possibleRank.append(10)
        else:
               possibleRank.append(6)
    #Straight
    elif all(sortedRanks[i]== sortedRanks[i-1]+1 for i in range(1,len(sortedRanks))):
        possibleRank.append(5)

    handUniqueVal = list(set(sortedRanks))
    #print(f"handUniqueVal is {handUniqueVal}")

    #Four of a kind
    # 33335 -- set 3 5 -- Four of a kind
    # 33355  -- set 3 5 -- Full house
    if len(handUniqueVal)== 2:
        for val in handUniqueVal:
            if sortedRanks.count(val)==4:
                possibleRank.append(8)
            if sortedRanks.count(val)==3:
                possibleRank.append(7)
    # 55534 -- set 3 5 4 -- three of a kind
    # 88772 -- set 8 7 2 -- two pair
    if len(handUniqueVal)==3:
        for val in handUniqueVal:
            if sortedRanks.count(val)== 3:
                possibleRank.append(4)
            elif sortedRanks.count(val) == 2:
                possibleRank.append(3)

    # Pair
    if len(handUniqueVal)==4:
        possibleRank.append(2)

    if not possibleRank:
            possibleRank.append(1)

    #print(possibleRank)
    pokerHandRanks = {10:"Royal Flush",9 :"Straight Flush",8 : "Four of a Kind ",7: "Full House",6: "Flush", 5 : "Straight ",
                      4 : "Three of a Kind",3 : " Two Pair",2 : "Pair ",1:"High Card"}

    output =  pokerHandRanks[max(possibleRank)]
    print(hand,output)
    return output



if __name__ == "__main__":
    findPokerHand(["KH", "AH", "QH", "JH", "10H"])  # Royal Flush
    findPokerHand(["QC", "JC", "10C", "9C", "8C"])  # Straight Flush
    findPokerHand(["5C", "5S", "5H", "5D", "QH"])  # Four of a Kind
    findPokerHand(["2H", "2D", "2S", "10H", "10C"])  # Full House
    findPokerHand(["2D", "KD", "7D", "6D", "5D"])  # Flush
    findPokerHand(["JC", "10H", "9C", "8C", "7D"])  # Straight
    findPokerHand(["10H", "10C", "10D", "2D", "5S"])  # Three of a Kind
    findPokerHand(["KD", "KH", "5C", "5S", "6D"])  # Two Pair
    findPokerHand(["2D", "2S", "9C", "KD", "10C"])  # Pair
    findPokerHand(["KD", "5H", "2D", "10C", "JH"])  # High Card


