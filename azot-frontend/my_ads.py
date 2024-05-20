import streamlit as st


def show_my_ads():
    st.title('My Ads')
    st.write('Here you can manage your ads.')

    # Example ad management interface
    ads = [
        {'title': 'Selling Laptop', 'description': 'A great laptop in excellent condition.', 'price': '1000 PLN'},
        {'title': 'Old Phone', 'description': 'A used phone, still works fine.', 'price': '200 PLN'},
    ]

    for ad in ads:
        st.subheader(ad['title'])
        st.write(ad['description'])
        st.write(f'Price: {ad["price"]}')
        if st.button('Edit', key=f'edit_{ad["title"]}'):
            st.write(f'Editing {ad["title"]}')
        if st.button('Delete', key=f'delete_{ad["title"]}'):
            st.write(f'Deleting {ad["title"]}')
