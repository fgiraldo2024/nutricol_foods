"""English content for Nutricol. Product IDs and brands remain unchanged."""

SECTIONS = {
    "home": "", "nosotros": "about", "mercados": "markets",
    "servicios": "services", "catalogo": "catalog", "contacto": "contact",
}
SEO = {
    "home": ("Nutricol Foods | Colombian foods for new markets", "Connecting Colombian foods with importers, distributors and retailers. Rooted in Antioquia, with an international outlook."),
    "nosotros": ("About us | Nutricol Foods", "Meet Nutricol Foods: connecting Colombia's food heritage with business opportunities in new markets."),
    "mercados": ("Markets | Nutricol Foods", "Colombian foods for importers, distributors, retailers, Latin American stores and foodservice buyers exploring the United States and Europe."),
    "servicios": ("B2B services | Nutricol Foods", "Explore B2B sourcing, distribution, private label, co-packing, gift assortments and go-to-market opportunities for Colombian foods."),
    "catalogo": ("Colombian product catalog | Nutricol Foods", "Explore Colombian coffee, cacao, honey, fruit spreads and pantry products. Select products and request B2B information on WhatsApp."),
    "contacto": ("Business contact | Nutricol Foods", "Discuss sourcing, distribution or private-label opportunities with Nutricol Foods. Contact our team on WhatsApp."),
    "404": ("Page not found | Nutricol Foods", "This page is unavailable. Discover Nutricol Foods and explore our Colombian products."),
}
PRODUCT_COPY = [
    ("Cafetto Coffee", "Artisan coffee. Available presentations: 2.5 kg and 450 g."),
    ("Cafetto Coffee Tin", "Artisan coffee. Available presentations: 2.5 kg and 450 g."),
    ("Pure Cacao Tablets", "Tablets made with 100% pure cacao."),
    ("Pure Cacao Powder", "100% cacao powder. Ask our team for product specifications."),
    ("70% Cacao Bars", "Bean-to-bar chocolate with 70% cacao and notes of dried fruit and nuts."),
    ("70% Cacao Bar with Berries", "Bean-to-bar chocolate with berries and notes of dried fruit and nuts."),
    ("Cordillera 70% Cacao", "Chocolate with 70% cacao."),
    ("Cacao Nibs", "Roasted cacao nibs. Ask our team for product specifications."),
    ("Pure Honey", "Natural honey. Ask about available sizes and product specifications."),
    ("Pure Honey", "Natural honey. Ask about available sizes and product specifications."),
    ("Pure Honey", "Pure honey. Ask about available sizes."),
    ("Peanut Butter", "Spreadable peanut butter, with or without pure honey."),
    ("Goldenberry and Honey Spread", "Goldenberry (uchuva) fruit spread with honey."),
    ("Cashew Butter", "Cashew nut spread."),
    ("Avocado Oil", "Pure avocado oil, 250 ml."),
    ("Panela", "Traditional Colombian unrefined cane sugar."),
]
CATEGORIES = {"Café": "Coffee", "Cacao": "Cacao", "Miel y frutas": "Honey & fruit", "Despensa": "Pantry"}


def translated_products(products):
    if len(products) != len(PRODUCT_COPY):
        raise ValueError("English catalog copy must cover every product.")
    return [
        {**product, "titulo": PRODUCT_COPY[index][0],
         "descripcion": PRODUCT_COPY[index][1]}
        for index, product in enumerate(products)
    ]
