#!/usr/bin/env python3
"""
seed_data.py - Populate the FAAC Tracker database with comprehensive Nigerian
fiscal data including all 36 states + FCT, 774 LGAs, FAAC allocations for
Oct-Dec 2024, and 2023 IGR data.

Usage:
    python seed_data.py
"""

import random
from app import app, db, State, LGA, FAACAllocation, IGR

# ---------------------------------------------------------------------------
# 1. STATE DATA: name, code, geo_zone
# ---------------------------------------------------------------------------

STATES_DATA = [
    # South East
    ("Abia", "AB", "South East"),
    ("Anambra", "AN", "South East"),
    ("Ebonyi", "EB", "South East"),
    ("Enugu", "EN", "South East"),
    ("Imo", "IM", "South East"),
    # South South
    ("Akwa Ibom", "AK", "South South"),
    ("Bayelsa", "BY", "South South"),
    ("Cross River", "CR", "South South"),
    ("Delta", "DE", "South South"),
    ("Edo", "ED", "South South"),
    ("Rivers", "RI", "South South"),
    # South West
    ("Ekiti", "EK", "South West"),
    ("Lagos", "LA", "South West"),
    ("Ogun", "OG", "South West"),
    ("Ondo", "ON", "South West"),
    ("Osun", "OS", "South West"),
    ("Oyo", "OY", "South West"),
    # North Central
    ("Benue", "BN", "North Central"),
    ("Kogi", "KO", "North Central"),
    ("Kwara", "KW", "North Central"),
    ("Nasarawa", "NA", "North Central"),
    ("Niger", "NI", "North Central"),
    ("Plateau", "PL", "North Central"),
    ("FCT", "FC", "North Central"),
    # North East
    ("Adamawa", "AD", "North East"),
    ("Bauchi", "BA", "North East"),
    ("Borno", "BO", "North East"),
    ("Gombe", "GO", "North East"),
    ("Taraba", "TA", "North East"),
    ("Yobe", "YO", "North East"),
    # North West
    ("Jigawa", "JI", "North West"),
    ("Kaduna", "KD", "North West"),
    ("Kano", "KN", "North West"),
    ("Katsina", "KT", "North West"),
    ("Kebbi", "KB", "North West"),
    ("Sokoto", "SK", "North West"),
    ("Zamfara", "ZA", "North West"),
]

# ---------------------------------------------------------------------------
# 2. LGA DATA: state_name -> list of LGA names
# ---------------------------------------------------------------------------

