# Learning Management System (LMS) with Attendance Management

This project is a full-stack Learning Management System (LMS) with integrated attendance management. It is built using modern web technologies to provide a seamless experience for both educators and students.

## Features

- **Course Management**: Create, update, and delete courses.
- **User Roles**: Differentiate between administrators, instructors, and students.
- **Attendance Tracking**: Automatically track and manage student attendance.
- **Responsive Design**: Built with a mobile-first approach using Tailwind CSS.
- **Modern UI**: Utilizes ShadcnUI components for a sleek and intuitive user interface.
- **Type Safety**: Frontend built with TypeScript for improved developer experience and code reliability.
- **Scalable Backend**: Powered by Django, ensuring robust and scalable server-side operations.
- **Database**: Uses PostgreSQL for reliable and efficient data storage.

## Technologies Used

### Frontend
- **Next.js**: A React framework for server-side rendering and static site generation.
- **TypeScript**: Adds static types to JavaScript, improving code quality and understanding.
- **ShadcnUI**: A collection of beautifully designed, accessible, and customizable UI components.
- **Tailwind CSS**: A utility-first CSS framework for rapidly building custom user interfaces.

### Backend
- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **PostgreSQL**: A powerful, open-source object-relational database system.

## Getting Started

### Prerequisites

- Node.js and npm installed on your machine.
- Python 3.x installed on your machine.
- PostgreSQL installed and running.

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/UBITians/learning-management-system.git
cd learning-management-system
```

2. **Install dependencies**
   ```bash
   cd frontend
   npm install
   cd ../backend
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**
   ```bash
   cp .env.example .env.local
   ```

4. **Run the development server**
   ```bash
   cd frontend
   npm run dev
   cd ../backend
   python manage.py runserver
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:3000` to access the application.
