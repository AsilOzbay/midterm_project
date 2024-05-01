import mysql.connector
from flask import Flask, render_template, request
import base64

app = Flask(__name__)

def encode_base64(data):
  """Encodes data using base64 and returns a UTF-8 string."""
  return base64.b64encode(data).decode('utf-8')

app.jinja_env.filters['b64encode'] = encode_base64  # Use a more descriptive name

# Configure MySQL connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'newuser'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'products'

# Connect to MySQL database
cnx = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    auth_plugin='mysql_native_password'
)


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/search')
def search():
  query = request.args.get('query')

  # Execute search query
  cursor = cnx.cursor()
  cursor.execute("SELECT * FROM hepsiburada WHERE isim LIKE %s", ('%' + query + '%',))
  products = cursor.fetchall()
  cursor.close()

  # Get all categories (distinct)
  cursor = cnx.cursor()
  cursor.execute("SELECT DISTINCT kategori FROM hepsiburada")
  categories = cursor.fetchall()
  cursor.close()

  # Count products by category matching the search query
  category_counts = {category[0]: 0 for category in categories}
  for category in categories:
    cursor = cnx.cursor()
    cursor.execute("SELECT COUNT(*) FROM hepsiburada WHERE kategori = %s AND isim LIKE %s", (category[0], '%' + query + '%'))
    count = cursor.fetchone()[0]
    category_counts[category[0]] = count
    cursor.close()

  # Prepare matched categories with highlighting and counts
  matched_categories = []
  for category in categories:
    is_match = query.lower() in category[0].lower()
    matched_categories.append((category[0], is_match, category_counts.get(category[0], 0)))

  num_results = len(products)
  return render_template('search_results.html', products=products, categories=matched_categories, category_counts=category_counts, search_term=query, num_results=num_results)


@app.route('/category/<category>')
def category(category):
  # Fetch products and categories similar to search route
  cursor = cnx.cursor()
  cursor.execute("SELECT * FROM hepsiburada WHERE kategori = %s", (category,))
  products = cursor.fetchall()
  cursor.close()

  cursor = cnx.cursor()
  cursor.execute("SELECT DISTINCT kategori FROM hepsiburada")
  categories = cursor.fetchall()
  cursor.close()

  category_counts = {cat[0]: 0 for cat in categories}
  for cat in categories:
    cursor = cnx.cursor()
    cursor.execute("SELECT COUNT(*) FROM hepsiburada WHERE kategori = %s", (cat[0],))
    count = cursor.fetchone()[0]
    category_counts[cat[0]] = count
    cursor.close()

  num_results = len(products)
  return render_template('category_results.html', products=products, categories=categories, category_counts=category_counts, selected_category=category, num_results=num_results)


@app.route('/product/<int:product_id>')
def product(product_id):
  # Fetch product details
  cursor = cnx.cursor()
  cursor.execute("SELECT * FROM hepsiburada WHERE id = %s", (product_id,))
  product = cursor.fetchone()
  cursor.close()

  if not product:
    return "Product not found", 404

  return render_template('product_details.html', product=product)


if __name__ == '__main__':
  app.run()