LGAS_DATA = {
    "Abia": [
        "Aba North", "Aba South", "Arochukwu", "Bende", "Ikwuano",
        "Isiala Ngwa North", "Isiala Ngwa South", "Isuikwuato", "Obi Ngwa",
        "Ohafia", "Osisioma Ngwa", "Ugwunagbo", "Ukwa East", "Ukwa West",
        "Umuahia North", "Umuahia South", "Umu Nneochi",
    ],
    "Adamawa": [
        "Demsa", "Fufore", "Ganye", "Gayuk", "Gombi", "Grie", "Hong",
        "Jada", "Lamurde", "Madagali", "Maiha", "Mayo-Belwa", "Michika",
        "Mubi North", "Mubi South", "Numan", "Shelleng", "Song", "Toungo",
        "Yola North", "Yola South",
    ],
    "Akwa Ibom": [
        "Abak", "Eastern Obolo", "Eket", "Esit Eket", "Essien Udim",
        "Etim Ekpo", "Etinan", "Ibeno", "Ibesikpo Asutan", "Ibiono Ibom",
        "Ika", "Ikono", "Ikot Abasi", "Ikot Ekpene", "Ini", "Itu", "Mbo",
        "Mkpat Enin", "Nsit Atai", "Nsit Ibom", "Nsit Ubium", "Obot Akara",
        "Okobo", "Onna", "Oron", "Oruk Anam", "Udung Uko", "Ukanafun",
        "Uruan", "Urue Offong/Oruko", "Uyo",
    ],
    "Anambra": [
        "Aguata", "Anambra East", "Anambra West", "Anaocha", "Awka North",
        "Awka South", "Ayamelum", "Dunukofia", "Ekwusigo", "Idemili North",
        "Idemili South", "Ihiala", "Njikoka", "Nnewi North", "Nnewi South",
        "Ogbaru", "Onitsha North", "Onitsha South", "Orumba North",
        "Orumba South", "Oyi",
    ],
    "Bauchi": [
        "Alkaleri", "Bauchi", "Bogoro", "Damban", "Darazo", "Dass",
        "Gamawa", "Ganjuwa", "Giade", "Itas/Gadau", "Jama'are", "Katagum",
        "Kirfi", "Misau", "Ningi", "Shira", "Tafawa Balewa", "Toro",
        "Warji", "Zaki",
    ],
    "Bayelsa": [
        "Brass", "Ekeremor", "Kolokuma/Opokuma", "Nembe", "Ogbia",
        "Sagbama", "Southern Ijaw", "Yenagoa",
    ],
    "Benue": [
        "Ado", "Agatu", "Apa", "Buruku", "Gboko", "Guma", "Gwer East",
        "Gwer West", "Katsina-Ala", "Konshisha", "Kwande", "Logo",
        "Makurdi", "Obi", "Ogbadibo", "Ohimini", "Oju", "Okpokwu",
        "Otukpo", "Tarka", "Ukum", "Ushongo", "Vandeikya",
    ],
    "Borno": [
        "Abadam", "Askira/Uba", "Bama", "Bayo", "Biu", "Chibok", "Damboa",
        "Dikwa", "Gubio", "Guzamala", "Gwoza", "Hawul", "Jere", "Kaga",
        "Kala/Balge", "Konduga", "Kukawa", "Kwaya Kusar", "Mafa",
        "Magumeri", "Maiduguri", "Marte", "Mobbar", "Monguno", "Ngala",
        "Nganzai", "Shani",
    ],
    "Cross River": [
        "Abi", "Akamkpa", "Akpabuyo", "Bakassi", "Bekwarra", "Biase",
        "Boki", "Calabar Municipal", "Calabar South", "Etung", "Ikom",
        "Obanliku", "Obubra", "Obudu", "Odukpani", "Ogoja", "Yakurr",
        "Yala",
    ],
    "Delta": [
        "Aniocha North", "Aniocha South", "Bomadi", "Burutu",
        "Ethiope East", "Ethiope West", "Ika North East", "Ika South",
        "Isoko North", "Isoko South", "Ndokwa East", "Ndokwa West", "Okpe",
        "Oshimili North", "Oshimili South", "Patani", "Sapele", "Udu",
        "Ughelli North", "Ughelli South", "Ukwuani", "Uvwie",
        "Warri North", "Warri South", "Warri South West",
    ],
    "Ebonyi": [
        "Abakaliki", "Afikpo North", "Afikpo South", "Ebonyi",
        "Ezza North", "Ezza South", "Ikwo", "Ishielu", "Ivo", "Izzi",
        "Ohaozara", "Ohaukwu", "Onicha",
    ],
    "Edo": [
        "Akoko-Edo", "Egor", "Esan Central", "Esan North-East",
        "Esan South-East", "Esan West", "Etsako Central", "Etsako East",
        "Etsako West", "Igueben", "Ikpoba-Okha", "Oredo", "Orhionmwon",
        "Ovia North-East", "Ovia South-West", "Owan East", "Owan West",
        "Uhunmwonde",
    ],
    "Ekiti": [
        "Ado-Ekiti", "Efon", "Ekiti East", "Ekiti South-West",
        "Ekiti West", "Emure", "Gbonyin", "Ido-Osi", "Ijero", "Ikere",
        "Ikole", "Ilejemeje", "Irepodun/Ifelodun", "Ise/Orun", "Moba",
        "Oye",
    ],
    "Enugu": [
        "Aninri", "Awgu", "Enugu East", "Enugu North", "Enugu South",
        "Ezeagu", "Igbo-Etiti", "Igbo-Eze North", "Igbo-Eze South",
        "Isi-Uzo", "Nkanu East", "Nkanu West", "Nsukka", "Oji River",
        "Udenu", "Udi", "Uzo-Uwani",
    ],
    "Gombe": [
        "Akko", "Balanga", "Billiri", "Dukku", "Funakaye", "Gombe",
        "Kaltungo", "Kwami", "Nafada", "Shongom", "Yamaltu/Deba",
    ],
    "Imo": [
        "Aboh Mbaise", "Ahiazu Mbaise", "Ehime Mbano",
        "Ezinihitte Mbaise", "Ideato North", "Ideato South",
        "Ihitte/Uboma", "Ikeduru", "Isiala Mbano", "Isu", "Mbaitoli",
        "Ngor Okpala", "Njaba", "Nkwerre", "Nwangele", "Obowo", "Oguta",
        "Ohaji/Egbema", "Okigwe", "Onuimo", "Orlu", "Orsu", "Oru East",
        "Oru West", "Owerri Municipal", "Owerri North", "Owerri West",
    ],
    "Jigawa": [
        "Auyo", "Babura", "Biriniwa", "Birnin Kudu", "Buji", "Dutse",
        "Gagarawa", "Garki", "Gumel", "Guri", "Gwaram", "Gwiwa",
        "Hadejia", "Jahun", "Kafin Hausa", "Kaugama", "Kazaure",
        "Kiri Kasama", "Kiyawa", "Maigatari", "Malam Madori", "Miga",
        "Ringim", "Roni", "Sule Tankarkar", "Taura", "Yankwashi",
    ],
    "Kaduna": [
        "Birnin Gwari", "Chikun", "Giwa", "Igabi", "Ikara", "Jaba",
        "Jema'a", "Kachia", "Kaduna North", "Kaduna South", "Kagarko",
        "Kajuru", "Kaura", "Kauru", "Kubau", "Kudan", "Lere", "Makarfi",
        "Sabon Gari", "Sanga", "Soba", "Zangon Kataf", "Zaria",
    ],
    "Kano": [
        "Ajingi", "Albasu", "Bagwai", "Bebeji", "Bichi", "Bunkure",
        "Dala", "Dambatta", "Dawakin Kudu", "Dawakin Tofa", "Doguwa",
        "Fagge", "Gabasawa", "Garko", "Garun Mallam", "Gaya", "Gezawa",
        "Gwale", "Gwarzo", "Kabo", "Kano Municipal", "Karaye", "Kibiya",
        "Kiru", "Kumbotso", "Kunchi", "Kura", "Madobi", "Makoda",
        "Minjibir", "Nasarawa", "Rano", "Rimin Gado", "Rogo", "Shanono",
        "Sumaila", "Takai", "Tarauni", "Tofa", "Tsanyawa", "Tudun Wada",
        "Ungogo", "Warawa", "Wudil",
    ],
    "Katsina": [
        "Bakori", "Batagarawa", "Batsari", "Baure", "Bindawa", "Charanchi",
        "Dandume", "Danja", "Dan Musa", "Daura", "Dutsi", "Dutsin-Ma",
        "Faskari", "Funtua", "Ingawa", "Jibia", "Kafur", "Kaita",
        "Kankara", "Kankia", "Katsina", "Kurfi", "Kusada", "Mai'Adua",
        "Malumfashi", "Mani", "Mashi", "Matazu", "Musawa", "Rimi",
        "Sabuwa", "Safana", "Sandamu", "Zango",
    ],
    "Kebbi": [
        "Aleiro", "Arewa Dandi", "Argungu", "Augie", "Bagudo",
        "Birnin Kebbi", "Bunza", "Dandi", "Fakai", "Gwandu", "Jega",
        "Kalgo", "Koko/Besse", "Maiyama", "Ngaski", "Sakaba", "Shanga",
        "Suru", "Wasagu/Danko", "Yauri", "Zuru",
    ],
    "Kogi": [
        "Adavi", "Ajaokuta", "Ankpa", "Bassa", "Dekina", "Ibaji", "Idah",
        "Igalamela-Odolu", "Ijumu", "Kabba/Bunu", "Koton Karfe", "Lokoja",
        "Mopa-Muro", "Ofu", "Ogori/Magongo", "Okehi", "Okene",
        "Olamaboro", "Omala", "Yagba East", "Yagba West",
    ],
    "Kwara": [
        "Asa", "Baruten", "Edu", "Ekiti", "Ifelodun", "Ilorin East",
        "Ilorin South", "Ilorin West", "Irepodun", "Isin", "Kaiama",
        "Moro", "Offa", "Oke Ero", "Oyun", "Pategi",
    ],
    "Lagos": [
        "Agege", "Ajeromi-Ifelodun", "Alimosho", "Amuwo-Odofin", "Apapa",
        "Badagry", "Epe", "Eti-Osa", "Ibeju-Lekki", "Ifako-Ijaiye",
        "Ikeja", "Ikorodu", "Kosofe", "Lagos Island", "Lagos Mainland",
        "Mushin", "Ojo", "Oshodi-Isolo", "Shomolu", "Surulere",
    ],
    "Nasarawa": [
        "Akwanga", "Awe", "Doma", "Karu", "Keana", "Keffi", "Kokona",
        "Lafia", "Nasarawa", "Nasarawa Eggon", "Obi", "Toto", "Wamba",
    ],
    "Niger": [
        "Agaie", "Agwara", "Bida", "Borgu", "Bosso", "Chanchaga",
        "Edatti", "Gbako", "Gurara", "Katcha", "Kontagora", "Lapai",
        "Lavun", "Magama", "Mariga", "Mashegu", "Mokwa", "Munya",
        "Paikoro", "Rafi", "Rijau", "Shiroro", "Suleja", "Tafa",
        "Wushishi",
    ],
    "Ogun": [
        "Abeokuta North", "Abeokuta South", "Ado-Odo/Ota", "Egbado North",
        "Egbado South", "Ewekoro", "Ifo", "Ijebu East", "Ijebu North",
        "Ijebu North East", "Ijebu Ode", "Ikenne", "Imeko Afon", "Ipokia",
        "Obafemi Owode", "Odeda", "Odogbolu", "Ogun Waterside",
        "Remo North", "Sagamu",
    ],
    "Ondo": [
        "Akoko North-East", "Akoko North-West", "Akoko South-East",
        "Akoko South-West", "Akure North", "Akure South", "Ese Odo",
        "Idanre", "Ifedore", "Ilaje", "Ile Oluji/Okeigbo", "Irele",
        "Odigbo", "Okitipupa", "Ondo East", "Ondo West", "Ose", "Owo",
    ],
    "Osun": [
        "Aiyedaade", "Aiyedire", "Atakunmosa East", "Atakunmosa West",
        "Boluwaduro", "Boripe", "Ede North", "Ede South", "Egbedore",
        "Ejigbo", "Ife Central", "Ife East", "Ife North", "Ife South",
        "Ifedayo", "Ifelodun", "Ila", "Ilesa East", "Ilesa West",
        "Irepodun", "Irewole", "Isokan", "Iwo", "Obokun", "Odo Otin",
        "Ola Oluwa", "Olorunda", "Oriade", "Orolu", "Osogbo",
    ],
    "Oyo": [
        "Afijio", "Akinyele", "Atiba", "Atisbo", "Egbeda", "Ibadan North",
        "Ibadan North-East", "Ibadan North-West", "Ibadan South-East",
        "Ibadan South-West", "Ibarapa Central", "Ibarapa East",
        "Ibarapa North", "Ido", "Irepo", "Iseyin", "Itesiwaju", "Iwajowa",
        "Kajola", "Lagelu", "Ogbomosho North", "Ogbomosho South",
        "Ogo Oluwa", "Oluyole", "Ona Ara", "Orelope", "Ori Ire",
        "Oyo East", "Oyo West", "Saki East", "Saki West", "Surulere",
        "Olorunsogo",
    ],
    "Plateau": [
        "Barkin Ladi", "Bassa", "Bokkos", "Jos East", "Jos North",
        "Jos South", "Kanam", "Kanke", "Langtang North", "Langtang South",
        "Mangu", "Mikang", "Pankshin", "Qua'an Pan", "Riyom", "Shendam",
        "Wase",
    ],
    "Rivers": [
        "Abua/Odual", "Ahoada East", "Ahoada West", "Akuku-Toru",
        "Andoni", "Asari-Toru", "Bonny", "Degema", "Eleme", "Emohua",
        "Etche", "Gokana", "Ikwerre", "Khana", "Obio/Akpor",
        "Ogba/Egbema/Ndoni", "Ogu/Bolo", "Okrika", "Omuma",
        "Opobo/Nkoro", "Oyigbo", "Port Harcourt", "Tai",
    ],
    "Sokoto": [
        "Binji", "Bodinga", "Dange Shuni", "Gada", "Goronyo", "Gudu",
        "Gwadabawa", "Illela", "Isa", "Kebbe", "Kware", "Rabah",
        "Sabon Birni", "Shagari", "Silame", "Sokoto North", "Sokoto South",
        "Tambuwal", "Tangaza", "Tureta", "Wamako", "Wurno", "Yabo",
    ],
    "Taraba": [
        "Ardo Kola", "Bali", "Donga", "Gashaka", "Gassol", "Ibi",
        "Jalingo", "Karim Lamido", "Kurmi", "Lau", "Sardauna", "Takum",
        "Ussa", "Wukari", "Yorro", "Zing",
    ],
    "Yobe": [
        "Bade", "Bursari", "Damaturu", "Fika", "Fune", "Geidam", "Gujba",
        "Gulani", "Jakusko", "Karasuwa", "Machina", "Nangere", "Nguru",
        "Potiskum", "Tarmuwa", "Yunusari", "Yusufari",
    ],
    "Zamfara": [
        "Anka", "Bakura", "Birnin Magaji/Kiyaw", "Bukkuyum", "Bungudu",
        "Gummi", "Gusau", "Kaura Namoda", "Maradun", "Maru", "Shinkafi",
        "Talata Mafara", "Tsafe", "Zurmi",
    ],
    "FCT": [
        "Abaji", "Bwari", "Gwagwalada", "Kuje", "Kwali",
        "Municipal Area Council (AMAC)",
    ],
}

