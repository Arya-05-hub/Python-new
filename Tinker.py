import bcrypt
import pickle
import os

USER_DATA_FILE = 'users.pkl'
BLOG_DATA_FILE = 'blogs.pkl'

# Utility functions
def load_data(filename, default_data):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    return default_data

def save_data(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

# User management
class UserManager:
    def init(self):
        self.users = load_data(USER_DATA_FILE, {})

    def register(self, username, password):
        if username in self.users:
            return False
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.users[username] = hashed_pw
        save_data(USER_DATA_FILE, self.users)
        return True

    def authenticate(self, username, password):
        if username not in self.users:
            return False
        hashed_pw = self.users[username]
        return bcrypt.checkpw(password.encode(), hashed_pw)

# Blog management
class BlogManager:
    def init(self):
        self.blogs = load_data(BLOG_DATA_FILE, {})

    def create_post(self, username, title, content):
        if username not in self.blogs:
            self.blogs[username] = []
        self.blogs[username].append({'title': title, 'content': content})
        save_data(BLOG_DATA_FILE, self.blogs)

    def delete_post(self, username, title):
        if username in self.blogs:
            self.blogs[username] = [post for post in self.blogs[username] if post['title'] != title]
            save_data(BLOG_DATA_FILE, self.blogs)

    def modify_post(self, username, title, new_title, new_content):
        if username in self.blogs:
            for post in self.blogs[username]:
                if post['title'] == title:
                    post['title'] = new_title
                    post['content'] = new_content
                    save_data(BLOG_DATA_FILE, self.blogs)
                    return True
        return False

    def list_posts(self, username):
        return self.blogs.get(username, [])

# Main interface
def main():
    user_manager = UserManager()
    blog_manager = BlogManager()

    while True:
        print("\n--- Blog System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if user_manager.register(username, password):
                print("Registration successful!")
            else:
                print("Username already exists.")

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if user_manager.authenticate(username, password):
                while True:
                    print("\n--- Blog Menu ---")
                    print("1. Create Post")
                    print("2. Delete Post")
                    print("3. Modify Post")
                    print("4. List Posts")
                    print("5. Logout")
                    option = input("Choose an option: ")

                    if option == '1':
                        title = input("Enter post title: ")
                        content = input("Enter post content: ")
                        blog_manager.create_post(username, title, content)
                        print("Post created successfully.")

                    elif option == '2':
                        title = input("Enter post title to delete: ")
                        blog_manager.delete_post(username, title)
                        print("Post deleted successfully.")

                    elif option == '3':
                        title = input("Enter post title to modify: ")
                        new_title = input("Enter new title: ")
                        new_content = input("Enter new content: ")
                        if blog_manager.modify_post(username, title, new_title, new_content):
                            print("Post modified successfully.")
                        else:
                            print("Post not found.")

                    elif option == '4':
                        posts = blog_manager.list_posts(username)
                        if posts:
                            for post in posts:
                                print(f"Title: {post['title']}")
                                print(f"Content: {post['content']}\n")
                        else:
                            print("No posts available.")

                    elif option == '5':
                        print("Logging out...")
                        break

                    else:
                        print("Invalid option, please try again.")

            else:
                print("Invalid username or password.")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")

if _name_ == "main":
    main()
