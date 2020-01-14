$env:DB_USER="<database user>"
$env:DB_PASSWORD="<database password>"
$env:DB_NAME="<database name>"

./virtual/Scripts/Activate.ps1
python manage.py runserver
