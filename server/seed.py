from run import app, db
from models.customer import Customer
from models.product import Product
from models.order import Order, OrderItem
from models.custom_order import CustomOrder
from datetime import datetime
from werkzeug.security import generate_password_hash

with app.app_context():
    # clear existing data
    print("🌱 Clearing existing data...")
    OrderItem.query.delete()
    Order.query.delete()
    CustomOrder.query.delete()
    Customer.query.delete()
    Product.query.delete()

    # ── PRODUCTS ──────────────────────────────────────────
    print("🌱 Seeding products...")
    products = [
        Product(name="Merino Wool Scarf",      category="handmade", price=1800.0, stock=5,  is_available=True,  description="Hand-knitted soft merino scarf, perfect for cold evenings.",         image_url="scarf.jpg"),
        Product(name="Crochet Bucket Hat",      category="handmade", price=2200.0, stock=3,  is_available=True,  description="Summer cotton crochet hat, lightweight and stylish.",                image_url="hat.jpg"),
        Product(name="Chunky Knit Blanket",     category="handmade", price=4500.0, stock=2,  is_available=True,  description="Super chunky arm-knitted blanket, warm and cozy.",                  image_url="blanket.jpg"),
        Product(name="Crochet Mittens",         category="handmade", price=1200.0, stock=8,  is_available=True,  description="Wool blend mittens, handmade with love.",                           image_url="mittens.jpg"),
        Product(name="Amigurumi Teddy Bear",    category="handmade", price=950.0,  stock=10, is_available=True,  description="Adorable crochet teddy bear, great as a gift.",                     image_url="bear.jpg"),
        Product(name="Aran Wool 100g",          category="yarn",     price=650.0,  stock=20, is_available=True,  description="Natural brown aran weight wool, 200m per ball.",                    image_url="aran.jpg"),
        Product(name="Cotton DK 100g",          category="yarn",     price=580.0,  stock=15, is_available=True,  description="Sage green cotton DK yarn, 220m per ball.",                        image_url="cotton.jpg"),
        Product(name="Alpaca Blend 50g",        category="yarn",     price=820.0,  stock=12, is_available=True,  description="Mustard alpaca blend, incredibly soft, 180m per ball.",             image_url="alpaca.jpg"),
        Product(name="Merino Lace 50g",         category="yarn",     price=900.0,  stock=10, is_available=True,  description="Ivory white merino lace weight, 400m per ball.",                    image_url="lace.jpg"),
        Product(name="Chunky Acrylic 200g",     category="yarn",     price=450.0,  stock=18, is_available=True,  description="Rust orange chunky acrylic yarn, great for beginners, 150m.",      image_url="acrylic.jpg"),
    ]
    db.session.add_all(products)
    db.session.commit()

    # ── CUSTOMERS ─────────────────────────────────────────
    print("🌱 Seeding customers...")
    customers = [
        Customer(firstname="Amara",   lastname="Odhiambo", username="amara",   email="amara@email.com",   phone="0712345678", delivery_address="Kilimani, Nairobi",   password_hash=generate_password_hash("Amara123!"), is_deleted=False),
        Customer(firstname="Brian",   lastname="Kamau",    username="brian",   email="brian@email.com",   phone="0723456789", delivery_address="Westlands, Nairobi",  password_hash=generate_password_hash("Brian123!"), is_deleted=False),
        Customer(firstname="Cynthia", lastname="Wanjiku",  username="cynthia", email="cynthia@email.com", phone="0734567890", delivery_address="Kasarani, Nairobi",   password_hash=generate_password_hash("Cynthia123!"), is_deleted=False),
        Customer(firstname="David",   lastname="Otieno",   username="david",   email="david@email.com",   phone="0745678901", delivery_address="Langata, Nairobi",    password_hash=generate_password_hash("David123!"), is_deleted=False),
        Customer(firstname="Esther",  lastname="Muthoni",  username="esther",  email="esther@email.com",  phone="0756789012", delivery_address="Karen, Nairobi",      password_hash=generate_password_hash("Esther123!"), is_deleted=False),
        Customer(firstname="Felix",   lastname="Njoroge",  username="felix",   email="felix@email.com",   phone="0767890123", delivery_address="Eastleigh, Nairobi",  password_hash=generate_password_hash("Felix123!"), is_deleted=False),
        Customer(firstname="Grace",   lastname="Achieng",  username="grace",   email="grace@email.com",   phone="0778901234", delivery_address="Ruaka, Nairobi",      password_hash=generate_password_hash("Grace123!"), is_deleted=False),
        Customer(firstname="Hassan",  lastname="Mwangi",   username="hassan",  email="hassan@email.com",  phone="0789012345", delivery_address="South B, Nairobi",    password_hash=generate_password_hash("Hassan123!"), is_deleted=False),
        Customer(firstname="Irene",   lastname="Chebet",   username="irene",   email="irene@email.com",   phone="0790123456", delivery_address="Lavington, Nairobi",  password_hash=generate_password_hash("Irene123!"), is_deleted=False),
        Customer(firstname="James",   lastname="Kariuki",  username="james",   email="james@email.com",   phone="0701234567", delivery_address="Embakasi, Nairobi",   password_hash=generate_password_hash("James123!"), is_deleted=False),

        # Deleted customers (for testing soft delete)
        Customer(firstname="Karen",   lastname="Njeri",    username="karen",   email="karen@email.com",   phone="0701234567", delivery_address="Embakasi, Nairobi",   password_hash=generate_password_hash("Karen123!"), is_deleted=True),
        Customer(firstname="Leo",     lastname="Mugambi",   username="leo",     email="leo@email.com",     phone="0701234567", delivery_address="Embakasi, Nairobi",   password_hash=generate_password_hash("Leo123!"), is_deleted=True),
    ]
    db.session.add_all(customers)
    db.session.commit()

    # ── ORDERS ────────────────────────────────────────────
    print("🌱 Seeding orders...")
    orders = [
        Order(customer_id=customers[0].id, total_amount=2450.0,  status="delivered"),
        Order(customer_id=customers[1].id, total_amount=1800.0,  status="shipped"),
        Order(customer_id=customers[2].id, total_amount=4500.0,  status="confirmed"),
        Order(customer_id=customers[3].id, total_amount=1230.0,  status="pending"),
        Order(customer_id=customers[4].id, total_amount=3000.0,  status="delivered"),
        Order(customer_id=customers[5].id, total_amount=650.0,   status="pending"),
        Order(customer_id=customers[6].id, total_amount=1640.0,  status="confirmed"),
        Order(customer_id=customers[7].id, total_amount=2200.0,  status="shipped"),
        Order(customer_id=customers[8].id, total_amount=900.0,   status="delivered"),
        Order(customer_id=customers[9].id, total_amount=5350.0,  status="confirmed"),
    ]
    db.session.add_all(orders)
    db.session.commit()

    # ── ORDER ITEMS ───────────────────────────────────────
    print("🌱 Seeding order items...")
    order_items = [
        OrderItem(order_id=orders[0].id, product_id=products[0].id, quantity=1, unit_price=1800.0),
        OrderItem(order_id=orders[0].id, product_id=products[6].id, quantity=1, unit_price=580.0),
        OrderItem(order_id=orders[1].id, product_id=products[0].id, quantity=1, unit_price=1800.0),
        OrderItem(order_id=orders[2].id, product_id=products[2].id, quantity=1, unit_price=4500.0),
        OrderItem(order_id=orders[3].id, product_id=products[3].id, quantity=1, unit_price=1200.0),
        OrderItem(order_id=orders[4].id, product_id=products[1].id, quantity=1, unit_price=2200.0),
        OrderItem(order_id=orders[4].id, product_id=products[7].id, quantity=1, unit_price=820.0),
        OrderItem(order_id=orders[5].id, product_id=products[5].id, quantity=1, unit_price=650.0),
        OrderItem(order_id=orders[6].id, product_id=products[6].id, quantity=2, unit_price=580.0),
        OrderItem(order_id=orders[7].id, product_id=products[1].id, quantity=1, unit_price=2200.0),
    ]
    db.session.add_all(order_items)
    db.session.commit()

    # ── CUSTOM ORDERS ─────────────────────────────────────
    print("🌱 Seeding custom orders...")
    custom_orders = [
        CustomOrder(customer_id=customers[0].id, item_description="Knee-length cardigan in earthy tones",         yarn_preference="Merino",  color_preference="Camel brown",  size_notes="UK size 12",      budget=5000.0,  deadline=datetime(2025, 6, 1),  status="in_progress",  admin_notes="Started knitting"),
        CustomOrder(customer_id=customers[1].id, item_description="Baby blanket with star pattern",               yarn_preference="Cotton",  color_preference="Mint green",   size_notes="60x80cm",         budget=2500.0,  deadline=datetime(2025, 5, 15), status="quoted",       admin_notes="Quote sent via email"),
        CustomOrder(customer_id=customers[2].id, item_description="Matching hat and scarf set",                   yarn_preference="Alpaca",  color_preference="Dusty rose",   size_notes="Adult medium",    budget=3000.0,  deadline=datetime(2025, 5, 20), status="received",     admin_notes=None),
        CustomOrder(customer_id=customers[3].id, item_description="Crochet market bag",                           yarn_preference="Cotton",  color_preference="Natural white",size_notes="Medium sized",    budget=1500.0,  deadline=datetime(2025, 5, 10), status="ready",        admin_notes="Ready for pickup"),
        CustomOrder(customer_id=customers[4].id, item_description="Chunky knit cushion covers x2",               yarn_preference="Acrylic", color_preference="Terracotta",   size_notes="45x45cm each",    budget=2000.0,  deadline=datetime(2025, 6, 10), status="in_progress",  admin_notes="One cover done"),
        CustomOrder(customer_id=customers[5].id, item_description="Crochet wall hanging for living room",         yarn_preference="Cotton",  color_preference="Boho mixed",   size_notes="50cm wide",       budget=3500.0,  deadline=datetime(2025, 7, 1),  status="reviewing",    admin_notes=None),
        CustomOrder(customer_id=customers[6].id, item_description="Knitted dog sweater",                          yarn_preference="Merino",  color_preference="Grey",         size_notes="Small dog, 30cm", budget=1200.0,  deadline=datetime(2025, 5, 25), status="received",     admin_notes=None),
        CustomOrder(customer_id=customers[7].id, item_description="Amigurumi custom doll resembling daughter",    yarn_preference="Cotton",  color_preference="Brown skin tones", size_notes="20cm tall",   budget=1800.0,  deadline=datetime(2025, 6, 5),  status="in_progress",  admin_notes="Hair style confirmed"),
        CustomOrder(customer_id=customers[8].id, item_description="Lace shawl for wedding",                       yarn_preference="Merino Lace", color_preference="Ivory",    size_notes="180x60cm",        budget=6000.0,  deadline=datetime(2025, 8, 1),  status="quoted",       admin_notes="Design approved"),
        CustomOrder(customer_id=customers[9].id, item_description="Set of 6 crochet coasters",                    yarn_preference="Cotton",  color_preference="Multicolor",   size_notes="10cm diameter",   budget=800.0,   deadline=datetime(2025, 5, 30), status="ready",        admin_notes="Packed and ready"),
    ]
    db.session.add_all(custom_orders)
    db.session.commit()

    print("✅ Seeding complete!")
