# Shoe Store API

Kattava backend-API kenkäkaupalle. Sisältää käyttäjähallinnan, tuotteiden hallinnan, variantit (koot/värit), tilaukset ja admin-toiminnot.

## Teknologiat

- **FastAPI** - Moderni Python web framework
- **SQLAlchemy** - ORM tietokantaoperaatioille
- **SQLite** - Tietokanta (vaihdettavissa PostgreSQL:ään)
- **JWT** - Token-pohjainen autentikointi
- **Bcrypt** - Salasanojen hashays
- **Pydantic** - Data validointi

## Ominaisuudet

### Käyttäjähallinta
- ✅ Rekisteröinti
- ✅ Kirjautuminen (JWT token)
- ✅ Käyttäjäroolit (customer/admin)
- ✅ Salasanojen turvallinen tallentaminen (bcrypt)

### Tuotteet
- ✅ Tuotteiden lisääminen (admin)
- ✅ Tuotteiden listaus
- ✅ Variantit (koko, väri, hinta, varastosaldo)

### Tilaukset
- ✅ Tilausten tekeminen
- ✅ Varastosaldon automaattinen vähentäminen
- ✅ Hintojen tallentaminen tilaushetkellä
- ✅ Tilausten statusten hallinta (admin)
- ✅ Omien tilausten näkeminen

### Admin-toiminnot
- ✅ Kaikkien tilausten näkeminen
- ✅ Tilausten statusten päivittäminen
- ✅ Tuotteiden ja varianttien hallinta

## Asennus

### 1. Kloonaa repositorio
```bash
git clone https://github.com/Xmas178/shoe-store-api.git
cd shoe-store-api
```

### 2. Luo virtuaaliympäristö
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# tai
venv\Scripts\activate  # Windows
```

### 3. Asenna riippuvuudet
```bash
pip install -r requirements.txt
```

### 4. Käynnistä sovellus
```bash
uvicorn main:app --reload
```

API käynnistyy osoitteessa: `http://127.0.0.1:8000`

## API Dokumentaatio

Interaktiivinen API-dokumentaatio: `http://127.0.0.1:8000/docs`

## Endpointit

### Autentikointi
- `POST /auth/login` - Kirjautuminen
- `POST /users/register` - Rekisteröityminen
- `GET /users/me` - Oma profiili (vaatii tokenin)

### Tuotteet
- `GET /products/` - Listaa tuotteet
- `POST /products/` - Lisää tuote (admin)

### Variantit
- `GET /variants/product/{product_id}` - Tuotteen variantit
- `POST /variants/` - Lisää variantti (admin)

### Tilaukset
- `POST /orders/` - Tee tilaus (vaatii tokenin)
- `GET /orders/my-orders` - Omat tilaukset (vaatii tokenin)
- `GET /orders/all` - Kaikki tilaukset (admin)
- `PATCH /orders/{order_id}/status` - Päivitä status (admin)

## Tietokantarakenne

### Users
- id, name, email, hashed_password, role

### Products
- id, name, brand, description, base_price, image_url

### Variants
- id, product_id, size, color, price, stock

### Orders
- id, user_id, total_price, status, created_at

### OrderItems
- id, order_id, variant_id, quantity, price_at_purchase

## Tulevaisuuden kehitysideat

- [ ] PostgreSQL tuki
- [ ] Payment gateway integraatio
- [ ] Sähköposti-notifikaatiot
- [ ] Tuotteiden hakutoiminnot
- [ ] Arvostelut ja kommentit
- [ ] Frontend (React)
- [ ] Deployment (Railway/Render)

## Tekijä

Xmas178 - [GitHub](https://github.com/Xmas178)

## Lisenssi

MIT