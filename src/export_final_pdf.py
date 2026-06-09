from pathlib import Path

import markdown
from weasyprint import HTML


def export_final_draft_pdf() -> None:
    input_path = Path("outputs/review_drafts/nepal_import_review_final_draft.md")
    output_path = Path("outputs/review_drafts/nepal_import_review_final_draft.pdf")

    markdown_text = input_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(markdown_text, extensions=["extra"])

    html = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{
          font-family: Arial, sans-serif;
          font-size: 11pt;
          line-height: 1.5;
          max-width: 760px;
          margin: 40px auto;
          color: #222;
        }}
        h1, h2, h3 {{
          color: #111;
        }}
        h1 {{
          font-size: 22pt;
          border-bottom: 1px solid #ddd;
          padding-bottom: 8px;
        }}
        h2 {{
          font-size: 15pt;
          margin-top: 28px;
        }}
        li {{
          margin-bottom: 4px;
        }}
        code {{
          font-family: monospace;
        }}
      </style>
    </head>
    <body>
      {html_body}
    </body>
    </html>
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html).write_pdf(output_path)

    print(f"PDF written to {output_path}")


if __name__ == "__main__":
    export_final_draft_pdf()
