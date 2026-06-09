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
        @page {{
          size: A4;
          margin: 22mm 18mm;
        }}
        body {{
          font-family: Arial, sans-serif;
          font-size: 10.5pt;
          line-height: 1.45;
          color: #222;
        }}
        h1, h2, h3 {{
          color: #111;
        }}
        h1 {{
          font-size: 20pt;
          margin-bottom: 18px;
          border-bottom: 1px solid #ccc;
          padding-bottom: 8px;
        }}
        h2 {{
          font-size: 14pt;
          margin-top: 22px;
          margin-bottom: 10px;
          page-break-after: avoid;
        }}
        h3 {{
          font-size: 11.5pt;
          margin-top: 14px;
          margin-bottom: 8px;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
          margin: 10px 0 16px 0;
        }}
        th, td {{
          border: 1px solid #ccc;
          padding: 6px 8px;
          vertical-align: top;
        }}
        th {{
          background: #f2f2f2;
          font-weight: bold;
        }}
        ul, ol {{
          margin-top: 6px;
          margin-bottom: 10px;
          padding-left: 22px;
        }}
        li {{
          margin-bottom: 3px;
        }}
        p {{
          margin: 0 0 8px 0;
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
