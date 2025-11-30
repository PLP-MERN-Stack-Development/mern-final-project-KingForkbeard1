# BLACKOUT MARKETPLACE

A fully functional marketplace web application built with Flask, SQLAlchemy, and modern web technologies.

## Features

- User authentication and registration with phone numbers
- Item listing and management with seller information display
- Shopping cart functionality
- Search functionality
- Image upload for items
- **Comprehensive messaging system** between buyers and sellers
- Conversation threading with reply functionality
- Email notifications for new messages
- Dedicated Messages page with conversation interface
- Responsive design
- User dashboard with message inbox
- Contact forms

## Installation

1. Clone or download the project files.

2. Install Python 3.8+ if not already installed.

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. (Optional) Add sample images to `static/` folder:
   - `service-graphic.jpg`
   - `service-photo.jpg`
   - `service-fashion.jpg`
   - `default-item.jpg` (fallback image)

5. (Optional) Configure email notifications:
   - Set environment variables for email:
     ```
     export MAIL_USERNAME=your-email@gmail.com
     export MAIL_PASSWORD=your-app-password
     ```
   - For Gmail, use an app password instead of your regular password.

6. Run the application:
   ```
   python app.py
   ```

7. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
marketplace_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── add_item.html
│   ├── cart.html
│   ├── contact.html
│   └── dashboard.html
├── static/                # Static files (CSS, JS, images)
│   └── uploads/           # Uploaded item images
└── marketplace.db         # SQLite database (created automatically)
```

## Usage

1. **Registration**: Create a new account with your phone number or login with existing credentials.

2. **Browse Items**: View available services and products on the homepage with seller information displayed.

3. **Search**: Use the search bar to find specific items.

4. **Contact Sellers**: Click "Contact Seller" to send direct messages to item owners with your phone number.

5. **Messaging System**:
   - Use the "Messages" page to view all your conversations
   - Click on any conversation to view the full message thread
   - Reply to messages directly within conversations
   - Unread messages are highlighted

6. **Add to Cart**: Click "Add to Cart" on items you're interested in.

7. **Manage Cart**: View and manage items in your cart.

8. **Add Items**: Logged-in users can list their own items for sale.

9. **Dashboard**: View your profile and manage your listed items.

10. **Email Notifications**: Receive email alerts when someone contacts you about your items.

## Database Models

- **User**: Stores user information (name, email, password)
- **Item**: Stores item listings (title, description, price, category, image)
- **CartItem**: Manages items in user carts

## Security Features

- Password hashing with Flask-Bcrypt
- User session management with Flask-Login
- CSRF protection
- Input validation

## Future Enhancements

- Payment integration (Stripe)
- Email notifications
- Admin panel for managing users and items
- Real-time chat between buyers and sellers
- Review and rating system

## Contributing

Feel free to fork this project and submit pull requests with improvements.

## License

This project is open source and available under the MIT License.