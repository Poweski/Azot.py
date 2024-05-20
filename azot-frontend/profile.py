import streamlit as st


def show_profile():
    st.title('Profile')

    user_info = st.session_state.user_info

    st.subheader('User Information')
    st.write('**Username:**', user_info['username'])
    st.write('**Email:**', user_info['email'])
    st.write('**Name:**', user_info['name'])
    st.write('**Address:**', user_info['address'])

    st.subheader('Update Profile')
    new_name = st.text_input('Name', user_info['name'])
    new_email = st.text_input('Email', user_info['email'])
    new_address = st.text_input('Address', user_info['address'])

    if st.button('Update Profile'):
        st.session_state.user_info['name'] = new_name
        st.session_state.user_info['email'] = new_email
        st.session_state.user_info['address'] = new_address
        st.success('Profile updated successfully')

        st.write('**Username:**', user_info['username'])
        st.write('**Email:**', st.session_state.user_info['email'])
        st.write('**Name:**', st.session_state.user_info['name'])
        st.write('**Address:**', st.session_state.user_info['address'])
