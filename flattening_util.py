# flattens a list and returns sublist lengths
def flatten(original):
    flattened = []
    lengths = []

    for sublist in original:
        lengths.append(len(sublist))
        flattened.extend(sublist)

    return flattened, lengths
    
# iteratively unflattens a flattened list
# using length data produced by flatten method
def unflatten(flattened, lengths):
    unflattened = []

    for length in lengths:
        
        # partitions off next chunk
        sublist = flattened[:length]
        unflattened.append(sublist)
        flattened = flattened[length:]

    # checks that we've used everything
    assert(not flattened)

    return unflattened
