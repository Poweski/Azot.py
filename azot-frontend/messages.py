import streamlit as st

def show_messages():
    st.title('Messages')
    st.write('Here you can see your messages.')

    # Example messages
    messages = [
        {'from': 'User1', 'content': 'Is the item still available?'},
        {'from': 'User2', 'content': 'Can you lower the price?'},
    ]

    for msg in messages:
        st.subheader(f'From: {msg["from"]}')
        st.write(msg['content'])
        if st.button('Reply', key=f'reply_{msg["from"]}'):
            st.write(f'Replying to {msg["from"]}')
