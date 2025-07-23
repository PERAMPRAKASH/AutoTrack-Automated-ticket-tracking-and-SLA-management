# 🛠️ AutoTrack – Automated Ticket Tracking & SLA Management

**AutoTrack** is a full-featured internal ticketing system designed to streamline support workflows within organizations. It offers role-based access, SLA-driven escalation, comment tracking, and automation using Django and MariaDB.

---

## 🔧 Tech Stack

- **Backend**: Django (Python)
- **Database**: MariaDB
- **Authentication**: Custom JWT (Organization, Manager, Employee, Support Agent)
- **Automation**: Cron-based SLA escalation with Django management commands
- **API**: Django REST Framework (DRF)

---

## 🚀 Key Features

- 🔐 Multi-role JWT authentication (`Organization`, `Employee`, `SupportAgent`, `Manager`)
- 📝 Ticket lifecycle: `Open`, `Resolved`, `Closed`
- ⏱️ Automatic ticket escalation to managers if SLA deadlines are breached
- 💬 Role-based commenting on tickets
- 📄 Bulk setup via CSV upload (departments, ticket types)
- 🏢 Organization-specific data isolation for multi-tenant support

---

## 🗂️ Models Overview

### 👥 User Roles

- **Organization**: Manages departments, agents, managers, ticket types
- **Employee**: Raises tickets
- **Support Agent**: Resolves assigned tickets
- **Manager**: Handles escalated tickets

### 🧾 Ticket Flow

- **CreateTicket**: Stores ticket information and metadata
- **Comment**: Tracks communication on tickets by different roles
- **Priority**: Defines SLA durations for escalation
- **Escalation**: Managed via scheduled Django command jobs

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/PERAMPRAKASH/AutoTrack.git
   cd AutoTrack
   
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
3. **Configure the database**
   Update settings.py with your MariaDB credentials:
   ```python
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'autotrack_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
      }
  }


4. **Run migrations and start the server**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   
## Future Enhancements
- Email alerts for SLA violations
- Admin dashboard with ticket metrics
- File attachments on tickets
- Frontend UI (React/Bootstrap)


