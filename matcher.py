import re


def norm_plate(plate):
    return re.sub(r'[\s.\-]', '', (plate or '')).upper()


def match_invoices(deliveries, invoices):
    """Match VAT invoices to deliveries. Returns (matches, unmatched).
    matches: dict of delivery_id -> list of invoice_ids
    unmatched: list of invoice_ids with no delivery match
    """
    # Index: normalized plate -> list of deliveries
    plate_index = {}
    for d in deliveries:
        truck = (d.get('computed_data') or {}).get('truck')
        if truck:
            plate_index.setdefault(norm_plate(truck['plate']), []).append(d)

    matches = {}
    unmatched = []

    for inv in invoices:
        plate = norm_plate(inv.get('truck_plate'))
        candidates = plate_index.get(plate)

        if not candidates:
            unmatched.append(inv['id'])
            continue

        if len(candidates) == 1:
            match = candidates[0]
        else:
            # Disambiguate by dropoff_location_id
            by_loc = [d for d in candidates if d['dropoff_location_id'] == inv.get('dropoff_location_id')]
            match = by_loc[0] if len(by_loc) == 1 else None

        if match:
            matches.setdefault(match['id'], []).append(inv['id'])
        else:
            unmatched.append(inv['id'])

    return matches, unmatched
