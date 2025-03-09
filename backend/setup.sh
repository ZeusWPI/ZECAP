echo "Migrating database..."
python manage.py migrate > /dev/null 2>&1
echo "Setup complete"