
def all_same_or_all_diff (attr1, attr2, attr3):
    if attr1 == attr2 == attr3:
        return True
    elif (attr1 != attr2) and (attr2 != attr3) and (attr3 != attr1):
        return True
    else:
        return False


def checkSet(card1, card2, card3):
    color_check = all_same_or_all_diff (card1.color, card2.color, card3.color)
    shape_check = all_same_or_all_diff (card1.shape, card2.shape, card3.shape)
    num_check = all_same_or_all_diff (card1.num, card2.num, card3.num)
    shade_check = all_same_or_all_diff (card1.shade, card2.shade, card3.shade)
    return color_check and shape_check and num_check and shade_check


def find_first_set(table_cards):
    for card1 in table_cards:
        for card2 in table_cards:
            for card3 in table_cards:
                if card1 != card2 and card2 != card3 and card1 != card3:
                    if isSet.checkSet(card1, card2, card3):
                        return [card1, card2, card3]
