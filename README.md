# 📝 Note-Taking Web App on AWS EC2 with Backup Strategy

This project demonstrates how to deploy a simple note-taking web application using Flask and MariaDB on a Red Hat Enterprise Linux (RHEL 9) EC2 instance. It also includes a backup strategy by mounting a separate EBS volume to store database backups.
# Technologies Used

- 🐍 Python 3
- 🔥 Flask (Python Web Framework)
- 🐬 MariaDB (Relational Database)
- 🐘 SQL (Basic CRUD)
- 🐧 RHEL 9 (Red Hat Enterprise Linux)
- ☁️ AWS EC2 (t2.micro)
- 💾 AWS EBS (for backup)
- 🔧 Gunicorn (WSGI HTTP server)
- 🌐 Nginx (Reverse Proxy)
- 🛠️ Systemd (Service Manager)
- 📂 Git & GitHub (Version Control)

## 🏗️ Project Architecture

The project is structured as follows:

1. **Frontend**: Simple HTML form to submit and display notes.
2. **Backend**: Flask application running with Gunicorn on port `5000`.
3. **Database**: MariaDB stores notes with timestamps.
4. **Web Server**: Nginx forwards HTTP requests to Gunicorn.
5. **Systemd**: Manages the Flask app as a service (`noteapp.service`).
6. **Backup**: Automated SQL dumps to `/backup` on a mounted EBS volume.

## 🧰 Step-by-Step Setup

### 1. Create EC2 Instance
- OS: Red Hat Enterprise Linux 9
- Type: t2.micro
- Open ports: 22 (SSH), 80 (HTTP)
- Create key pair for SSH access.

### 2. Install Required Packages
```bash
sudo dnf update -y
sudo dnf install git python3 python3-pip mariadb105-server nginx -y

##Clone the Repository & Set Up App
git clone https://github.com/omar-elmallah/note_app.git
cd note_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

##Set Up MariaDB
sudo systemctl enable mariadb --now
sudo mysql -u root

##then run 
CREATE DATABASE notesdb;
CREATE USER 'noteuser'@'localhost' IDENTIFIED BY 'strongpassword';
GRANT ALL PRIVILEGES ON notesdb.* TO 'noteuser'@'localhost';
FLUSH PRIVILEGES;
USE notesdb;
CREATE TABLE notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

##Create systemd Service
[Unit]
Description=Gunicorn instance to serve Flask Note App
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/note-app
Environment="PATH=/home/ec2-user/note-app/venv/bin"
ExecStart=/home/ec2-user/note-app/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target

##Enable and start the service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable noteapp
sudo systemctl start noteapp

## Configure Nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

sudo nginx -t
sudo systemctl restart nginx

##Setup Backup Volume
sudo mkfs.xfs /dev/xvdf
sudo mkdir /backup
sudo mount /dev/xvdf /backup
echo "/dev/xvdf /backup xfs defaults,nofail 0 0" | sudo tee -a /etc/fstab
##Backup MariaDB
sudo mysqldump -u root notesdb > /backup/notes_backup.sql

## ✅ Deliverables Summary

- ✅ **Source Code**: Full Flask app code including `app.py`, `templates`, and `requirements.txt`.
- ✅ **Screenshots**: Captured while app was running successfully on EC2.
- ✅ **MariaDB Schema**:
  - Database: `notesdb`
  - Table: `notes` with columns `id`, `content`, and `created_at`
- ✅ **Mounted Backup Volume**:
  - Volume mounted at `/backup`
  - Persisted in `/etc/fstab`
- ✅ **Database Backup**:
  - File created: `/backup/notes_backup.sql`
- ✅ **Documentation**:
  - Full setup steps included in this `README.md` file.

