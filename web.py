# import streamlit as st
# from st_files_connection import FilesConnection
# import json
# from streamlit_extras.colored_header import colored_header
# import random

# # Create connection object and retrieve file contents.
# # Specify input format is a csv and to cache the result for 600 seconds.
# conn = st.experimental_connection('s3', type=FilesConnection)


# df = conn.read("guna-yaaasss/csps.json", input_format="jsonl")
# entries = []
# for row in df.itertuples():
#     entries.append({'gun': row.guna, 'spanish': row.spanish})

# dontuse = True
# while(dontuse):
#     entry = random.choice(entries)
#     st.write(entry)
#     if len(entry['gun']) >= 1:
#         continue
#     else:
#         dontuse = False
        
# colored_header(
#     label="Proyecto de Traducción",
#     description="Traduce una oración de español a Guna",
#     color_name='red-70'
# )
# st.header("Proyecto de Traducción") 

# if 'stage' not in st.session_state:
#     st.session_state.stage = 0

# def set_state(i):
#     st.session_state.stage = i
    
# def set_state2(i, trad):
#     file = open('buffer.txt',"w")
#     file.truncate(0)
#     file.write(trad)
#     file.close()
#     st.session_state.stage =i

# if st.session_state.stage == 0:
#     col1, col2, col3 , col4, col5 = st.columns(5)
#     with col1:
#         pass
#     with col2:
#         pass
#     with col4:
#         pass
#     with col5:
#         pass
#     with col3 :
#         st.button('Traduce una oración', on_click=set_state, args=[1])

# if st.session_state.stage == 1:
#     st.write("La oración a traducir es: ")
#     st.subheader(f"{entry['spanish']}")
#     trad = st.text_input('Tu traducción en Guna')
#     st.button('Enviar', on_click=set_state2, args=[2, trad])
#     st.write("Dale clic al botón para mandar tu traducción")

# if st.session_state.stage >= 2:
#     trad = open('buffer.txt').read()
#     st.write(f"Tu traducción es: {trad}. Esta traducción es correcta?")
#     col1, col2, col3 , col4, col5 = st.columns(5)
#     with col1:
#         pass
#     with col2:
#         pass
#     with col4:
#         pass
#     with col5:
#         pass
#     with col3 :
#         st.button('Sí', on_click=set_state, args=[3])
#         st.button('No', on_click=set_state, args=[1])
    

# if st.session_state.stage >= 3:
#     st.write(f':{"red"}[¡Muchas gracias por tu contribución!]')
#     entry['gun'] = (trad)

#     with conn.open('guna-yaaasss/csps.json', 'a') as file:
#         json.dump(entry, file)
#         file.write('\n')
    
#     st.button('Traduce otra oración', on_click=set_state, args=[0])


import streamlit as st
import random
import json

from st_files_connection import FilesConnection


if 'submitted' not in st.session_state:
    st.session_state.submitted = ''

def submit():
    result = st.session_state.guna
    st.session_state.submitted = result
    print(st.session_state.spanish, st.session_state.guna)

    # Open the JSONL file csps.json and read it to dictionary
    entries = {}
    conn = st.experimental_connection('s3', type=FilesConnection)
    df = conn.read("guna-yaaasss/spanish_words.json", input_format="jsonl")
    for row in df.itertuples():
        entries[row.spanish] = row.guna

    # Add the new entry to the dictionary
    entries[st.session_state.spanish] = result

    # Write the dictionary back to the JSONL file
    conn = st.experimental_connection('s3', type=FilesConnection)
    with conn.open('guna-yaaasss/spanish_words.json', 'w') as f:
        for key, value in entries.items():
            f.write(json.dumps({'spanish': key, 'guna': value}) + '\n')

col1,col2 = st.columns(2)
col1.title('Sum:')
if isinstance(st.session_state.submitted, float):
    col2.title(f'{st.session_state.submitted}')
    st.experimental_rerun()

with st.form('addition'):
    #st.experimental_rerun()
    conn = st.experimental_connection('s3', type=FilesConnection)

    df = conn.read("guna-yaaasss/spanish_words.json", input_format="jsonl")
    entries = []
    for row in df.itertuples():
        if len(row.guna) < 1:
            entries.append({'guna': row.guna, 'spanish': row.spanish})
    
    selection = random.choice(entries)
    st.write('Please input the guna translation for the following sentence:')
    st.write(selection['spanish'])
    spanish = selection['spanish']
    guna = st.text_input('Your translation')
    submit = st.form_submit_button('submit')
    #st.form_submit_button('Submit', on_click=submit)

if submit:
    entries = {}
    conn = st.experimental_connection('s3', type=FilesConnection)
    df = conn.read("guna-yaaasss/spanish_words.json", input_format="jsonl")
    for row in df.itertuples():
        entries[row.spanish] = row.guna

    # Add the new entry to the dictionary
    entries[spanish] = guna

    # Write the dictionary back to the JSONL file
    conn = st.experimental_connection('s3', type=FilesConnection)
    with conn.open('guna-yaaasss/spanish_words.json', 'w') as f:
        for key, value in entries.items():
            f.write(json.dumps({'spanish': key, 'guna': value}) + '\n')

    st.experimental_rerun()