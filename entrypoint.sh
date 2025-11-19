#!/bin/sh

# Exit immediately if any command exits with a non-zero status
set -e

# Copy default media only if sliders folder is empty
#if [ ! -d "/app/eshop/media/sliders" ] || [ -z "$(ls -A /app/eshop/media/sliders 2>/dev/null)" ]; then
#  echo "Copying initial slider images..."
#  mkdir -p /app/eshop/media/sliders
#  cp -r /app/eshop/media_initial/sliders/* /app/eshop/media/sliders/
#fi

echo "Running database seed..."
python eshop/manage.py seed

echo "Running Collect Static files"
python eshop/manage.py collectstatic

echo "Starting Django development server..."
exec python eshop/manage.py runserver 0.0.0.0:8000
