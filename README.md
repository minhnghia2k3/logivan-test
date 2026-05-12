    Attached is a JSON file containing deliveries and VAT invoices.
    The task is simple: write code to match the VAT invoices to deliveries.
    There are many more VAT invoices than deliveries; most invoices don't match any of the included deliveries.
    An important aspect of this problem is a low token budget.
    Please try to explore the data and determine: where (if at all) do we need to use LLMs?

# Answer

## 1. Based on my analysis of the data:

No LLM is needed for this dataset. The matching is fully deterministic:

1. Normalize truck plate (strip -, ., spaces) → match invoice `truck_plate` to delivery `computed_data.truck.plate`
2. Use `dropoff_location_id` to disambiguate when the same plate serves multiple deliveries

Output:
```
✗ python3 main.py
Delivery 72206: 1 invoices -> [35053219]
Delivery 72207: 1 invoices -> [35053243]
Delivery 72208: 1 invoices -> [35053245]
Delivery 72209: 3 invoices -> [35053068, 35053070, 35053078]
Delivery 72210: 1 invoices -> [35053156]
Delivery 72211: 4 invoices -> [35053170, 35053172, 35053173, 35053177]
Delivery 72212: 5 invoices -> [35052984, 35052986, 35052988, 35052990, 35052992]
Delivery 72213: 2 invoices -> [35052963, 35052966]
Delivery 72214: 1 invoices -> [35052815]
Delivery 72215: 1 invoices -> [35052755]
```

**Result**: 20/680 invoices match the 10 deliveries. The other 660 are for trucks not in the delivery set.

=> Token budget strategy: Run deterministic rules first (zero cost), only send failures to an LLM.