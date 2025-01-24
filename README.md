# Placement Portal

## Overview

The Placement Portal is a comprehensive platform designed to streamline and enhance the campus placement process. It facilitates communication and collaboration between three main stakeholders: Admin, Students, and Companies. The portal offers a wide range of features, including role applications, a query system, interview experience submissions, and data analysis of past placement records.

---

## Features

### Admin

1. **Role Management**

   - Approve or reject job roles posted by companies.
   - Manage the list of active roles available for students.

2. **Query Management**

   - Address and resolve queries raised by students and companies.

3. **Placement Analytics**

   - Analyze past placement records to provide insights and trends.
   - Generate detailed reports for institutional evaluation.

4. **Student and Company Management**

   - Maintain and update records of registered students and companies.
   - Approve new accounts and ensure data integrity.

### Student

1. **Job Applications**

   - Browse and apply for various roles posted by companies.
   - Track application statuses and view job descriptions.

2. **Query System**

   - Raise queries related to job roles, the application process, or other placement-related issues.
   - Track query resolution status.

3. **Interview Experiences**

   - Submit detailed interview experiences to guide peers.
   - Browse and learn from shared interview experiences.

4. **Dashboard**

   - View personal placement statistics, such as applied roles and interview outcomes.
   - Access placement analytics and trends.

### Company

1. **Role Posting**

   - Post job openings with detailed descriptions and requirements.
   - View and manage student applications for each role.

2. **Query System**

   - Raise queries regarding the portal, student applications, or placement procedures.
   - Communicate with the admin for issue resolution.

3. **Candidate Evaluation**

   - Shortlist candidates based on application details and attached resumes.
   - Provide feedback on the placement process.

4. **Dashboard**

   - View past placement statistics and role-specific analytics.
   - Monitor active postings and student engagement.

---

## Additional Modules

1. **Interview Experiences**

   - A dedicated section for students to share and explore interview tips, processes, and outcomes.
   - Includes search functionality for easy access to relevant experiences.

2. **Placement Record Analytics**

   - Visual and interactive insights into past placement records.
   - Filters for department, batch, and company-specific data.

3. **Notifications and Alerts**

   - Real-time notifications for updates on job roles, queries, and application statuses.
   - Email alerts for critical updates.

---

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS (TailwindCSS), JavaScript
- **Database:** MySQL
- **Additional Tools:** Chart.js (for data visualization)

---

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/suryaansh001/flask_dbms.git
   cd flask-dbms
   ```

2. Install dependencies:

   ```bash
   pip install -r req.txt
   ```

3. Set up the database:

   - Create a MySQL database and import the schema from `schema.sql`.
   - Update database connection details in the `app.py` file.

4. Run the application:

   ```bash
   python surya.py #student side
   ```

5. Access the portal at `http://127.0.0.1:5000/`.

---

## Future Enhancements

- Integration with third-party platforms for resume building and skill assessments.
- AI-based candidate-job matching.
- Enhanced data analysis.
- Advanced analytics with predictive models for placement trends.
- Mobile app version of the portal.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with detailed information about your changes.

