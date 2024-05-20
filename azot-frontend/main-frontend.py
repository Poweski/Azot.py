import streamlit as st
import home
import profile
import my_ads
import watched_ads
import messages
import notifications
import my_shipments

# Function to handle login (mock)
def login(username, password):
    # Mocked user credentials
    if username == 'user' and password == 'password':
        return {
            'username': 'john_doe',
            'email': 'john_doe@example.com',
            'name': 'John Doe',
            'address': '123 Main St, Springfield, USA'
        }
    else:
        return None

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

# Login screen
if not st.session_state.logged_in:
    st.title('Login to Azot')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        user_info = login(username, password)
        if user_info:
            st.session_state.logged_in = True
            st.session_state.user_info = user_info
            st.success('Logged in successfully')
        else:
            st.error('Invalid username or password')
else:
    # Page settings
    st.set_page_config(page_title='Azot', layout='wide')

    # Create tabs
    tabs = st.tabs(['Home', 'My Shipments', 'My Ads', 'Watched Ads', 'Messages', 'Notifications', 'Profile'])

    # Home tab content
    with tabs[0]:
        home.show_home()

    # Profile tab content
    with tabs[1]:
        my_shipments.show_my_shipments()

    # My Ads tab content
    with tabs[2]:
        my_ads.show_my_ads()

    # Watched Ads tab content
    with tabs[3]:
        watched_ads.show_watched_ads()

    # Messages tab content
    with tabs[4]:
        messages.show_messages()

    # Notifications tab content
    with tabs[5]:
        notifications.show_notifications()

    # My Shipments tab content
    with tabs[6]:
        profile.show_profile()

    # Logout button
    if st.sidebar.button('Logout'):
        st.session_state.logged_in = False
        st.session_state.user_info = {}
        st.experimental_rerun()
