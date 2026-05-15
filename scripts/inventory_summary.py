import csv, json
from collections import Counter, defaultdict

vehicles = []
makes = Counter()
models_by_make = defaultdict(Counter)
price_brackets = Counter()
conditions = Counter()

with open('data/vehicles.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        vehicles.append(row)
        make = row['make']
        model = row['model']
        condition = row['condition']
        price = float(row['price'])
        makes[make] += 1
        models_by_make[make][model] += 1
        conditions[condition] += 1
        if price < 15000: price_brackets['Under $15K'] += 1
        elif price < 25000: price_brackets['$15K - $25K'] += 1
        elif price < 40000: price_brackets['$25K - $40K'] += 1
        elif price < 60000: price_brackets['$40K - $60K'] += 1
        else: price_brackets['$60K+'] += 1

summary = {
    'dealership': 'T&C AUTOS',
    'location': '4200 Stevens Creek Blvd, San Jose, CA 95129',
    'phone': '(408) 555-0120',
    'email': 'info@tcautos.com',
    'hours': {
        'monday_friday': '9:00 AM – 8:00 PM',
        'saturday': '9:00 AM – 7:00 PM',
        'sunday': '10:00 AM – 5:00 PM'
    },
    'total_vehicles': len(vehicles),
    'by_condition': dict(conditions),
    'by_make': {m: {'count': c, 'models': dict(models_by_make[m])} for m, c in makes.most_common()},
    'by_price_bracket': dict(price_brackets),
    'price_range': {
        'min': min(float(v['price']) for v in vehicles),
        'max': max(float(v['price']) for v in vehicles),
        'avg': round(sum(float(v['price']) for v in vehicles) / len(vehicles), 2)
    },
    'services': {
        'oil_change': 49.99,
        'tire_rotation': 39.99,
        'air_filter': 49.99,
        'coolant_flush': 119.99,
        'spark_plugs': 179.99,
        'timing_belt': 599.99,
        'engine_diagnostic': 129.99,
        'brake_service_per_axle': 199.99,
        'transmission_service': 249.99,
        'ac_service': 179.99,
        'battery': 169.99,
        'suspension': 449.99,
        'exhaust': 249.99,
        'windshield': 299.99,
        'alignment': 99.99,
        'car_wash': 59.99,
        'ecu_update': 79.99
    },
    'promotions': {
        'may_2026_sales_event': '0% APR for 60 months on select 2025-2026 models (720+ credit)',
        'trade_in_bonus': 'Extra $1,000 on trade-in value through May 31, 2026',
        'referral_program': '$500 gift card or service credit per referral',
        'college_graduate': '$500 bonus cash + 90 days no payment',
        'price_match': 'Match + extra $200 off',
        'oil_change_tire_bundle': '$79.99',
        'military_discount': '10% off parts and labor'
    },
    'financing': {
        'standard_rate': '3.99% – 7.99% APR',
        'standard_term': '24–72 months',
        'standard_credit': '680+',
        'first_time_buyer_rate': '5.99% – 9.99% APR',
        'first_time_buyer_term': '48–60 months',
        'college_graduate_rate': '4.49% – 7.49% APR',
        'military_rate': '3.49% – 6.99% APR',
        'credit_challenged_rate': '8.99% – 14.99% APR',
        'credit_challenged_minimum': '580',
        'gap_insurance': 799,
        'extended_warranty_powertrain': '5yr/60K miles, $100 deductible',
        'extended_warranty_platinum': '7yr/100K miles, $100 deductible',
        'extended_warranty_ultimate': '7yr/100K miles, $0 deductible'
    },
    'policies': {
        'exchange_policy': '7 days / 500 miles',
        'cancellation_policy': '3 business days (used only), $250 restocking fee',
        'new_warranty_bumper_to_bumper': '3 years / 36,000 miles',
        'new_warranty_powertrain': '5 years / 60,000 miles',
        'repair_warranty': '12 months / 12,000 miles',
        'price_match_radius': '100 miles'
    },
    'team': {
        'general_manager': 'James Carter (10 years)',
        'sales_manager': 'Linda Martinez (8 years)',
        'finance_manager': 'Robert Kim (6 years)',
        'service_manager': 'Sarah Patel (7 years)',
        'lead_technician': 'David Okafor (ASE Certified Master Technician)'
    }
}

with open('knowledge_base/08_inventory_summary.md', 'w', encoding='utf-8') as f:
    f.write("# Inventory Summary (as of May 2026)\n\n")
    f.write("## Overview\n")
    f.write(f"- **Total Vehicles:** {summary['total_vehicles']}\n")
    f.write(f"- **Price Range:** ${summary['price_range']['min']:,.0f} – ${summary['price_range']['max']:,.0f}\n")
    f.write(f"- **Average Price:** ${summary['price_range']['avg']:,.0f}\n\n")
    f.write("## By Condition\n")
    for cond, count in sorted(summary['by_condition'].items()):
        f.write(f"- **{cond}:** {count}\n")
    f.write("\n## By Price Range\n")
    for bracket, count in sorted(summary['by_price_bracket'].items()):
        f.write(f"- **{bracket}:** {count}\n")
    f.write("\n## Inventory by Make\n\n")
    for make, data in sorted(summary['by_make'].items()):
        f.write(f"### {make} ({data['count']} vehicles)\n")
        for model, mcount in sorted(data['models'].items()):
            f.write(f"- {model}: {mcount}\n")
        f.write("\n")

with open('app/facts.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print("Done. Created knowledge_base/08_inventory_summary.md and app/facts.json")
