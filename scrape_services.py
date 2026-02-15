import os
import csv
import re
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlencode
from bs4 import BeautifulSoup

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Zone țintă pentru scraping
SEARCH_AREAS = [
    # București + Ilfov (zona metropolitană)
    "București",
    "sector 1 București",
    "sector 2 București",
    "sector 3 București",
    "sector 4 București",
    "sector 5 București",
    "sector 6 București",
    "Ilfov",

    # Top orașe
    "Cluj-Napoca",
    "Timișoara",
    "Iași",
    "Constanța",
    "Craiova",
    "Brașov",
    "Galați",
    "Ploiești",
    "Oradea",
]

# Tipuri de căutări pentru a găsi mai multe service-uri relevante
SEARCH_KEYWORDS = [
    "service auto",
    "service multimarca",
    "diagnoză auto",
    "electrica auto",
    "vulcanizare auto",
    "tinichigerie auto",
]


def build_search_queries():
    """
    Construiește lista completă de query-uri (keyword x zonă), fără duplicate.
    """
    queries = []
    seen = set()

    for area in SEARCH_AREAS:
        for keyword in SEARCH_KEYWORDS:
            query = f"{keyword} {area}".strip()
            if query in seen:
                continue
            seen.add(query)
            queries.append(query)

    return queries


SEARCH_QUERIES = build_search_queries()

# Regex pentru extragere email
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


def classify_size(user_ratings_total):
    """
    Clasifică service-ul după dimensiune bazat pe numărul de review-uri.

    Args:
        user_ratings_total: Număr total de review-uri Google

    Returns:
        str: "small", "medium", "large", sau "unknown"
    """
    if user_ratings_total is None:
        return "unknown"
    if user_ratings_total < 50:
        return "small"
    if user_ratings_total < 200:
        return "medium"
    return "large"


def extract_city_from_address(address):
    """
    Extrage orașul din adresa formatată de Google Maps.

    Args:
        address: Adresa completă (ex: "Str. Exemplu 1, București, România")

    Returns:
        str: Numele orașului
    """
    if not address:
        return ""
    # Split după virgulă și ia penultimul element (de obicei orașul)
    parts = [p.strip() for p in address.split(",")]
    if len(parts) >= 2:
        return parts[-2]
    return parts[-1] if parts else ""


