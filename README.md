# Django Weather Project Setup

Follow these steps to clone the project, set up a virtual environment, and install the required dependencies.


First, clone the repository to your local machine by running the following command:

```bash
git clone https://github.com/MuhammadjonArabov/Weather.git
```
Let's get into the project.
```bash
cd Weather/
```
We'll open it in Visual Studio Code. If you prefer, open it in PyCharma.
```bash
code .
```
Open the terminal and configure the virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
We install libraries
```bash
pip install -r requarments.txt
```
We create a .env package and copy all the code from .env.example and fill in our PostgreSQL data.
We run the migration
```bash
python manage.py makemigrations
python manage.py migrate
```
Run
```bash
python manage.py runserver
```
After the project is launched, check the work by visiting the following URLs:
```bash
https://2ynd74-8000.csb.app/redoc/
```

Username: admin  .    Password: 1
```bash
https://2ynd74-8000.csb.app/admin/
```
Register API
```bash
https://2ynd74-8000.csb.app/api/v1/common/register/
```
Login API
```bash
https://2ynd74-8000.csb.app/api/v1/common/login/
```
Weather API - You can get weather information by replacing Tashkent with the name of the country or city you want.
```bash
https://2ynd74-8000.csb.app/api/v1/common/weather/?q=Tashkent
```
Result
```bash
{
    "name": "Tashkent",
    "country": "Uzbekistan",
    "lat": 41.3167,
    "lon": 69.25,
    "temp_c": 5.2,
    "temp_color": "#D1F2D3",
    "wind_kph": 3.6,
    "wind_color": "#E0F7FA",
    "cloud": 0,
    "cloud_color": "#FFF9C4",
    "created_at": "2025-01-28T13:08:44.579689+05:00"
}
```



