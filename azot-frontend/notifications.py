import streamlit as st


def show_notifications():
    st.title('Notifications')
    st.write('Here you can see your notifications.')

    # Example notifications
    notifications = [
        'Your ad "Vintage Car" has received a new offer.',
        'Your shipment has been delivered.',
    ]

    for notification in notifications:
        st.write(notification)
