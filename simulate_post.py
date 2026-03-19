from nlp_processor import NLPProcessor
from location_validator import LocationValidator
from database.db_posts import insert_post

nlp = NLPProcessor()
lv = LocationValidator()


def simulate_posts():
    test_cases_extended = [
        # --- Category: Leak / Pipe Burst ---
        "Sir, naay nibuto nga pipe diri sa San Pedro Main Road, baha na ang dalan!",
        "Paging DCWD!! Ang dako nga leak sa Linabo Proper wala pa gihapon na repair.",
        "Grabeha sa usik sa tubig sa Coastline Street, Polo. Naay buslot ang tubo.",
        "Naay nag leak sa amoa kanto sa Baybay Road, Napo. Please check tawn.",
        "Hello po, report lang ko leak dri dapit sa Crossing Street Bagtingon.",
        "Water is gushing out from the ground here in Cawa Cawa, looks like a burst main.",
        # --- Category: No Water / Low Pressure ---
        "Hapit na mag 1 week walay agas diri sa Owaon, pait kaayo.",
        "Hinay kaayo ang agas sa Station Road, Liyang. Dili kaabot sa second floor.",
        "Low water pressure alert: Purok Sanramon, San Pedro area.",
        "Zero agas in Baylimango since 5 AM. Any updates?",
        "Nganong wala namay agas diri sa Sinonoc? Ting ligo na raba.",
        "Diri sa Upper Sicayab, Hillside Drive area, 2 days na walay agas.",
        # --- Category: Dirty Water ---
        "Nganong lapok man ang tubig sa kran diri sa Dawo? Highway Road area.",
        "Murag kape ang color sa tubig diri sa Banonong, San Jose Street.",
        "Yellowish and smelly water in Larayan forest drive area.",
        "Sir/Ma'am, daghan man og balas ang tubig diri sa Purok Bayli, Baylimango.",
        "Hugaw kaayo ang agas sa amoa faucet, dili mi kapanglaba ani sa Sinonoc.",
        # --- Tricky / Non-Incidents (The "Noise") ---
        "Nganong mahal man kaayo akong bill karon nga bulan? @DCWD",  # Bill complaint
        "Pila ang bayad magpa reconnect og tubig? Salamat.",  # Inquiry
        "Salamat DCWD sa paspas nga pag repair sa leak sa Central Road!",  # Praise (Status: Non-Incident)
        "Kinsay naay baligya nga mineral water diri dapit sa Bagting? Gi uhaw nako.",  # Not a utility report
        "Water is life, but life is hard. Charot.",  # Random thought
        "Hala ka dako sa akong bill, 2k man jud. Basin naay leak sulod sa amoa balay?",  # Internal leak (Not DCWD responsibility)
        "Drinking water available here in Purok 1 Antipolo.",  # Business ad
        "Hahahahahaha uiiiiiiiiii kalingaw ba ani.",  # Gibberish/Social chatter
        "Go go go! Practice ta ninyo sa swimming pool unya.",  # Keywords used in wrong context
        # --- Dialect/Taglish Mix ---
        "Brown ang water sa amoa, Larayan forest area. Di mi katarong og ligo.",
        "Asa dapit ang office sa DCWD diri sa Dapitan? Mag bayad ko.",  # Inquiry
        "Agay! Buslot na sad ang tubo sa amoa kanto, Hilltop Drive.",
        "Please send water tank diri sa Purok 2 Burgos, 3 days na mi walay agas.",
        "Grabe ka murky ang water sa Spring Road, Linabo. Is there a maintenance?",
        "Grabeeeeeee ka murky ang tubg diari sa Spring Road, Linabo. Is there a maintenance?",
    ]

    # Header with more detail
    header = f"{'RAW TEXT':<45} | {'INTENT':<12} | {'CONF':<6} | {'STATUS':<15} | {'MATCHED LOCATION'}"
    print(header)
    print("-" * len(header))

    for text in test_cases_extended:
        # 1. NLP Extraction
        intent, confidence = nlp.extract_intent(text)

        # 2. Location Logic
        barangay = lv.matchBarangay(text)
        street = lv.matchStreet(text)
        location_row = lv.get_row_from_matches(barangay, street)

        # 3. Status Logic Gate
        if intent == "Unknown" or confidence < 0.45:  # Raised to 0.45 to kill gibberish
            status = "Non-Incident"
        elif not location_row.get("id"):
            status = "Under Evaluation (No ID)"
        else:
            status = "Under Evaluation"

        # 4. Format Location String
        if location_row.get("id"):
            loc_display = f"[{location_row['id']}] {location_row['street']}, {location_row['barangay']}"
        else:
            # Show what fuzzy matching found even if no ID was assigned
            b_found = barangay if barangay else "?"
            s_found = street if street else "?"
            loc_display = f"Partial: {s_found} | {b_found}"

        # Print Row
        print(
            f"{text[:43]:<45} | {intent:<12} | {confidence:.2f} | {status:<15} | {loc_display}"
        )


if __name__ == "__main__":
    simulate_posts()