# ---------------------------------------------------------------------------
# 3. FAAC MONTHLY NET ALLOCATION BASELINES (in Naira)
#    These are approximate mid-range net allocations per month.
#    Oct/Nov/Dec 2024 will vary +/- around these values.
# ---------------------------------------------------------------------------

# Multiplier: 1 billion = 1_000_000_000
B = 1_000_000_000

FAAC_NET_BASELINES = {
    "Lagos":       35.0 * B,
    "Rivers":      28.0 * B,
    "Delta":       22.0 * B,
    "Akwa Ibom":   20.0 * B,
    "Bayelsa":     14.5 * B,
    "FCT":         14.5 * B,
    "Kano":        11.5 * B,
    "Oyo":          9.0 * B,
    "Edo":          9.0 * B,
    "Kaduna":       8.0 * B,
    "Ogun":         8.0 * B,
    "Ondo":         8.0 * B,
    "Enugu":        7.0 * B,
    "Imo":          7.0 * B,
    "Cross River":  7.0 * B,
    "Abia":         6.0 * B,
    "Anambra":      6.0 * B,
    "Benue":        6.0 * B,
    "Borno":        6.0 * B,
    "Plateau":      6.0 * B,
    "Kogi":         6.0 * B,
    "Niger":        6.0 * B,
    "Osun":         6.0 * B,
    "Katsina":      6.0 * B,
    "Bauchi":       6.0 * B,
    "Kwara":        5.0 * B,
    "Sokoto":       5.0 * B,
    "Adamawa":      5.0 * B,
    "Taraba":       5.0 * B,
    "Nasarawa":     5.0 * B,
    "Jigawa":       5.0 * B,
    "Gombe":        4.5 * B,
    "Ebonyi":       4.5 * B,
    "Ekiti":        4.5 * B,
    "Kebbi":        4.5 * B,
    "Yobe":         4.5 * B,
    "Zamfara":      4.5 * B,
}

