# import libraries
import sqlite3
import streamlit as st
import requests


# ASEA API
API_URL = "https://www.stack-inference.com/run_deployed_flow?flow_id=659e84417c04c17941237900&org=54bd58b7-9ffa-4161-91f0-565405a9d32d"
headers = {'Authorization':
           'Bearer cfc3f051-23da-4dc6-b3e8-0fce0dabe449',
           'Content-Type': 'application/json'
           }

##############


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


######## Set Streamlit page title and icon #######
st.set_page_config(
    page_title="Astro_Mind",
    page_icon="🌌"
)


###### Department ########
st.title("Astro_Mind🌌")

######## Title and introduction #######

st.write("An AI Assistant for every ARSSDC questions!")

###### Text Uploader #######

# Database setup
conn = sqlite3.connect("conversation.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        role TEXT,
        content TEXT
    )
""")
conn.commit()


# React to user input
prompt = st.text_input("Write down your question here:")

# Display user message in chat message container
if st.button("Send"):
    with st.container():
        st.title(f"Question: {prompt}")
       

    # Add user message to the database
    cursor.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)", ("user", prompt))
    conn.commit()

    # Process the user prompt and get the response
    answer = query({"in-0": prompt})
    response = answer.get('out-2', '')

    # Display the response in the chat message container
    with st.container():
        st.title("Astro Mind:")
        st.write(response)

    # Add assistant response to the database
    cursor.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", response))
    conn.commit()

# Retrieve entire conversation from the database
# if st.button("Show Conversation"):
#     conversation = cursor.execute(
#         "SELECT role, content FROM messages").fetchall()
#     for role, content in conversation:
#         with st.container():
#             st.write(f"{role.capitalize()}:")
#             st.write(content)
#####################################


def main():
    st.title("")


if __name__ == "__main__":
    main()