def search_places(query):
    """
    Caută locații folosind Google Maps Places Text Search API.

    Args:
        query: Query-ul de căutare (ex: "service auto București")

    Yields:
        dict: Obiecte place din rezultate
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": GOOGLE_API_KEY,
        "language": "ro",
        "type": "car_repair",
    }

    while True:
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            status = data.get("status")

            # next_page_token poate fi invalid pentru câteva secunde după emitere.
            if status == "INVALID_REQUEST" and "pagetoken" in params:
                token_valid = False
                for _ in range(4):
                    time.sleep(2)
                    retry_resp = requests.get(url, params=params, timeout=15)
                    retry_resp.raise_for_status()
                    retry_data = retry_resp.json()
                    retry_status = retry_data.get("status")
                    if retry_status == "OK":
                        data = retry_data
                        status = retry_status
                        token_valid = True
                        break
                if not token_valid:
                    print(f"[WARNING] API error for '{query}': {status} - {data.get('error_message', 'No message')}")
                    break

            # Verifică dacă API-ul returnează erori
            if status not in ["OK", "ZERO_RESULTS"]:
                print(f"[WARNING] API error for '{query}': {status} - {data.get('error_message', 'No message')}")
                break

            for result in data.get("results", []):
                yield result

            # Verifică dacă există mai multe pagini
            next_page_token = data.get("next_page_token")
            if not next_page_token:
                break

            # Google cere un mic delay până tokenul devine valid
            time.sleep(2)
            params = {
                "pagetoken": next_page_token,
                "key": GOOGLE_API_KEY,
            }
        except requests.RequestException as e:
            print(f"[ERROR] Request failed for '{query}': {e}")
            break


def get_place_details(place_id):
    """
    Obține detalii complete despre un loc folosind Place Details API.

    Args:
        place_id: ID-ul locației din Google Maps

    Returns:
        dict: Detalii despre locație (name, address, website, phone, etc.)
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    fields = [
        "name",
        "formatted_address",
        "website",
        "formatted_phone_number",
        "rating",
        "user_ratings_total",
    ]
    params = {
        "place_id": place_id,
        "fields": ",".join(fields),
        "key": GOOGLE_API_KEY,
        "language": "ro",
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "OK":
            print(f"[WARNING] Place details error for {place_id}: {data.get('status')}")
            return {}

        return data.get("result", {})
    except requests.RequestException as e:
        print(f"[ERROR] Failed to get details for {place_id}: {e}")
        return {}


def scrape_emails_from_website(website_url):
    """
    Extrage adrese de email din website-ul public al service-ului.

    Args:
        website_url: URL-ul website-ului

    Returns:
        list: Lista de adrese de email găsite
    """
    emails = set()
    if not website_url:
        return list(emails)

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        resp = requests.get(website_url, timeout=15, headers=headers)

        if resp.status_code != 200:
            return list(emails)

        html = resp.text
        # Caută toate emailurile în HTML raw
        for match in EMAIL_REGEX.findall(html):
            # Filtrare simplă pentru emailuri comune care nu sunt business
            if not any(x in match.lower() for x in ['example.com', 'sampleemail', 'youremail']):
                emails.add(match)
    except Exception as e:
        # Fail silently - multe website-uri pot avea probleme (SSL, timeout, etc.)
        pass

    return list(emails)


def load_existing_services():
    """
    Încarcă service-urile existente din CSV pentru a evita duplicatele.

    Returns:
    -----    dict: Dicționar cu place_id-uri existente și recordurile lor
    """
    existing = {}
    csv_path = os.path.join("data", "services.csv")

    if not os.path.exists(csv_path):
        return existing

    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                place_id = row.get("id")
                if place_id:
                    existing[place_id] = row
        print(f"[INFO] Loaded {len(existing)} existing services from CSV")
    except Exception as e:
        print(f"[WARNING] Could not load existing CSV: {e}")

    return existing


def normalize_phone(phone):
    """
    Normalizează numărul de telefon pentru deduplicare.
    """
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    return digits


def normalize_website(website):
    """
    Normalizează website-ul pentru deduplicare (fără protocol, www, trailing slash).
    """
    if not website:
        return ""
    w = website.strip().lower()
    w = re.sub(r"^https?://", "", w)
    w = re.sub(r"^www\.", "", w)
    w = w.rstrip("/")
    return w


def normalize_text(value):
    """
    Normalizează textul pentru deduplicare (lowercase, spații compacte).
    """
    if not value:
        return ""
    v = value.strip().lower()
    v = re.sub(r"\s+", " ", v)
    return v


def build_dedupe_keys(record):
    """
    Construiește chei de deduplicare pentru un record.
    """
    keys = set()
    name = normalize_text(record.get("name", ""))
    address = normalize_text(record.get("address", ""))
    city = normalize_text(record.get("city", ""))
    phone = normalize_phone(record.get("phone", ""))
    website = normalize_website(record.get("website", ""))

    if name and address:
        keys.add(f"name_addr:{name}|{address}")
    if name and city and not address:
        keys.add(f"name_city:{name}|{city}")

    return keys


def main():
    """
    Funcția principală care orchestrează întregul proces de scraping.
    """
    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_MAPS_API_KEY nu este setat în environment variables.\n"
            "Setează-l folosind: export GOOGLE_MAPS_API_KEY='your-api-key'"
        )

    print("[INFO] Starting scraper...")
    print(f"[INFO] Searching {len(SEARCH_QUERIES)} locations")

    # Creează directorul pentru date dacă nu există
    os.makedirs("data", exist_ok=True)

    # Încarcă service-urile existente pentru deduplicare
    existing_services = load_existing_services()
    seen_places = existing_services.copy()  # Start cu cele existente
    results = list(existing_services.values())  # Păstrează datele vechi
    seen_dedupe_keys = set()
    for row in results:
        seen_dedupe_keys.update(build_dedupe_keys(row))

    # Procesează fiecare query
    new_services_count = 0
    for idx, query in enumerate(SEARCH_QUERIES, 1):
        print(f"\n[{idx}/{len(SEARCH_QUERIES)}] Searching: {query}")

        place_count = 0
        for place in search_places(query):
            place_id = place.get("place_id")
            if not place_id:
                continue

            # Skip dacă place_id există deja (deduplicare)
            if place_id in seen_places:
                continue

            # Obține detalii complete
            details = get_place_details(place_id)
            if not details:
                continue

            name = details.get("name")
            address = details.get("formatted_address")
            website = details.get("website")
            phone = details.get("formatted_phone_number")
            rating = details.get("rating")
            reviews = details.get("user_ratings_total")

            # Extrage email din website
            emails = scrape_emails_from_website(website)
            email = emails[0] if emails else ""

            # Clasifică dimensiunea
            size = classify_size(reviews)

            # Extrage orașul
            city = extract_city_from_address(address)

            # Timestamp
            now_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            # Construiește recordul
            record = {
                "id": place_id,
                "name": name or "",
                "size": size,
                "email": email,
                "phone": phone or "",
                "website": website or "",
                "address": address or "",
                "city": city or "",
                "rating": rating if rating is not None else "",
                "reviews": reviews if reviews is not None else "",
                "source": "google_places",
                "last_updated": now_str,
            }

            # Deduplicare suplimentară pe chei (nume+adresă, telefon, website)
            record_keys = build_dedupe_keys(record)
            if record_keys and record_keys.intersection(seen_dedupe_keys):
                continue

            seen_places[place_id] = record
            seen_dedupe_keys.update(record_keys)
            results.append(record)
            place_count += 1
            new_services_count += 1

            # Rate limiting pentru a nu abuza API-ul
            time.sleep(0.3)

        print(f"    Found {place_count} new places")

    # Scrie CSV
    csv_path = os.path.join("data", "services.csv")
    fieldnames = [
        "id",
        "name",
        "size",
        "email",
        "phone",
        "website",
        "address",
        "city",
        "rating",
        "reviews",
        "source",
        "last_updated",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    # Scrie XML
    root = ET.Element("services")
    for row in results:
        s = ET.SubElement(root, "service")
        for key in fieldnames:
            el = ET.SubElement(s, key)
            el.text = str(row.get(key, ""))

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")  # Pretty print
    xml_path = os.path.join("data", "services.xml")
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)

    # Statistici finale
    email_count = sum(1 for r in results if r.get("email"))
    size_dist = {}
    for r in results:
        size = r.get("size", "unknown")
        size_dist[size] = size_dist.get(size, 0) + 1

    print(f"\n{'='*60}")
    print(f"[SUCCESS] Scraping complete!")
    print(f"{'='*60}")
    print(f"Total services in database: {len(results)}")
    print(f"NEW services added this run: {new_services_count}")
    print(f"Services with email: {email_count} ({email_count*100//len(results) if results else 0}%)")
    print(f"\nSize distribution:")
    for size, count in sorted(size_dist.items()):
        print(f"  {size.capitalize()}: {count} ({count*100//len(results)}%)")
    print(f"\nOutput files:")
    print(f"  CSV: {csv_path}")
    print(f"  XML: {xml_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
