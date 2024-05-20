import streamlit as st


def show_home():
    st.title('Welcome to Azot!')
    st.subheader('Find the best deals online')

    # Create columns for search bar and categories
    col1, col2 = st.columns([3, 1])

    with col1:
        search_query = st.text_input('Search for products', '')

    with col2:
        st.write('### Categories')
        categories = ['Electronics', 'Fashion', 'Home & Garden', 'Automotive', 'Sports & Leisure']
        selected_category = st.selectbox('Choose a category', categories)

    st.header('Featured Products')
    products = [
        {'name': 'Smartphone XYZ', 'price': '999 PLN', 'image': 'https://via.placeholder.com/150'},
        {'name': 'Laptop ABC', 'price': '2499 PLN', 'image': 'https://via.placeholder.com/150'},
        {'name': 'Watch QRS', 'price': '199 PLN', 'image': 'https://via.placeholder.com/150'},
    ]

    cols = st.columns(3)
    for i, product in enumerate(products):
        with cols[i]:
            st.image(product['image'], width=150)
            st.write(product['name'])
            st.write(product['price'])
            if st.button('Buy now', key=product['name']):
                st.write(f'You are buying {product["name"]}')
