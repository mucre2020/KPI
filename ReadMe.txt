Project Summary: KPI Dashboard App
This Django-based KPI Dashboard app, developed for the Rwanda Forensic Institute, provides a platform to track and visualize Key Performance Indicators (KPIs) for forensic units. The app supports role-based access, data uploads, and interactive visualizations, enabling users to monitor case metrics efficiently.
Key Features Implemented
1. Role-Based Dashboard
Role-Based Access: Implemented user roles (Admin, Director General, Director, Division Manager) with tailored views:
Admins can upload KPI data.

Division Managers see data for their division only.

Directors and Director General have access to all data.

Dynamic Metrics: Displays key metrics (Cases Received, Cases Reported, Total Amount, Resolution Rate) based on the user’s role and applied filters.

2. Professional Login Page
Design: Created a clean, centered login page with the Rwanda Forensic Institute logo, styled using Tailwind CSS.

Functionality: Includes username and password fields, error messaging for invalid credentials, and a redirect to the dashboard upon successful login.

3. Data Upload and Download
Excel Upload: Admins can upload KPI data via Excel files, which are processed using pandas and saved to the database (KPI model).

CSV Download: Users can download a summary of KPIs (Cases Received, Cases Reported, Resolution Rate, Total Amount) as a CSV file.

4. Interactive Dashboard with Filters
Filter Form: Added a filter form to refine data by Year, Month, Division, and Unit, improving data granularity.

Responsive Design: Used Tailwind CSS for a modern, responsive layout that works on desktop and mobile devices.

5. Enhanced Data Visualization
Initial Charts:
Resolution Rate Overview: A bar chart showing the average resolution rate, color-coded (green for ≥75%, red for <75%).

Cases by Unit: A bar chart comparing Cases Received and Reported across units, with a horizontal scrollbar for large datasets.

Chart Improvements:
Fixed scrolling issues by setting consistent chart heights (300px for Resolution Rate, 400px for Cases by Unit) and adding horizontal scrolling for wide charts.

Added smaller font sizes for x-axis labels to reduce clutter.

New Charts:
Cases Trend Over Time: A line chart showing trends of Cases Received and Reported across months.

Cases by Division: A pie chart displaying the distribution of Cases Received across divisions (e.g., Biology, Chemistry).

Interactivity:
Added tooltips to all charts, showing detailed data on hover (e.g., "Cases Received: 85").

Implemented drill-down functionality for the "Cases by Unit" chart: clicking a bar redirects to a detailed view showing a monthly breakdown for the selected unit.

Chart Export: Added a "Download Chart" button for each chart, allowing users to export charts as PNG images using html2canvas.

6. Bug Fixes and Improvements
Syntax Errors: Fixed a SyntaxError in forms.py caused by a mismatched parenthesis in the FilterForm initialization.

KeyError Fix: Resolved a KeyError: 'unit' by adding the unit field to FilterForm and ensuring the view handles it correctly.

Template Syntax Error: Fixed an Unclosed tag 'block' error in dashboard.html by ensuring all {% block %} tags are properly closed.

Scrolling Issues: Addressed excessive scrolling in charts by setting fixed heights and adding horizontal scrollbars where needed.

7. Code Structure
Models: Defined Division, Unit, KPI, and UserProfile models to store data and user roles.

Views: Implemented dashboard, upload_excel, download_summary, and unit_details views to handle core functionality.

Templates: Created base.html, dashboard.html, login.html, upload.html, and unit_details.html with a consistent design using Tailwind CSS.

Forms: Added ExcelUploadForm for uploads and FilterForm for filtering data.

Future Improvements
Data Table View: Add a sortable, paginated table to display raw KPI data.

Notifications: Implement alerts for low resolution rates (e.g., <75%).

PDF Reports: Allow users to download a PDF report with charts and metrics.

Predictive Analytics: Use machine learning to predict future case volumes or resolution rates.

Technologies Used
Backend: Django 5.1.4, Python 3.12

Frontend: Tailwind CSS, Chart.js, html2canvas

Database: SQLite (default, can be swapped for PostgreSQL)

Dependencies: pandas (for Excel processing)

The app is hosted locally at http://127.0.0.1:8000/ during development. Below are the key URLs, their purposes, and the associated views.

## Important URLs

Below are the key URLs for navigating the KPI Dashboard app:

| URL                          | Name                  | Description                                                                 | Access Requirements         |
|------------------------------|-----------------------|-----------------------------------------------------------------------------|-----------------------------|
| `/`                          | `dashboard`           | Main dashboard with KPIs, filters, and charts.                              | Requires login (all roles)  |
| `/login/`                    | `login`               | Login page for user authentication.                                         | Public                      |
| `/logout/`                   | `logout`              | Logs out the current user.                                                  | Requires login              |
| `/upload/`                   | `upload_excel`        | Upload KPI data via Excel (admins only).                                    | Requires login (Admin only) |
| `/download/`                 | `download_summary`    | Download a CSV summary of KPIs.                                             | Requires login (all roles)  |
| `/unit-details/`             | `unit_details`        | Detailed monthly breakdown for a selected unit (via drill-down).            | Requires login (all roles)  |
| `/admin/`                    | N/A                   | Django admin panel for managing data.                                       | Requires superuser access   |

admin role
user : mupenziii
pw: RFL@2o2o

dg role
user: dg
pw: Test@123

division role
BDM1
Test@123

Director

Dna 
Test@123