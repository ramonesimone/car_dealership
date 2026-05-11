"""
Synthetic Car Dealership Data Generator
Generates realistic, relational datasets for AI/ML demo projects.
"""

import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUTPUT_DIR = Path(__file__).parent / "data"

# ── Real-world car data ──────────────────────────────────────────────

MAKES_MODELS = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Tacoma", "Tundra", "Sienna", "4Runner"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "HR-V", "Odyssey"],
    "Ford": ["F-150", "Mustang", "Explorer", "Escape", "Bronco", "Edge", "Ranger"],
    "Chevrolet": ["Silverado", "Equinox", "Tahoe", "Suburban", "Malibu", "Traverse", "Camaro"],
    "BMW": ["3 Series", "5 Series", "X3", "X5", "M4", "7 Series"],
    "Mercedes": ["C-Class", "E-Class", "GLC", "GLE", "S-Class", "A-Class"],
    "Tesla": ["Model 3", "Model Y", "Model S", "Model X", "Cybertruck"],
    "Nissan": ["Altima", "Rogue", "Sentra", "Pathfinder", "Frontier"],
    "Hyundai": ["Elantra", "Tucson", "Santa Fe", "Sonata", "Palisade"],
    "Kia": ["Telluride", "Sorento", "Sportage", "Forte", "EV6"],
    "Subaru": ["Outback", "Forester", "Crosstrek", "Impreza", "Ascent"],
    "Volkswagen": ["Jetta", "Tiguan", "Atlas", "ID.4", "Golf GTI"],
}

COLORS = ["White", "Black", "Silver", "Gray", "Blue", "Red", "Green", "Beige", "Brown", "Navy"]

TRANSMISSIONS = ["Automatic", "CVT", "DCT", "Manual"]
FUEL_TYPES = ["Gasoline", "Hybrid", "Electric", "Diesel", "Plug-in Hybrid"]

CONDITIONS = ["New", "Certified Pre-Owned", "Used"]
VEHICLE_STATUS = ["Available", "Sold", "In Transit", "In Service", "Reserved"]

DEALERSHIPS = [
    {"name": "AutoMax Premier", "city": "Los Angeles", "state": "CA", "phone": "310-555-0101"},
    {"name": "City Motors", "city": "New York", "state": "NY", "phone": "212-555-0202"},
    {"name": "Lone Star Auto", "city": "Houston", "state": "TX", "phone": "713-555-0303"},
    {"name": "Windy City Cars", "city": "Chicago", "state": "IL", "phone": "312-555-0404"},
    {"name": "Sunshine Autos", "city": "Miami", "state": "FL", "phone": "305-555-0505"},
    {"name": "Pacific Motors", "city": "Seattle", "state": "WA", "phone": "206-555-0606"},
    {"name": "Peach State Cars", "city": "Atlanta", "state": "GA", "phone": "404-555-0707"},
    {"name": "Desert Auto Group", "city": "Phoenix", "state": "AZ", "phone": "602-555-0808"},
    {"name": "Rocky Mountain Auto", "city": "Denver", "state": "CO", "phone": "303-555-0909"},
    {"name": "Motor City Elite", "city": "Detroit", "state": "MI", "phone": "313-555-1010"},
]