# ---------------------------------------------------------------------------
# 4. IGR 2023 ANNUAL DATA (in Naira)
# ---------------------------------------------------------------------------

IGR_ANNUAL_2023 = {
    "Lagos":       651.0 * B,
    "Rivers":      117.0 * B,
    "FCT":          92.0 * B,
    "Ogun":         65.0 * B,
    "Delta":        50.0 * B,
    "Kaduna":       40.0 * B,
    "Kano":         38.0 * B,
    "Oyo":          35.0 * B,
    "Edo":          32.0 * B,
    "Ondo":         28.0 * B,
    "Enugu":        25.0 * B,
    "Akwa Ibom":    23.0 * B,
    "Cross River":  20.0 * B,
    "Anambra":      19.0 * B,
    "Abia":         18.0 * B,
    "Kwara":        17.0 * B,
    "Bauchi":       16.0 * B,
    "Osun":         15.0 * B,
    "Plateau":      14.0 * B,
    "Ekiti":        13.0 * B,
    "Imo":          12.0 * B,
    "Benue":        12.0 * B,
    "Niger":        11.0 * B,
    "Kogi":         11.0 * B,
    "Nasarawa":     10.0 * B,
    "Adamawa":      10.0 * B,
    "Borno":        10.0 * B,
    "Ebonyi":        9.0 * B,
    "Katsina":       9.0 * B,
    "Sokoto":        8.0 * B,
    "Bayelsa":       8.0 * B,
    "Gombe":         8.0 * B,
    "Taraba":        7.0 * B,
    "Jigawa":        7.0 * B,
    "Zamfara":       6.0 * B,
    "Kebbi":         6.0 * B,
    "Yobe":          5.0 * B,
}

