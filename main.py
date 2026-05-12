import json
from matcher import match_invoices

with open('20250901.json') as f:
    data = json.load(f)['data']

matches, unmatched = match_invoices(data['deliveries'], data['vat_invoices'])

for del_id, inv_ids in sorted(matches.items()):
    print(f"Delivery {del_id}: {len(inv_ids)} invoices -> {inv_ids}")

print(f"\nMatched: {sum(len(v) for v in matches.values())} invoices across {len(matches)} deliveries")
print(f"Unmatched: {len(unmatched)}/{len(data['vat_invoices'])}")