FIRST_NAMES = [
    "James", "Maria", "Robert", "Jennifer", "Michael", "Linda", "David", "Patricia",
    "William", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah",
    "Christopher", "Karen", "Charles", "Lisa", "Daniel", "Nancy", "Matthew", "Betty",
    "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley", "Steven", "Dorothy",
    "Paul", "Kimberly", "Andrew", "Emily", "Joshua", "Donna", "Kenneth", "Michelle",
    "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", "Timothy", "Deborah",
    "Ronald", "Stephanie", "Jason", "Rebecca", "Jeffrey", "Sharon", "Ryan", "Laura",
    "Jacob", "Cynthia", "Gary", "Kathleen", "Nicholas", "Amy", "Eric", "Angela",
    "Jonathan", "Helen", "Stephen", "Anna", "Larry", "Brenda", "Justin", "Pamela",
    "Scott", "Nicole", "Brandon", "Samantha", "Benjamin", "Katherine", "Samuel", "Emma",
    "Raymond", "Christine", "Gregory", "Debra", "Frank", "Rachel", "Alexander", "Carolyn",
    "Patrick", "Janet", "Jack", "Catherine", "Dennis", "Olivia", "Jerry", "Heather",
    "Tyler", "Diane", "Aaron", "Julie", "Jose", "Joyce", "Nathan", "Victoria",
    "Henry", "Kelly", "Douglas", "Lauren", "Adam", "Christina", "Peter", "Joan",
    "Zachary", "Evelyn", "Walter", "Abigail", "Harold", "Andrea", "Jeremy", "Cheryl",
    "Chad", "Megan", "Dylan", "Martha", "Kyle", "Brittany", "Arthur", "Rose",
    "Bruce", "Lori", "Ethan", "Jacqueline", "Carl", "Frances", "Luis", "Doris",
    "Juan", "Alice", "Albert", "Judith", "Gerald", "Julia", "Billy", "Grace",
    "Bryan", "Ann", "Roy", "Jean", "Logan", "Ruth", "Jordan", "Kathryn",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz",
    "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales",
    "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson",
    "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward",
    "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray",
    "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel",
    "Myers", "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry",
    "Russell", "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes", "Coleman",
]

SERVICE_TYPES = [
    "Oil Change", "Tire Rotation", "Brake Inspection", "Engine Diagnostic",
    "Transmission Service", "AC Repair", "Battery Replacement", "Wheel Alignment",
    "Car Wash & Detail", "Timing Belt Replacement", "Spark Plug Replacement",
    "Coolant Flush", "Air Filter Replacement", "Windshield Replacement",
    "Suspension Repair", "Exhaust System Repair", "Software Update",
]

SERVICE_NOTES = {
    "Oil Change": "Performed full synthetic oil change. Topped off fluids. No leaks detected.",
    "Tire Rotation": "Rotated all 4 tires. Pressure adjusted to spec. Tread depth measured within acceptable range.",
    "Brake Inspection": "Inspected brake pads and rotors. Front pads at 6mm, rear at 5mm. Recommended replacement within 3 months.",
    "Engine Diagnostic": "Connected OBD-II scanner. Code P0420 detected. Catalytic converter efficiency below threshold.",
    "Transmission Service": "Drained and replaced transmission fluid. New filter installed. Shifts smooth on test drive.",
    "AC Repair": "Recharged AC refrigerant. System holding pressure. Outlet temp measured at 42F.",
    "Battery Replacement": "Tested battery: 540 CCA (rated 650). Replaced with OEM battery. Tested charging system: 14.2V.",
    "Wheel Alignment": "Front toe out of spec by 0.15 degrees. Adjusted both front wheels. Camber within spec.",
    "Car Wash & Detail": "Exterior wash, wax, interior vacuum, windows cleaned, dashboard conditioned.",
    "Timing Belt Replacement": "Replaced timing belt and tensioner. Water pump inspected and replaced as preventive measure.",
    "Spark Plug Replacement": "Replaced all spark plugs. Old plugs showed normal wear. Gap set to 0.044 inches.",
    "Coolant Flush": "Flushed cooling system. Replaced with OEM coolant 50/50 mix. No leaks after pressure test.",
    "Air Filter Replacement": "Replaced engine air filter and cabin air filter. Both were significantly dirty.",
    "Windshield Replacement": "Removed old windshield. Cleaned frame. Installed new OEM windshield with proper sealant.",
    "Suspension Repair": "Replaced front struts. Both were leaking oil. Performed alignment after replacement.",
    "Exhaust System Repair": "Welded repair on exhaust pipe. Replaced gasket at catalytic converter joint.",
    "Software Update": "Updated infotainment system firmware. Applied navigation map update. Cleared error codes.",
}

LEAD_SOURCES = [
    "Website", "Phone Inquiry", "Walk-in", "Referral", "Social Media",
    "Email Campaign", "Third-Party Site", "Trade Show", "Direct Mail",
    "Online Ad",
]

LEAD_STATUSES = ["New", "Contacted", "Qualified", "Test Drive", "Negotiation", "Closed Won", "Closed Lost"]


# ── Helpers ──────────────────────────────────────────────────────────

def gen_phone():
    return f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"

def gen_email(fname, lname):
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "proton.me", "icloud.com"]
    return f"{fname.lower()}.{lname.lower()}{random.randint(1, 99)}@{random.choice(domains)}"