# Capital / main LGAs that get a slightly larger share of LGA allocations
CAPITAL_LGAS = {
    "Abia": "Umuahia North",
    "Adamawa": "Yola North",
    "Akwa Ibom": "Uyo",
    "Anambra": "Awka South",
    "Bauchi": "Bauchi",
    "Bayelsa": "Yenagoa",
    "Benue": "Makurdi",
    "Borno": "Maiduguri",
    "Cross River": "Calabar Municipal",
    "Delta": "Oshimili South",
    "Ebonyi": "Abakaliki",
    "Edo": "Oredo",
    "Ekiti": "Ado-Ekiti",
    "Enugu": "Enugu South",
    "Gombe": "Gombe",
    "Imo": "Owerri Municipal",
    "Jigawa": "Dutse",
    "Kaduna": "Kaduna North",
    "Kano": "Kano Municipal",
    "Katsina": "Katsina",
    "Kebbi": "Birnin Kebbi",
    "Kogi": "Lokoja",
    "Kwara": "Ilorin West",
    "Lagos": "Ikeja",
    "Nasarawa": "Lafia",
    "Niger": "Chanchaga",
    "Ogun": "Abeokuta South",
    "Ondo": "Akure South",
    "Osun": "Osogbo",
    "Oyo": "Ibadan North",
    "Plateau": "Jos North",
    "Rivers": "Port Harcourt",
    "Sokoto": "Sokoto North",
    "Taraba": "Jalingo",
    "Yobe": "Damaturu",
    "Zamfara": "Gusau",
    "FCT": "Municipal Area Council (AMAC)",
}


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def vary(base, pct=0.05):
    """Return base value varied randomly by +/- pct."""
    return base * random.uniform(1 - pct, 1 + pct)


