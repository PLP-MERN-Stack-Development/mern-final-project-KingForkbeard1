# Instagram-Style Marketplace

A social commerce platform built with Flask, featuring Instagram-like posts, user profiles, followers, likes, comments, and product sales in Kenyan Shillings (KES).

## Features

### 👤 User Accounts
- User registration and authentication
- Profile pages with bio, profile picture, and phone number
- Follow/unfollow system
- Followers and following counts

### 📸 Product Posts
- Instagram-style product posts with images
- Product descriptions and pricing in KES
- Image upload from local device files
- Posts display user info and timestamp

### ❤️ Likes & 💬 Comments
- Like/unlike posts functionality
- Instagram-style comment system
- Comments show username and timestamp
- Like counts displayed on posts

### 📞 Contact System
- Phone numbers displayed on user profiles
- "Contact Seller" button for direct calling
- Phone numbers stored securely

### 🏠 Feed & Discovery
- Instagram-like feed showing posts from followed users
- Explore page for discovering all products
- Grid layout for profile posts

### 💾 Database
- SQLite database with proper relationships
- Tables: Users, Posts, Comments, Likes, Follows
- Foreign key relationships maintained

## Installation

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and visit `http://localhost:5000`

## Usage

### Getting Started
1. **Sign Up**: Create an account with username, email, and phone number
2. **Complete Profile**: Add a bio and profile picture
3. **Create Posts**: Upload product images and set prices in KES
4. **Explore**: Browse products from all users
5. **Follow**: Follow other sellers to see their posts in your feed

### Navigation
- **Home**: Your personalized feed
- **Explore**: Discover all products
- **Create**: Upload new product posts
- **Profile**: View and edit your profile
- **Messages**: (Future feature for direct messaging)

### Posting Products
1. Click "Create" in the navigation
2. Upload a product image from your device
3. Write a compelling description
4. Set the price in Kenyan Shillings
5. Share your post

### Interacting with Posts
- **Like**: Click the heart icon to like posts
- **Comment**: Add comments using the comment form
- **Contact**: Use the "Contact Seller" button to call sellers
- **View Details**: Click on posts to see all comments

## Technical Details

### Database Schema
- **Users**: id, username, email, password, phone, profile_pic, bio, created_at
- **Posts**: id, image, description, price, created_at, user_id
- **Comments**: id, text, created_at, user_id, post_id
- **Likes**: id, user_id, post_id, created_at
- **Follows**: id, follower_id, followed_id, created_at

### File Upload
- Product images stored in `static/uploads/`
- Profile pictures stored in `static/profile_pics/`
- Secure filename generation to prevent conflicts
- File size and type validation

### Security
- Password hashing with Flask-Bcrypt
- Session-based authentication
- CSRF protection
- Input validation and sanitization

## API Endpoints

- `GET /` - Home feed
- `GET /explore` - Explore all posts
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /signup` - Signup page
- `POST /signup` - Process signup
- `GET /profile/<username>` - User profile
- `POST /follow/<username>` - Follow/unfollow user
- `GET /create_post` - Create post page
- `POST /create_post` - Process post creation
- `GET /post/<post_id>` - Post detail page
- `POST /like/<post_id>` - Like/unlike post
- `POST /comment/<post_id>` - Add comment
- `GET /edit_profile` - Edit profile page
- `POST /edit_profile` - Process profile update

## Future Enhancements

- Direct messaging between users
- Product categories and search
- Payment integration
- Push notifications
- Advanced analytics for sellers
- Mobile app version

## Contributing

This is a complete Instagram-style marketplace implementation. Feel free to extend it with additional features or improve the existing functionality.

## License

Open source project - feel free to use and modify.