def gen_price(base_min, base_max, condition):
    multiplier = {"New": 1.0, "Certified Pre-Owned": 0.78, "Used": 0.62}
    return round(random.uniform(base_min, base_max) * multiplier[condition], -2)

def gen_vin():
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    return "".join(random.choices(chars, k=17))

def gen_date(start_year=2018, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))


# ── Generators ───────────────────────────────────────────────────────

def generate_dealerships():
    rows = []
    for i, d in enumerate(DEALERSHIPS, 1):
        rows.append({
            "dealership_id": i,
            "name": d["name"],
            "city": d["city"],
            "state": d["state"],
            "phone": d["phone"],
            "email": f"info@{d['name'].lower().replace(' ', '')}.com",
            "established_year": random.randint(1985, 2020),
        })
    return rows


def generate_employees(dealerships, count=80):
    roles = [
        "Salesperson", "Salesperson", "Salesperson", "Sales Manager",
        "Finance Manager", "Service Advisor", "Service Technician",
        "Service Technician", "Detailer", "General Manager", "Receptionist",
    ]
    rows = []
    for i in range(1, count + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        dealership = random.choice(dealerships)
        role = random.choice(roles)
        start = gen_date(2019, 2025)
        base_salary = {
            "Salesperson": random.randint(35000, 55000),
            "Sales Manager": random.randint(65000, 95000),
            "Finance Manager": random.randint(60000, 85000),
            "Service Advisor": random.randint(40000, 60000),
            "Service Technician": random.randint(45000, 75000),
            "Detailer": random.randint(28000, 38000),
            "General Manager": random.randint(90000, 150000),
            "Receptionist": random.randint(28000, 35000),
        }.get(role, 40000)

        rows.append({
            "employee_id": i,
            "first_name": first,
            "last_name": last,
            "email": gen_email(first, last),
            "phone": gen_phone(),
            "role": role,
            "dealership_id": dealership["dealership_id"],
            "hire_date": start.strftime("%Y-%m-%d"),
            "base_salary": base_salary,
            "is_active": random.random() < 0.92,
        })
    return rows


def generate_customers(dealerships, count=2000):
    rows = []
    for i in range(1, count + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        dealership = random.choice(dealerships)
        reg_date = gen_date(2019, 2026)
        rows.append({
            "customer_id": i,
            "first_name": first,
            "last_name": last,
            "email": gen_email(first, last),
            "phone": gen_phone(),
            "city": random.choice([d["city"] for d in DEALERSHIPS] + ["Other"]),
            "state": random.choice([d["state"] for d in DEALERSHIPS] + ["TX", "CA", "NY", "FL", "IL"]),
            "preferred_dealership_id": dealership["dealership_id"],
            "registration_date": reg_date.strftime("%Y-%m-%d"),
            "is_returning": random.random() < 0.35,
        })
    return rows


def generate_vehicles(dealerships, count=500):
    rows = []
    for i in range(1, count + 1):
        make = random.choice(list(MAKES_MODELS.keys()))
        model = random.choice(MAKES_MODELS[make])
        year = random.randint(2018, 2026)
        condition = random.choices(CONDITIONS, weights=[0.25, 0.15, 0.60])[0]
        mileage = 0 if condition == "New" else random.randint(5000, 90000)
        base_price_map = {
            "Toyota": (25000, 55000), "Honda": (24000, 50000),
            "Ford": (28000, 70000), "Chevrolet": (25000, 65000),
            "BMW": (42000, 120000), "Mercedes": (45000, 130000),
            "Tesla": (40000, 100000), "Nissan": (22000, 48000),
            "Hyundai": (22000, 50000), "Kia": (22000, 55000),
            "Subaru": (26000, 45000), "Volkswagen": (23000, 45000),
        }
        price_range = base_price_map.get(make, (25000, 50000))
        price = gen_price(price_range[0], price_range[1], condition)
        # Adjust price down by age
        age_factor = max(0.5, 1.0 - (2026 - year) * 0.04)
        price = round(price * age_factor, -2)

        dealership = random.choice(dealerships)
        status = random.choices(VEHICLE_STATUS, weights=[0.30, 0.45, 0.08, 0.07, 0.10])[0]
        listed = gen_date(2024, 2026)

        rows.append({
            "vehicle_id": i,
            "vin": gen_vin(),
            "make": make,
            "model": model,
            "year": year,
            "condition": condition,
            "mileage": mileage,
            "color": random.choice(COLORS),
            "transmission": random.choice(TRANSMISSIONS),
            "fuel_type": random.choice(FUEL_TYPES),
            "engine": f"{random.choice(['1.5L', '2.0L', '2.5L', '3.0L', '3.5L', '5.0L', '6.2L'])} {random.choice(['I4', 'V6', 'V8', 'I6', 'Electric'])}",
            "doors": random.choice([2, 4, 4, 4, 4]),
            "seats": random.choice([5, 5, 5, 5, 7, 7, 8]),
            "price": price,
            "msrp": round(price * random.uniform(1.05, 1.20), -2),
            "dealership_id": dealership["dealership_id"],
            "status": status,
            "date_listed": listed.strftime("%Y-%m-%d"),
            "description": f"{year} {make} {model} - {condition.lower().replace('certified pre-owned', 'CPO')}, {mileage:,} miles, {random.choice(COLORS).lower()} exterior.",
        })
    return rows


def generate_sales(customers, vehicles, employees, count=1500):
    sold_vehicles = [v for v in vehicles if v["status"] == "Sold"]
    available_customers = customers[:]
    rows = []
    for i in range(1, min(count, len(sold_vehicles)) + 1):
        vehicle = random.choice(sold_vehicles)
        customer = random.choice(available_customers)
        # Prefer a mix of salespeople
        sales_employees = [e for e in employees if "Sales" in e["role"] or "Manager" in e["role"]]
        salesperson = random.choice(sales_employees) if sales_employees else random.choice(employees)

        sale_date = gen_date(2020, 2026)
        discount = random.choices([0, random.randint(500, 5000)], weights=[0.4, 0.6])[0]
        if isinstance(discount, int) and discount > vehicle["price"] * 0.15:
            discount = round(vehicle["price"] * 0.10, -2)

        final_price = vehicle["price"] - (discount if isinstance(discount, (int, float)) else 0)
        if final_price < 1000:
            final_price = vehicle["price"]

        rows.append({
            "sale_id": i,
            "customer_id": customer["customer_id"],
            "vehicle_id": vehicle["vehicle_id"],
            "employee_id": salesperson["employee_id"],
            "dealership_id": vehicle["dealership_id"],
            "sale_date": sale_date.strftime("%Y-%m-%d"),
            "sale_price": final_price,
            "discount": discount if isinstance(discount, (int, float)) else 0,
            "payment_method": random.choices(["Cash", "Finance", "Lease"], weights=[0.20, 0.55, 0.25])[0],
            "trade_in": random.random() < 0.30,
            "warranty_purchased": random.random() < 0.45,
        })
    return rows


def generate_service_records(customers, vehicles, employees, count=3000):
    service_employees = [e for e in employees if "Service" in e["role"] or "Technician" in e["role"]]
    if not service_employees:
        service_employees = employees
    rows = []
    for i in range(1, count + 1):
        vehicle = random.choice(vehicles)
        customer = random.choice(customers)
        tech = random.choice(service_employees)
        service_type = random.choice(SERVICE_TYPES)
        service_date = gen_date(2021, 2026)
        cost_map = {
            "Oil Change": (40, 80), "Tire Rotation": (30, 60),
            "Brake Inspection": (50, 100), "Engine Diagnostic": (100, 200),
            "Transmission Service": (200, 400), "AC Repair": (150, 500),
            "Battery Replacement": (150, 300), "Wheel Alignment": (80, 150),
            "Car Wash & Detail": (50, 200), "Timing Belt Replacement": (500, 1200),
            "Spark Plug Replacement": (150, 400), "Coolant Flush": (100, 200),
            "Air Filter Replacement": (40, 100), "Windshield Replacement": (250, 600),
            "Suspension Repair": (400, 1500), "Exhaust System Repair": (200, 800),
            "Software Update": (50, 150),
        }
        cost_range = cost_map.get(service_type, (50, 200))
        cost = round(random.uniform(cost_range[0], cost_range[1]), 2)
        labor_hours = round(random.uniform(0.5, 4.0), 1)

        rows.append({
            "service_id": i,
            "customer_id": customer["customer_id"],
            "vehicle_id": vehicle["vehicle_id"],
            "employee_id": tech["employee_id"],
            "dealership_id": vehicle["dealership_id"],
            "service_date": service_date.strftime("%Y-%m-%d"),
            "service_type": service_type,
            "description": SERVICE_NOTES.get(service_type, "Routine service performed."),
            "cost": cost,
            "labor_hours": labor_hours,
            "odometer": random.randint(5000, 120000),
            "customer_rating": random.choices([1, 2, 3, 4, 4, 5, 5, 5], weights=[1, 1, 3, 6, 8, 10, 12, 8])[0],
        })
    return rows


def generate_leads(customers, dealerships, count=1000):
    rows = []
    for i in range(1, count + 1):
        customer = random.choice(customers)
        dealership = random.choice(dealerships)
        make = random.choice(list(MAKES_MODELS.keys()))
        model = random.choice(MAKES_MODELS[make])
        created = gen_date(2023, 2026)
        status = random.choices(LEAD_STATUSES, weights=[0.10, 0.15, 0.15, 0.20, 0.15, 0.15, 0.10])[0]
        closed = None
        if status in ("Closed Won", "Closed Lost"):
            closed = created + timedelta(days=random.randint(1, 90))

        rows.append({
            "lead_id": i,
            "customer_id": customer["customer_id"],
            "dealership_id": dealership["dealership_id"],
            "vehicle_make": make,
            "vehicle_model": model,
            "source": random.choice(LEAD_SOURCES),
            "status": status,
            "date_created": created.strftime("%Y-%m-%d"),
            "date_closed": closed.strftime("%Y-%m-%d") if closed else None,
            "notes": f"Customer interested in {make} {model}. Initial contact via {random.choice(LEAD_SOURCES).lower()}.",
            "budget_range": f"${random.randint(15000, 35000):,} - ${random.randint(35001, 80000):,}",
        })
    return rows


# ── CSV Writer ───────────────────────────────────────────────────────

def write_csv(filename, fieldnames, rows):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})
    print(f"  ✓ {filename} ({len(rows)} rows)")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    print("Generating synthetic car dealership data...\n")

    print("1/6  Dealerships")
    dealerships = generate_dealerships()
    write_csv("dealerships.csv", [
        "dealership_id", "name", "city", "state", "phone", "email", "established_year",
    ], dealerships)

    print("2/6  Employees")
    employees = generate_employees(dealerships)
    write_csv("employees.csv", [
        "employee_id", "first_name", "last_name", "email", "phone",
        "role", "dealership_id", "hire_date", "base_salary", "is_active",
    ], employees)

    print("3/6  Customers")
    customers = generate_customers(dealerships)
    write_csv("customers.csv", [
        "customer_id", "first_name", "last_name", "email", "phone",
        "city", "state", "preferred_dealership_id", "registration_date", "is_returning",
    ], customers)

    print("4/6  Vehicles")
    vehicles = generate_vehicles(dealerships)
    write_csv("vehicles.csv", [
        "vehicle_id", "vin", "make", "model", "year", "condition", "mileage",
        "color", "transmission", "fuel_type", "engine", "doors", "seats",
        "price", "msrp", "dealership_id", "status", "date_listed", "description",
    ], vehicles)

    print("5/6  Sales")
    sales = generate_sales(customers, vehicles, employees)
    write_csv("sales.csv", [
        "sale_id", "customer_id", "vehicle_id", "employee_id", "dealership_id",
        "sale_date", "sale_price", "discount", "payment_method", "trade_in", "warranty_purchased",
    ], sales)

    print("6/6  Service Records & Leads")
    services = generate_service_records(customers, vehicles, employees)
    write_csv("service_records.csv", [
        "service_id", "customer_id", "vehicle_id", "employee_id", "dealership_id",
        "service_date", "service_type", "description", "cost", "labor_hours",
        "odometer", "customer_rating",
    ], services)

    leads = generate_leads(customers, dealerships)
    write_csv("leads.csv", [
        "lead_id", "customer_id", "dealership_id", "vehicle_make", "vehicle_model",
        "source", "status", "date_created", "date_closed", "notes", "budget_range",
    ], leads)

    print(f"\n{'='*50}")
    print(f"All files written to: {OUTPUT_DIR}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