def generate_faac_for_state(state_name, month, year):
    """
    Generate a realistic FAAC allocation row for a state.
    Returns dict with statutory_allocation, vat_allocation, total_gross,
    deductions, net_allocation.
    """
    net_base = FAAC_NET_BASELINES.get(state_name, 5.0 * B)

    # Vary net by +/- 5% across months
    net_allocation = vary(net_base, 0.06)

    # net = gross - deductions
    # deductions are typically 8-12% of gross => net = gross * (1 - ded_rate)
    ded_rate = random.uniform(0.08, 0.12)
    total_gross = net_allocation / (1 - ded_rate)
    deductions = total_gross - net_allocation

    # statutory ~60% of gross, vat ~40%
    stat_ratio = random.uniform(0.58, 0.62)
    statutory_allocation = total_gross * stat_ratio
    vat_allocation = total_gross - statutory_allocation

    return {
        "statutory_allocation": round(statutory_allocation, 2),
        "vat_allocation": round(vat_allocation, 2),
        "total_gross": round(total_gross, 2),
        "deductions": round(deductions, 2),
        "net_allocation": round(net_allocation, 2),
    }


def distribute_lga_allocations(state_name, lga_names, state_alloc, month, year):
    """
    Distribute a state's FAAC allocation proportionally among its LGAs.
    The capital LGA gets a ~15-25% boost. Returns list of dicts.
    """
    n = len(lga_names)
    if n == 0:
        return []

    capital = CAPITAL_LGAS.get(state_name)

    # Generate random weights
    weights = {}
    for lga_name in lga_names:
        base_weight = random.uniform(0.8, 1.2)
        if lga_name == capital:
            base_weight *= random.uniform(1.15, 1.25)  # capital bonus
        weights[lga_name] = base_weight

    total_weight = sum(weights.values())

    # LGA allocations are roughly 30-40% of the state-level allocation
    # (separate from the state allocation shown at state level)
    lga_pool = state_alloc["net_allocation"] * random.uniform(0.30, 0.38)

    results = []
    for lga_name in lga_names:
        share = weights[lga_name] / total_weight
        lga_net = lga_pool * share

        # Derive components from the LGA net
        ded_rate = random.uniform(0.06, 0.10)
        lga_gross = lga_net / (1 - ded_rate)
        lga_ded = lga_gross - lga_net

        stat_ratio = random.uniform(0.58, 0.62)
        lga_stat = lga_gross * stat_ratio
        lga_vat = lga_gross - lga_stat

        results.append({
            "lga_name": lga_name,
            "statutory_allocation": round(lga_stat, 2),
            "vat_allocation": round(lga_vat, 2),
            "total_gross": round(lga_gross, 2),
            "deductions": round(lga_ded, 2),
            "net_allocation": round(lga_net, 2),
        })

    return results


