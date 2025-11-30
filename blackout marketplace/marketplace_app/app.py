from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Set your email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Set your app password
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    items = db.relationship('Item', backref='seller', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Item('{self.title}', '{self.price}')"

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    search_term = request.args.get('search', '')
    if search_term:
        items = Item.query.filter(
            (Item.title.contains(search_term)) |
            (Item.description.contains(search_term)) |
            (Item.category.contains(search_term))
        ).all()
    else:
        items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Login failed. Check email and password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_password, phone=phone)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')
        image = request.files.get('image')

        image_filename = None
        if image:
            image_filename = f"{datetime.now().timestamp()}_{image.filename}"
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        item = Item(title=title, description=description, price=float(price),
                   category=category, image=image_filename, user_id=current_user.id)
        db.session.add(item)
        db.session.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_item.html')

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    items = []
    total = 0
    for cart_item in cart_items:
        item = Item.query.get(cart_item.item_id)
        if item:
            items.append({'item': item, 'quantity': cart_item.quantity})
            total += item.price * cart_item.quantity
    return render_template('cart.html', items=items, total=total)

@app.route('/add_to_cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, item_id=item_id)
        db.session.add(cart_item)
    db.session.commit()
    flash('Item added to cart!', 'success')
    return redirect(url_for('home'))

@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('cart'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form
        flash('Message sent successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('contact.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_items = Item.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', items=user_items)

@app.route('/mark_message_read/<int:message_id>', methods=['POST'])
@login_required
def mark_message_read(message_id):
    message = Message.query.get_or_404(message_id)
    if message.receiver_id == current_user.id:
        message.is_read = True
        db.session.commit()
    return '', 204

@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html')

@app.route('/api/conversations')
@login_required
def get_conversations():
    # Get all unique conversations for the current user
    sent_messages = db.session.query(
        Message.receiver_id.label('other_user_id'),
        Message.sent_at.label('last_message_time'),
        Message.message.label('last_message'),
        Message.is_read
    ).filter(Message.sender_id == current_user.id).subquery()

    received_messages = db.session.query(
        Message.sender_id.label('other_user_id'),
        Message.sent_at.label('last_message_time'),
        Message.message.label('last_message'),
        Message.is_read
    ).filter(Message.receiver_id == current_user.id).subquery()

    # Combine and get latest message per conversation
    all_conversations = db.session.query(
        sent_messages.c.other_user_id,
        sent_messages.c.last_message_time,
        sent_messages.c.last_message,
        sent_messages.c.is_read
    ).union(
        db.session.query(
            received_messages.c.other_user_id,
            received_messages.c.last_message_time,
            received_messages.c.last_message,
            received_messages.c.is_read
        )
    ).subquery()

    conversations = db.session.query(
        all_conversations.c.other_user_id,
        User.name.label('other_user_name'),
        all_conversations.c.last_message,
        all_conversations.c.last_message_time,
        db.func.count(Message.id).filter(
            (Message.sender_id == all_conversations.c.other_user_id) &
            (Message.receiver_id == current_user.id) &
            (Message.is_read == False)
        ).label('unread_count')
    ).join(User, User.id == all_conversations.c.other_user_id).group_by(
        all_conversations.c.other_user_id,
        User.name,
        all_conversations.c.last_message,
        all_conversations.c.last_message_time
    ).order_by(all_conversations.c.last_message_time.desc()).all()

    return jsonify({
        'conversations': [{
            'id': conv.other_user_id,
            'other_user_name': conv.other_user_name,
            'last_message': conv.last_message[:50] + '...' if len(conv.last_message) > 50 else conv.last_message,
            'last_message_time': conv.last_message_time.strftime('%Y-%m-%d %H:%M'),
            'unread_count': conv.unread_count
        } for conv in conversations]
    })

@app.route('/api/conversation/<int:other_user_id>')
@login_required
def get_conversation(other_user_id):
    # Get all messages between current user and other user
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.sent_at).all()

    return jsonify({
        'messages': [{
            'id': msg.id,
            'sender_id': msg.sender_id,
            'sender_name': msg.sender.name,
            'message': msg.message,
            'sent_at': msg.sent_at.strftime('%Y-%m-%d %H:%M'),
            'is_read': msg.is_read
        } for msg in messages]
    })

@app.route('/api/mark_conversation_read/<int:other_user_id>', methods=['POST'])
@login_required
def mark_conversation_read(other_user_id):
    # Mark all messages from other_user to current_user as read
    Message.query.filter(
        (Message.sender_id == other_user_id) &
        (Message.receiver_id == current_user.id) &
        (Message.is_read == False)
    ).update({'is_read': True})
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/send_message/<int:receiver_id>', methods=['POST'])
@login_required
def send_message(receiver_id):
    data = request.get_json()
    message_text = data.get('message')

    if not message_text:
        return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400

    message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        message=message_text
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/contact_seller/<int:item_id>', methods=['GET', 'POST'])
@login_required
def contact_seller(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        message_text = request.form.get('message')
        phone = request.form.get('phone')

        # Create message
        message = Message(
            sender_id=current_user.id,
            receiver_id=item.user_id,
            item_id=item.id,
            subject=f"Inquiry about: {item.title}",
            message=message_text,
            phone=phone,
            email=current_user.email
        )
        db.session.add(message)
        db.session.commit()

        # Send email notification
        try:
            seller = User.query.get(item.user_id)
            email_body = f"""
Hi {seller.name},

You have received a new inquiry about your item "{item.title}".

From: {current_user.name} ({current_user.email})"""
            if phone:
                email_body += f"\nPhone: {phone}"
            email_body += f"""

Message:
{message_text}

Please check your Messages page to respond.

Best regards,
BLACKOUT Marketplace Team
"""

            msg = Message(
                subject=f"New inquiry about: {item.title}",
                recipients=[seller.email],
                body=email_body
            )
            mail.send(msg)
        except Exception as e:
            print(f"Email sending failed: {e}")

        flash('Message sent successfully! Check your Messages page to continue the conversation.', 'success')
        return redirect(url_for('messages'))

    return render_template('contact_seller.html', item=item)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add sample data if database is empty
        if Item.query.count() == 0:
            sample_items = [
                {
                    'title': 'Graphic Design Services',
                    'description': 'Professional logo design, branding, and visual identity services. Transform your brand with stunning graphics.',
                    'price': 150.00,
                    'category': 'graphic-design',
                    'image': 'service-graphic.jpg'
                },
                {
                    'title': 'Photography Services',
                    'description': 'Expert photography services for events, products, and portraits. High-quality images for all occasions.',
                    'price': 200.00,
                    'category': 'photography',
                    'image': 'service-photo.jpg'
                },
                {
                    'title': 'Fashion Design',
                    'description': 'Custom fashion design and styling services. From concept to creation, bring your fashion vision to life.',
                    'price': 300.00,
                    'category': 'fashion-design',
                    'image': 'service-fashion.jpg'
                }
            ]
            for item_data in sample_items:
                item = Item(**item_data)
                db.session.add(item)
            db.session.commit()
    app.run(debug=True)