sudo -u "$USER" bash -c 'bash -lc "
set -e

SHARED_DIR=\$HOME/shared
NGINX_CONF=/etc/nginx/sites-available/shared

echo \"🔧 Installing NGINX...\"
sudo apt update && sudo apt install -y nginx

echo \"📁 Creating shared directory at \$SHARED_DIR...\"
mkdir -p \$SHARED_DIR

if [ ! -f \$SHARED_DIR/index.html ]; then
  echo \"<h1>Hello from shared!</h1>\" > \$SHARED_DIR/index.html
fi

echo \"🔐 Setting directory and file permissions...\"
chmod o+x \"\$HOME\"
chmod o+x \"\$SHARED_DIR\"
chmod o+r \"\$SHARED_DIR\"/* || true
find \"\$SHARED_DIR\" -type d -exec chmod o+x {} \;
find \"\$SHARED_DIR\" -type f -exec chmod o+r {} \;

echo \"📝 Creating NGINX config at \$NGINX_CONF...\"
sudo bash -c \"cat > \$NGINX_CONF\" <<EOF
server {
    listen 80 default_server;
    server_name _;

    root \$HOME/shared;
    index index.html;

    location / {
        try_files \\\$uri \\\$uri/ =404;
    }

    location /shared/ {
        alias \$HOME/shared/;
        index index.html;
        autoindex on;
        autoindex_exact_size off;
    }
}
EOF

echo \"🔗 Enabling NGINX site...\"
sudo ln -sf \$NGINX_CONF /etc/nginx/sites-enabled/shared
sudo rm -f /etc/nginx/sites-enabled/default

echo \"🔄 Testing and reloading NGINX...\"
sudo nginx -t
sudo systemctl reload nginx

echo \"✅ NGINX is now serving: \$SHARED_DIR\"
"'
