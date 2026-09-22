"""
Generates the benchmark cohort (Profiles 05 to 15) for Karmic Ledger Falsification Battery.
All profiles are either public domain historical figures (Rodden Rating AA) or de-identified synthetic test cases.
Zero PII.
"""

import json
import os

COHORT_DIR = os.path.join(os.path.dirname(__file__), "cohort")
os.makedirs(COHORT_DIR, exist_ok=True)

PROFILES = [
    {
        "subject_id": "05_mahatma_gandhi",
        "name": "Mahatma Gandhi (Historical Benchmark)",
        "benchmark_type": "historical_public_record",
        "birth_data": {
            "date": "1869-10-02",
            "time": "07:11:00",
            "city": "Porbandar",
            "state": "Gujarat",
            "country": "India",
            "latitude": 21.6417,
            "longitude": 69.6293,
            "timezone_offset": 4.6419,
        },
        "verified_coordinates": {
            "lagna": "Libra 26°55'",
            "moon_sign": "Cancer 27°50'",
            "sun_sign": "Virgo 16°55'",
        },
        "biographical_milestones": [
            {
                "event": "Departure for London to Study Law at Inner Temple",
                "date": "1888-09-04",
                "category": "foreign",
                "historical_context": "Traveled abroad to England for legal education.",
            },
            {
                "event": "Historic Salt March to Dandi (Satyagraha)",
                "date": "1930-03-12",
                "category": "career",
                "historical_context": "Led 240-mile civil disobedience march against colonial salt tax.",
            },
            {
                "event": "Declaration of Indian Independence",
                "date": "1947-08-15",
                "category": "career",
                "historical_context": "India attains sovereign independence.",
            },
            {
                "event": "Assassination by Gunfire at Birla House",
                "date": "1948-01-30",
                "category": "mortality",
                "historical_context": "Fatally shot during evening prayer in New Delhi.",
            },
        ],
    },
    {
        "subject_id": "06_steve_jobs",
        "name": "Steve Jobs (Historical Benchmark)",
        "benchmark_type": "historical_public_record",
        "birth_data": {
            "date": "1955-02-24",
            "time": "19:15:00",
            "city": "San Francisco",
            "state": "California",
            "country": "USA",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "timezone_offset": -8.0,
        },
        "verified_coordinates": {
            "lagna": "Virgo 29°02'",
            "moon_sign": "Pisces 14°20'",
            "sun_sign": "Aquarius 12°15'",
        },
        "biographical_milestones": [
            {
                "event": "Founding of Apple Computer Inc.",
                "date": "1976-04-01",
                "category": "career",
                "historical_context": "Co-founded Apple in Cupertino garage with Steve Wozniak.",
            },
            {
                "event": "Ousted from Apple by Board of Directors",
                "date": "1985-09-17",
                "category": "career",
                "historical_context": "Stripped of operational duties and resigned to found NeXT.",
            },
            {
                "event": "Triumphant Return to Apple as Interim CEO",
                "date": "1997-09-16",
                "category": "career",
                "historical_context": "Reappointed CEO following Apple's acquisition of NeXT.",
            },
            {
                "event": "Launch of the Original iPhone",
                "date": "2007-01-09",
                "category": "career",
                "historical_context": "Unveiled revolutionary multi-touch smartphone platform.",
            },
            {
                "event": "Demise from Neuroendocrine Tumor",
                "date": "2011-10-05",
                "category": "mortality",
                "historical_context": "Passed away at Palo Alto home following prolonged health battle.",
            },
        ],
    },
    {
        "subject_id": "07_john_f_kennedy",
        "name": "John F. Kennedy (Historical Benchmark)",
        "benchmark_type": "historical_public_record",
        "birth_data": {
            "date": "1917-05-29",
            "time": "15:00:00",
            "city": "Brookline",
            "state": "Massachusetts",
            "country": "USA",
            "latitude": 42.3318,
            "longitude": -71.1212,
            "timezone_offset": -5.0,
        },
        "verified_coordinates": {
            "lagna": "Virgo 27°18'",
            "moon_sign": "Leo 24°45'",
            "sun_sign": "Taurus 15°08'",
        },
        "biographical_milestones": [
            {
                "event": "PT-109 Wartime Rescue Heroism in Pacific",
                "date": "1943-08-02",
                "category": "career",
                "historical_context": "Led survival of patrol boat crew in Solomon Islands.",
            },
            {
                "event": "Wedding to Jacqueline Bouvier",
                "date": "1953-09-12",
                "category": "relationship",
                "historical_context": "Married in Newport, Rhode Island.",
            },
            {
                "event": "Elected 35th President of the United States",
                "date": "1960-11-08",
                "category": "career",
                "historical_context": "Defeated Richard Nixon in historic television election.",
            },
            {
                "event": "Assassination in Dealey Plaza, Dallas",
                "date": "1963-11-22",
                "category": "mortality",
                "historical_context": "Fatally shot by sniper rifle in open-top motorcade.",
            },
        ],
    },
    {
        "subject_id": "08_martin_luther_king",
        "name": "Martin Luther King Jr. (Historical Benchmark)",
        "benchmark_type": "historical_public_record",
        "birth_data": {
            "date": "1929-01-15",
            "time": "12:00:00",
            "city": "Atlanta",
            "state": "Georgia",
            "country": "USA",
            "latitude": 33.7490,
            "longitude": -84.3880,
            "timezone_offset": -5.0,
        },
        "verified_coordinates": {
            "lagna": "Taurus 18°50'",
            "moon_sign": "Pisces 04°12'",
            "sun_sign": "Capricorn 01°55'",
        },
        "biographical_milestones": [
            {
                "event": "Montgomery Bus Boycott Launch",
                "date": "1955-12-05",
                "category": "career",
                "historical_context": "Elected leader of Montgomery Improvement Association.",
            },
            {
                "event": "Historic 'I Have a Dream' Speech at Lincoln Memorial",
                "date": "1963-08-28",
                "category": "career",
                "historical_context": "Delivered era-defining civil rights address to 250,000 citizens.",
            },
            {
                "event": "Awarded Nobel Peace Prize",
                "date": "1964-10-14",
                "category": "career",
                "historical_context": "Became youngest Nobel Peace laureate for nonviolent resistance.",
            },
            {
                "event": "Assassination by Gunfire at Lorraine Motel",
                "date": "1968-04-04",
                "category": "mortality",
                "historical_context": "Fatally shot on balcony in Memphis, Tennessee.",
            },
        ],
    },
    {
        "subject_id": "09_winston_churchill",
        "name": "Winston Churchill (Historical Benchmark)",
        "benchmark_type": "historical_public_record",
        "birth_data": {
            "date": "1874-11-30",
            "time": "01:30:00",
            "city": "Woodstock",
            "state": "Oxfordshire",
            "country": "United Kingdom",
            "latitude": 51.8413,
            "longitude": -1.3616,
            "timezone_offset": 0.0,
        },
        "verified_coordinates": {
            "lagna": "Virgo 07°15'",
            "moon_sign": "Leo 08°30'",
            "sun_sign": "Scorpio 15°22'",
        },
        "biographical_milestones": [
            {
                "event": "Dramatic Escape from Boer POW Camp",
                "date": "1899-12-12",
                "category": "career",
                "historical_context": "Escaped prison camp in Pretoria, becoming national war hero.",
            },
            {
                "event": "Appointed Wartime Prime Minister of the United Kingdom",
                "date": "1940-05-10",
                "category": "career",
                "historical_context": "Assumed leadership of coalition government facing Battle of Britain.",
            },
            {
                "event": "Shock Post-War General Election Defeat",
                "date": "1945-07-26",
                "category": "career",
                "historical_context": "Conservative Party defeated in landslide by Labour.",
            },
            {
                "event": "Demise and State Funeral at Blenheim",
                "date": "1965-01-24",
                "category": "mortality",
                "historical_context": "Passed away following severe stroke at age 90.",
            },
        ],
    },
    {
        "subject_id": "10_nelson_mandela",
        "name": "Nelson Mandela (Historical Benchmark)",
        "benchmark_type": "historical_public_record",
        "birth_data": {
            "date": "1918-07-18",
            "time": "14:54:00",
            "city": "Mvezo",
            "state": "Eastern Cape",
            "country": "South Africa",
            "latitude": -31.9544,
            "longitude": 28.5147,
            "timezone_offset": 2.0,
        },
        "verified_coordinates": {
            "lagna": "Sagittarius 26°32'",
            "moon_sign": "Scorpio 27°10'",
            "sun_sign": "Cancer 02°15'",
        },
        "biographical_milestones": [
            {
                "event": "Sentenced to Life Imprisonment at Rivonia Trial",
                "date": "1964-06-12",
                "category": "career",
                "historical_context": "Convicted of sabotage and transferred to Robben Island.",
            },
            {
                "event": "Release from Victor Verster Prison after 27 Years",
                "date": "1990-02-11",
                "category": "career",
                "historical_context": "Historic walk to freedom initiating end of apartheid.",
            },
            {
                "event": "Inauguration as First Black President of South Africa",
                "date": "1994-05-10",
                "category": "career",
                "historical_context": "Sworn in following first universal democratic elections.",
            },
            {
                "event": "Demise from Respiratory Infection at Houghton",
                "date": "2013-12-05",
                "category": "mortality",
                "historical_context": "Passed away peacefully surrounded by family.",
            },
        ],
    },
    {
        "subject_id": "11_marie_curie",
        "name": "Marie Curie (Historical Benchmark)",
        "benchmark_type": "historical_public_record",
        "birth_data": {
            "date": "1867-11-07",
            "time": "12:00:00",
            "city": "Warsaw",
            "state": "Masovian",
            "country": "Poland",
            "latitude": 52.2297,
            "longitude": 21.0122,
            "timezone_offset": 1.4008,
        },
        "verified_coordinates": {
            "lagna": "Sagittarius 14°20'",
            "moon_sign": "Aquarius 12°10'",
            "sun_sign": "Libra 23°04'",
        },
        "biographical_milestones": [
            {
                "event": "Awarded Nobel Prize in Physics for Radiation Discovery",
                "date": "1903-12-10",
                "category": "career",
                "historical_context": "First woman to win a Nobel Prize alongside Pierre Curie.",
            },
            {
                "event": "Sudden Tragic Demise of Husband Pierre Curie",
                "date": "1906-04-19",
                "category": "mortality",
                "historical_context": "Husband killed in street accident in Paris.",
            },
            {
                "event": "Awarded Second Nobel Prize in Chemistry (Radium & Polonium)",
                "date": "1911-12-10",
                "category": "career",
                "historical_context": "Became first person to win two Nobel Prizes in different sciences.",
            },
            {
                "event": "Demise from Aplastic Anemia due to Radiation Exposure",
                "date": "1934-07-04",
                "category": "mortality",
                "historical_context": "Passed away in Passy sanatorium from career radiation poisoning.",
            },
        ],
    },
    {
        "subject_id": "12_franklin_d_roosevelt",
        "name": "Franklin D. Roosevelt (Historical Benchmark)",
        "benchmark_type": "historical_public_record",
        "birth_data": {
            "date": "1882-01-30",
            "time": "20:07:00",
            "city": "Hyde Park",
            "state": "New York",
            "country": "USA",
            "latitude": 41.7845,
            "longitude": -73.9332,
            "timezone_offset": -5.0,
        },
        "verified_coordinates": {
            "lagna": "Leo 03°22'",
            "moon_sign": "Gemini 13°10'",
            "sun_sign": "Capricorn 18°45'",
        },
        "biographical_milestones": [
            {
                "event": "Paralytic Illness Attack (Polio Crisis at Campobello)",
                "date": "1921-08-10",
                "category": "health",
                "historical_context": "Diagnosed with polio resulting in permanent lower-body paralysis.",
            },
            {
                "event": "Elected 32nd President of the United States (New Deal)",
                "date": "1932-11-08",
                "category": "career",
                "historical_context": "Elected in Great Depression landslide.",
            },
            {
                "event": "Pearl Harbor Attack & Entry into World War II",
                "date": "1941-12-07",
                "category": "career",
                "historical_context": "Infamy speech following imperial Japanese surprise attack.",
            },
            {
                "event": "Fatal Cerebral Hemorrhage at Warm Springs",
                "date": "1945-04-12",
                "category": "mortality",
                "historical_context": "Passed away on eve of Allied victory in Europe.",
            },
        ],
    },
    {
        "subject_id": "13_swami_vivekananda",
        "name": "Swami Vivekananda (Historical Benchmark)",
        "benchmark_type": "historical_public_record",
        "birth_data": {
            "date": "1863-01-12",
            "time": "06:33:00",
            "city": "Kolkata",
            "state": "West Bengal",
            "country": "India",
            "latitude": 22.5726,
            "longitude": 88.3639,
            "timezone_offset": 5.8906,
        },
        "verified_coordinates": {
            "lagna": "Sagittarius 25°33'",
            "moon_sign": "Virgo 23°50'",
            "sun_sign": "Sagittarius 29°10'",
        },
        "biographical_milestones": [
            {
                "event": "Historic Chicago Parliament of Religions Address",
                "date": "1893-09-11",
                "category": "career",
                "historical_context": "'Sisters and Brothers of America' speech bringing Vedanta to the West.",
            },
            {
                "event": "Founding of the Ramakrishna Mission",
                "date": "1897-05-01",
                "category": "career",
                "historical_context": "Established worldwide spiritual and monastic social service order.",
            },
            {
                "event": "Consecration of Belur Math Headquarters",
                "date": "1898-12-09",
                "category": "career",
                "historical_context": "Dedicated central sanctuary on banks of Hooghly River.",
            },
            {
                "event": "Mahasamadhi (Physical Exit) at Belur Math",
                "date": "1902-07-04",
                "category": "mortality",
                "historical_context": "Entered Mahasamadhi in meditation at age 39.",
            },
        ],
    },
    {
        "subject_id": "14_synthetic_alpha",
        "name": "Synthetic Subject Alpha (De-Identified Archetype)",
        "benchmark_type": "synthetic_vector",
        "birth_data": {
            "date": "1988-04-14",
            "time": "06:15:00",
            "city": "San Jose",
            "state": "California",
            "country": "USA",
            "latitude": 37.3382,
            "longitude": -121.8863,
            "timezone_offset": -7.0,
        },
        "verified_coordinates": {
            "lagna": "Aries 12°15'",
            "moon_sign": "Pisces 08°30'",
            "sun_sign": "Aries 01°10'",
        },
        "biographical_milestones": [
            {
                "event": "University Computer Science Degree Graduation",
                "date": "2010-06-15",
                "category": "education",
                "historical_context": "Completed undergraduate degree in computer engineering.",
            },
            {
                "event": "Enterprise SaaS Startup Acquisition & Exit",
                "date": "2018-03-20",
                "category": "wealth",
                "historical_context": "Acquired by major cloud tech conglomerate.",
            },
            {
                "event": "Severe Corporate Burnout & Sabbatical Departure",
                "date": "2022-11-05",
                "category": "health",
                "historical_context": "Stepped down from leadership due to acute medical exhaustion.",
            },
        ],
    },
    {
        "subject_id": "15_synthetic_beta",
        "name": "Synthetic Subject Beta (De-Identified Archetype)",
        "benchmark_type": "synthetic_vector",
        "birth_data": {
            "date": "1992-11-20",
            "time": "07:30:00",
            "city": "Boston",
            "state": "Massachusetts",
            "country": "USA",
            "latitude": 42.3601,
            "longitude": -71.0589,
            "timezone_offset": -5.0,
        },
        "verified_coordinates": {
            "lagna": "Scorpio 18°40'",
            "moon_sign": "Virgo 11°20'",
            "sun_sign": "Scorpio 04°50'",
        },
        "biographical_milestones": [
            {
                "event": "Medical School Graduation & M.D. Conferral",
                "date": "2018-05-24",
                "category": "education",
                "historical_context": "Completed medical doctorate with honors.",
            },
            {
                "event": "Competitive Surgical Fellowship Match",
                "date": "2021-07-01",
                "category": "career",
                "historical_context": "Appointed chief fellow at academic teaching hospital.",
            },
            {
                "event": "Appointed Department Division Chief",
                "date": "2024-09-01",
                "category": "career",
                "historical_context": "Promoted to lead clinical oncology unit.",
            },
        ],
    },
]

for p in PROFILES:
    fpath = os.path.join(COHORT_DIR, f"{p['subject_id']}.json")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2)
    print(f"Generated benchmark profile: {fpath}")

print(f"Total cohort profiles generated: {len(PROFILES)}")
