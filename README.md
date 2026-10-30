# Student Information System (Django)

A simple beginner-friendly student information website built with Django. It includes a homepage, student list, add-student form, and delete action. It is prepared for deployment to AWS EC2 running Ubuntu.

## Requirements
- Python 3.10+
- pip
- Git (optional, for GitHub)

## Run on Windows

Open CMD or VS Code terminal inside this project folder:

```powershell
py -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

To stop the server, press `Ctrl+C`.

## Upload to GitHub

1. Create an empty repository at https://github.com/new (for example, `student-information-django`).
2. In this project folder, run these commands. Replace the URL with your own GitHub repository URL:

```bash
git init
git add .
git commit -m "Create Django student information website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/student-information-django.git
git push -u origin main
```

To clone it on another computer:

```bash
git clone https://github.com/YOUR-USERNAME/student-information-django.git
cd student-information-django
```

## Deploy to AWS EC2 (Ubuntu)

### 1. Launch EC2
- Launch an Ubuntu Server EC2 instance.
- In its Security Group, allow SSH (TCP 22) only from your own IP address.
- Allow HTTP (TCP 80) from anywhere for public website access.
- Add HTTPS (TCP 443) when you configure a domain and TLS certificate.
- Connect to the instance using the SSH command shown by AWS.

### 2. Install software

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip git nginx
```

### 3. Clone your GitHub project

```bash
git clone https://github.com/YOUR-USERNAME/student-information-django.git
cd student-information-django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Set production environment variables

Generate a secret key on the EC2 server:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Keep the generated value private. Do not commit it to GitHub.

For a quick first deployment in your SSH session, set:

```bash
export DJANGO_SECRET_KEY='PASTE-YOUR-GENERATED-SECRET-KEY'
export DJANGO_DEBUG='False'
export DJANGO_ALLOWED_HOSTS='YOUR_EC2_PUBLIC_IP'
```

Replace `YOUR_EC2_PUBLIC_IP` with the instance's public IPv4 address. These temporary exports disappear when the session ends; the systemd service below stores the settings used by the running website.

### 5. Prepare Django

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

### 6. Create a systemd service

Get the full project path with:

```bash
pwd
```

Create the service file:

```bash
sudo nano /etc/systemd/system/student-site.service
```

Paste this configuration. Replace `/home/ubuntu/student-information-django` with the exact path shown by `pwd`, and replace the secret and public IP:

```ini
[Unit]
Description=Gunicorn for Student Information Django Website
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/student-information-django
Environment="DJANGO_SECRET_KEY=PASTE-YOUR-GENERATED-SECRET-KEY"
Environment="DJANGO_DEBUG=False"
Environment="DJANGO_ALLOWED_HOSTS=YOUR_EC2_PUBLIC_IP"
ExecStart=/home/ubuntu/student-information-django/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 config.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Save in nano with Ctrl+O, Enter, then Ctrl+X.

Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable student-site
sudo systemctl start student-site
sudo systemctl status student-site
```

### 7. Configure Nginx

Create a configuration:

```bash
sudo nano /etc/nginx/sites-available/student-site
```

Paste this, replacing the IP and project path:

```nginx
server {
    listen 80;
    server_name YOUR_EC2_PUBLIC_IP;

    location /static/ {
        alias /home/ubuntu/student-information-django/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/student-site /etc/nginx/sites-enabled/student-site
sudo nginx -t
sudo systemctl restart nginx
```

Visit `http://YOUR_EC2_PUBLIC_IP/` in your browser.

## Useful commands after deployment

Check the Django service:

```bash
sudo systemctl status student-site
```

View application logs:

```bash
sudo journalctl -u student-site -n 50 --no-pager
```

After pushing code updates to GitHub:

```bash
cd /home/ubuntu/student-information-django
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart student-site
```

## Important notes
- This starter uses SQLite. It is suitable for a small learning project. For a larger production system, consider Amazon RDS.
- This is a basic student record demo, not a hardened school information system. Do not enter sensitive real student data without appropriate security, access controls, backups, and privacy review.
- Use HTTPS before collecting real user information.
- Never commit your Django secret key, passwords, or AWS credentials to GitHub.