# ---------------------------------------------------------------------------
# MAIN SEEDING LOGIC
# ---------------------------------------------------------------------------

def seed():
    random.seed(42)  # Reproducible data

    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()

    # ------------------------------------------------------------------
    # Step 1: Create States
    # ------------------------------------------------------------------
    print("Seeding states...")
    state_objects = {}
    for name, code, zone in STATES_DATA:
        s = State(name=name, code=code, geo_zone=zone)
        db.session.add(s)
        state_objects[name] = s

    db.session.flush()  # Assign IDs
    print(f"  -> {len(state_objects)} states created.")

    # ------------------------------------------------------------------
    # Step 2: Create LGAs
    # ------------------------------------------------------------------
    print("Seeding LGAs...")
    lga_objects = {}  # (state_name, lga_name) -> LGA object
    total_lga_count = 0

    for state_name, lga_names in LGAS_DATA.items():
        state_obj = state_objects[state_name]
        for lga_name in lga_names:
            lga = LGA(name=lga_name, state_id=state_obj.id)
            db.session.add(lga)
            lga_objects[(state_name, lga_name)] = lga
            total_lga_count += 1

    db.session.flush()  # Assign IDs
    print(f"  -> {total_lga_count} LGAs created.")

    # ------------------------------------------------------------------
    # Step 3: FAAC Allocations (Oct, Nov, Dec 2024) - State level + LGA level
    # ------------------------------------------------------------------
    print("Seeding FAAC allocations (Oct-Dec 2024)...")
    months = [(10, 2024), (11, 2024), (12, 2024)]
    alloc_count = 0

    for month, year in months:
        for state_name, state_obj in state_objects.items():
            # State-level allocation
            alloc_data = generate_faac_for_state(state_name, month, year)
            state_alloc = FAACAllocation(
                state_id=state_obj.id,
                lga_id=None,
                month=month,
                year=year,
                statutory_allocation=alloc_data["statutory_allocation"],
                vat_allocation=alloc_data["vat_allocation"],
                total_gross=alloc_data["total_gross"],
                deductions=alloc_data["deductions"],
                net_allocation=alloc_data["net_allocation"],
            )
            db.session.add(state_alloc)
            alloc_count += 1

            # LGA-level allocations
            lga_names = LGAS_DATA.get(state_name, [])
            lga_allocs = distribute_lga_allocations(
                state_name, lga_names, alloc_data, month, year
            )
            for la in lga_allocs:
                lga_obj = lga_objects[(state_name, la["lga_name"])]
                lga_alloc = FAACAllocation(
                    state_id=state_obj.id,
                    lga_id=lga_obj.id,
                    month=month,
                    year=year,
                    statutory_allocation=la["statutory_allocation"],
                    vat_allocation=la["vat_allocation"],
                    total_gross=la["total_gross"],
                    deductions=la["deductions"],
                    net_allocation=la["net_allocation"],
                )
                db.session.add(lga_alloc)
                alloc_count += 1

    db.session.flush()
    print(f"  -> {alloc_count} FAAC allocation records created.")

    # ------------------------------------------------------------------
    # Step 4: IGR 2023 Data (4 quarters)
    # ------------------------------------------------------------------
    print("Seeding IGR 2023 data...")
    igr_count = 0

    # Quarterly distribution factors (slight seasonal variation)
    q_factors = {
        1: 0.22,  # Q1 slightly lower
        2: 0.25,  # Q2 moderate
        3: 0.25,  # Q3 moderate
        4: 0.28,  # Q4 typically higher (year-end push)
    }

    for state_name, state_obj in state_objects.items():
        annual = IGR_ANNUAL_2023.get(state_name, 10.0 * B)
        for quarter in range(1, 5):
            base_quarterly = annual * q_factors[quarter]
            # Add small random variation (+/- 5%)
            amount = vary(base_quarterly, 0.05)
            igr = IGR(
                state_id=state_obj.id,
                year=2023,
                quarter=quarter,
                amount=round(amount, 2),
            )
            db.session.add(igr)
            igr_count += 1

    print(f"  -> {igr_count} IGR records created.")

    # ------------------------------------------------------------------
    # Commit everything
    # ------------------------------------------------------------------
    print("Committing to database...")
    db.session.commit()
    print("=" * 60)
    print("DATABASE SEEDED SUCCESSFULLY!")
    print(f"  States:           {len(state_objects)}")
    print(f"  LGAs:             {total_lga_count}")
    print(f"  FAAC Allocations: {alloc_count}")
    print(f"  IGR Records:      {igr_count}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    with app.app_context():
        seed()
