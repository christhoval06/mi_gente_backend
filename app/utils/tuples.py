def tuple_reducer(acc, el):
    (key, value) = el
    acc[key] = acc.get(key, 0) + value
    return acc