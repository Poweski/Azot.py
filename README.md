# Azot - Online Store Application

#### EN

**Azot** is an e-commerce web application that allows sellers to list products and customers to browse and purchase them. The project combines the functionality of managing products, orders, and ratings and reviews, offering a simple and intuitive interface for both sellers and customers. The application also allows you to manage your user account and add funds to your customers' account.

## Main functions
### For sellers:
- Adding, editing, and deleting products.
- Managing account details.
- Viewing the history of products sold.
- Receiving ratings and reviews from customers.
  
### For customers:
- Viewing available products.
- Adding products to the cart and managing its contents.
- Purchasing products if the funds in the account are sufficient.
- Adding funds to the account.
- Managing account details.
- Viewing purchase history.
- Rating and reviewing products and sellers.
  
### General:
- Registering and logging in users divided into roles: sellers and customers.
- Account activation via a link sent by email.
- Password reset via a link sent to the email address.

## Architecture and Technologies  

### Backend  
The backend is implemented in Python using the **Django** framework. It manages HTTP requests based on the **REST API** standard, handles business logic, and interacts with the database. Data is stored locally using **SQLite**.  

### Frontend  
The frontend is built using **CustomTkinter**, offering a graphical user interface that enables seamless interaction with the application's features. This approach ensures a user-friendly experience while leveraging Python’s capabilities for desktop applications.

#### PL
**Azot** to aplikacja internetowa typu e-commerce, umożliwiająca sprzedawcom wystawianie produktów oraz klientom ich przeglądanie i zakup. Projekt łączy w sobie funkcjonalność zarządzania produktami, zamówieniami oraz ocen i recenzji, oferując prosty i intuicyjny interfejs zarówno dla sprzedawców, jak i klientów. Aplikacja pozwala również na zarządzanie kontem użytkownika oraz dodawanie środków na konto klientów.

## Główne funkcje
### Dla sprzedawców:
  - Dodawanie, edytowanie i usuwanie produktów.
  - Zarządzanie szczegółami konta.
  - Przegląd historii sprzedanych produktów.
  - Odbieranie ocen i recenzji od klientów.
    
### Dla klientów:
  - Przeglądanie dostępnych produktów.
  - Dodawanie produktów do koszyka i zarządzanie jego zawartością.
  - Zakup produktów, jeśli środki na koncie są wystarczające.
  - Dodawanie środków do konta.
  - Zarządzanie szczegółami konta.
  - Przegląd historii zakupów.
  - Ocenianie i recenzowanie produktów oraz sprzedawców.
    
### Ogólne:
  - Rejestracja i logowanie użytkowników z podziałem na role: sprzedawców i klientów.
  - Aktywacja konta poprzez link wysyłany e-mailem.
  - Resetowanie hasła za pomocą linku wysyłanego na adres e-mail.

## Architektura i technologie

### Backend
Backend jest implementowany w Pythonie przy użyciu frameworka **Django**. Zarządza żądaniami HTTP w oparciu o standard **REST API**, obsługuje logikę biznesową i współpracuje z bazą danych. Dane są przechowywane lokalnie przy użyciu **SQLite**.

### Frontend
Frontend jest zbudowany przy użyciu **CustomTkinter**, oferując graficzny interfejs użytkownika, który umożliwia bezproblemową interakcję z funkcjami aplikacji. Takie podejście zapewnia przyjazne dla użytkownika środowisko, wykorzystując jednocześnie możliwości Pythona w aplikacjach desktopowych.

## Authors and responsibilities
- **[Aliaksei Samoshyn](https://github.com/Kawaban)**: Backend (Django, REST API).
- **[Jan Powęski](https://github.com/Poweski)**: Frontend (CustomTkinter).
