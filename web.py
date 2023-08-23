import streamlit as st
from st_files_connection import FilesConnection
import json
from streamlit_extras.colored_header import colored_header
import random

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.experimental_connection('s3', type=FilesConnection)

# with conn.open("guna-yaaasss/myfile.csv", "a") as f:
#     f.write("\nRobert,bird")


# df = conn.read("guna-yaaasss/myfile.csv", input_format="csv", ttl=600)
# # Print results.
# for row in df.itertuples():
#     st.write(f"{row.Owner} has a :{row.Pet}:")


with st.echo():
    # Read back the contents of the file
    st.write(conn.read("guna-yaaasss/csps.json", input_format='text'))

df = conn.read("guna-yaaasss/csps.json", input_format="jsonl")
# Print results.
for row in df.itertuples():
    st.write(f"{row.guna}, {row.spanish}:")

entries = []
for row in df.itertuples():
    entries.append({'gun': row.guna, 'spanish': row.spanish})
# with open('csps.json', 'r') as file:
#     for line in file:
#         entries.append(json.loads(line))
# dontuse = True
# while(dontuse):
#     entry = random.choice(entries)
#     st.write(entry)
#     if len(entry['gun']) >= 1:
#         continue
#     else:
#         dontuse = False
        
colored_header(
    label="Proyecto de Traducción",
    description="Traduce una oración de español a Guna",
    color_name='red-70'
)
st.header("Proyecto de Traducción") 