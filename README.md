My Blog is a simple blog project, it consists of a Django backend and a PostgreSQL database.
Since I used the Django MVT (Model-View-Template) architecture, the frontend HTML is server-side-rendered, which means Django handles the frontend as well, it builds the HTML the user recieves by dynamically allocating data into the pre-defined templates.

You can visit the online version on of the project on: blog.khalilcodes.com

In order to run the local version of the project, you must create a .env file with the necessary environment variables. The file sample_env_file.txt contains an example of how to write the .env file.

After creating the .env file all you have to do is run docker compose up --build
