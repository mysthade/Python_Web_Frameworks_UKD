from datetime import datetime
from pathlib import Path

from fpdf import FPDF

from models.user import User


def generate_users_report(users: list[User]) -> Path:
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"users_report_{timestamp}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Users Report", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(
        0, 8, f"Generated at: {datetime.now().isoformat(sep=' ', timespec='seconds')}"
    )
    pdf.ln(10)

    if not users:
        pdf.cell(0, 10, "No users found", new_x="LMARGIN", new_y="NEXT")
    else:
        for user in users:
            line = (
                f"ID: {user.id} | Name: {user.name} | "
                f"Email: {user.email} | Role: {user.role.value}"
            )
            pdf.multi_cell(0, 8, line)

    pdf.output(str(report_path))
    return report_path
