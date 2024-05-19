

def within_25_percent(y_true, y_pred):
    in_bounds_counter = 0

    total = len(y_true)

    for true, pred in zip(y_true, y_pred):
        if true == 0.0:
            total -= 1
            continue

        lower_bound = min(true * 0.75, true * 1.25)
        upper_bound = max(true * 0.75, true * 1.25)

        if lower_bound < pred < upper_bound:
            in_bounds_counter += 1

    if total == 0:
        return 0.0  # avoid division by zero

    return in_bounds_counter / total
