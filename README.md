# My-Blog

A straightforward blog project built using Django and PostgreSQL, fully containerized with Docker for easy deployment. 

The frontend is server-side rendered (SSR) using Django’s MVT architecture. Instead of dealing with a separate frontend framework, Django handles the views, pulls the data from Postgres, and dynamically injects it directly into the HTML templates before serving it to the browser.

🔗 **See it live:** [blog.khalilcodes.com](https://blog.khalilcodes.com)

## Local Setup

Want to run this project locally? As long as you have **Docker** and **Docker Compose** installed, it only takes a couple of steps.

### 1. Clone the repo
```bash
git clone [https://github.com/Khalil002/My-Blog.git](https://github.com/Khalil002/My-Blog.git)
cd My-Blog
```

### 2. Create your .env file
Create a file named .env in the root directory of the project. Use the keys provided in sample_env_file.txt as an example to write your necessary environment variables for the database and Django configurations.

#### 3. Build with Docker
Build the images and spin up both the Django app and the PostgreSQL database container by running:
```bash
docker compose up --build
```
