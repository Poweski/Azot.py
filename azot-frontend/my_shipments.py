import streamlit as st


def show_my_shipments():
    st.title('My Shipments')
    st.write('Here you can track your shipments.')

    # Example shipments
    shipments = [
        {'item': 'Smartphone', 'status': 'In Transit'},
        {'item': 'Laptop', 'status': 'Delivered'},
    ]

    for shipment in shipments:
        st.subheader(shipment['item'])
        st.write(f'Status: {shipment["status"]}')
