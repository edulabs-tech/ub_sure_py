css = """
.rtl {
    direction: rtl;
    text-align: right;
}
"""

def build_source_html(source_url, index, name_of_the_link, page, total_pages, start_line, end_line, joined_fields):
    html = (
        f'<div style="direction: rtl; text-align: right; white-space: pre-line; font-size: 0.75em;">'
        f'  <div>'
        f'    <a href="{source_url}" style="color: blue; text-decoration: none;">[{index}]</a> '
        f'    <a href="{source_url}" style="color: blue; text-decoration: none;">{name_of_the_link}</a>'
        f'  </div>'
        f'  <div>'
        f'    עמוד {page} מתוך {total_pages}, שורות {start_line}-{end_line}.'
        f'  </div>'
        f'  <div>{joined_fields}</div>'
        f'</div>'
    )
    return html

def format_source(doc, index):
    md = doc.metadata
    company = md.get('companyName', 'Unknown')
    doc_type = md.get('docType', 'Unknown')
    insurance_type = md.get('insuranceType', 'Unknown')
    coverage_type = md.get('coverageType', 'Unknown')
    category = md.get('docCategory', 'Unknown')
    sub_category = md.get('docSubCategory', 'Unknown')
    page = md.get('page', 'Unknown')
    total_pages = md.get('totalPages', 'Unknown')

    try:
        page = int(page) + 1
    except (ValueError, TypeError):
        # If page is not a number, it will remain unchanged (or you can handle it as needed)
        pass


    loc = md.get('loc', {})
    lines = loc.get('lines', {})
    start_line = lines.get('from', 'Unknown')
    end_line = lines.get('to', 'Unknown')

    source_url = md.get('source', '#')
    name_of_the_link = source_url.split("/")[-1]

    fields = [company]
    if doc_type != "Unknown":
        fields.append(doc_type)
    if insurance_type != "Unknown":
        fields.append(insurance_type)
    if coverage_type != "Unknown":
        fields.append(coverage_type)
    if category != "Unknown":
        fields.append(category)
    if sub_category != "Unknown":
        fields.append(sub_category)

    joined_fields = " | ".join(fields)

    ret_html = build_source_html(source_url, index, name_of_the_link, page, total_pages, start_line, end_line, joined_fields)

    # Return an HTML snippet:
    # The clickable number is in blue on its own line.
    return ret_html


source_separator = "\n\n---------מקורות----------\n"

