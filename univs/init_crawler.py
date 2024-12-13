import os
from univs.db.db_connector import DB_CLIENT

univs_names = {
    'harvard': "Harvard University",
    'yale': "Yale University",
    'stanford': "Stanford University",
    'uiuc': "University of Illinois at Urbana-Champaign"
}

ranking_spiders = ["shanghai"]
univs_spiders = ["harvard", "uiuc", "yale", "stanford"]

# Initialize DB client
db = DB_CLIENT("univs.db")

# Gather data from universities
def crawl_universities():
    for spider in univs_spiders:
        os.system(f"python3 -m scrapy crawl {spider}")

# Gather data from rankings
def crawl_rankings():
    for spider in ranking_spiders:
        os.system(f"python3 -m scrapy crawl {spider}")

# Insert University Addresses data
def insert_university_addresses():
    addresses_query = "INSERT INTO addresses VALUES(?, ?, ?, ?, ?, ?)"
    addresses = {
        'harvard': ("Cambridge", "Massachusetts", "United States of America", "02138"),
        'yale': ("New Haven", "Connecticut", "United States of America", "06520"),
        'uiuc': ("Champaign", "Illinois", "United States of America", "61820"),
        'stanford': ("Stanford", "California", "United States of America", "94305")
    }

    data = []
    for university in univs_spiders:
        data.append((univs_names[university], university, *addresses[university]))
    db.execute_many_inserts(addresses_query, data)

# Initialize the database and crawl data from universities
def init_db_and_crawl():
    db.init_db()
    
    crawl_universities()
    crawl_rankings()
    insert_university_addresses()

def format_ranking_data(university):
    query = f"SELECT pos, ranker FROM rankings WHERE university_name='{univs_names[university]}'"
    result = list(db.execute_select_query(query))[0]
    formatted_msg = f"Number {result[0]} univeristy in the world according to {result[1].capitalize()} ranking."
    return formatted_msg

def format_programs_data(university):
    formatted_msg = "Has the following list of undergraduate programs:\n"
    query = f"SELECT program_name FROM programs WHERE university_alias='{university}'"
    programs = list(db.execute_select_query(query))
    for program in programs:
        formatted_msg += f"- {program[0]}\n"
    return formatted_msg

def format_address_data(university):
    query = f"SELECT city, state, country, zipcode FROM addresses WHERE university_alias='{university}'"
    result = list(db.execute_select_query(query))[0]
    return f"University address:\n- City: {result[0]}\n- State: {result[1]}\n- Country: {result[2]}\n- Zipcode: {result[3]}"

def write_document(university, lines_to_write):
    if not os.path.exists("documents"):
        os.makedirs("documents")

    f = open(f"documents/{university}.txt", "w")
    f.write(lines_to_write)
    f.close()

# Generate documents to be used by Pyserini for querying
def generate_documents():
    for university in univs_spiders:
        formatted_ranking = format_ranking_data(university)
        formatted_programs = format_programs_data(university)
        formatted_address = format_address_data(university)

        formatted_document = f"{univs_names[university]}\n\n{formatted_ranking}\n\n{formatted_programs}\n{formatted_address}"

        write_document(university, formatted_document)

init_db_and_crawl()
generate_documents()
# db.drop_db()