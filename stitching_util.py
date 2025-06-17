# unstitches an array into true and false subset
def unstitch(array, bools):
    trues = [item for item, bool_val in zip(array, bools) if bool_val]
    falses = [item for item, bool_val in zip(array, bools) if not bool_val]
    return trues, falses

def stitch(trues, falses, bools):
    array = []
    for b in bools:
        if b:
            array.append(trues.pop(0))
        else:
            array.append(falses.pop(0))

    # both trues and falses should be empty
    assert not trues
    assert not falses

    return array



