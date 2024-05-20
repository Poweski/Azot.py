import streamlit as st


def show_watched_ads():
    st.title('Watched Ads')
    st.write('Here you can see ads you are watching.')

    # Example watched ads
    watched_ads = [
        {'title': 'Vintage Car', 'price': '50000 PLN'},
        {'title': 'Rare Book', 'price': '300 PLN'},
    ]

    for ad in watched_ads:
        st.subheader(ad['title'])
        st.write(f'Price: {ad["price"]}')
        if st.button('Unwatch', key=f'unwatch_{ad["title"]}'):
            st.write(f'Unwatched {ad["title"]}')
