from io import BytesIO
from flask import Flask, render_template, request, send_file
from playwright.sync_api import sync_playwright

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def form():
    # Show the main form page where users enter their CV information
    return render_template('form.html')


@app.route('/download', methods=['POST'])
def download_pdf():
    # 1. Collect personal information from the submitted form
    cv_data = {
        'name': request.form.get('name', ''),
        'phone': request.form.get('phone', ''),
        'email': request.form.get('email', ''),
        'linkedin': request.form.get('linkedin', ''),
        'skills': request.form.get('skills', ''),
    }

    # 2. Collect education history
    # Forms send lists of inputs (like multiple degrees), so we group them together
    education_list = []
    degrees = request.form.getlist('edu_degree[]')
    schools = request.form.getlist('edu_org[]')
    edu_dates = request.form.getlist('edu_dates[]')
    grades = request.form.getlist('edu_grade[]')
    
    for i in range(len(degrees)):
        # Only add an entry if a degree title was actually provided
        if degrees[i].strip():
            education_list.append({
                'degree': degrees[i].strip(),
                'org': schools[i].strip() if i < len(schools) else '',
                'dates': edu_dates[i].strip() if i < len(edu_dates) else '',
                'grade': grades[i].strip() if i < len(grades) else ''
            })
    cv_data['education'] = education_list

    # 3. Collect work experience
    experience_list = []
    roles = request.form.getlist('exp_role[]')
    companies = request.form.getlist('exp_org[]')
    exp_dates = request.form.getlist('exp_dates[]')
    exp_descriptions = request.form.getlist('exp_desc[]')
    
    for i in range(len(roles)):
        if roles[i].strip():
            raw_desc = exp_descriptions[i] if i < len(exp_descriptions) else ''
            # Break the description into separate lines/bullet points
            desc_lines = [line.strip() for line in raw_desc.split('\n') if line.strip()]
            
            experience_list.append({
                'role': roles[i].strip(),
                'org': companies[i].strip() if i < len(companies) else '',
                'dates': exp_dates[i].strip() if i < len(exp_dates) else '',
                'description': desc_lines
            })
    cv_data['experience'] = experience_list

    # 4. Collect project highlights
    projects_list = []
    project_titles = request.form.getlist('proj_title[]')
    project_dates = request.form.getlist('proj_dates[]')
    project_descriptions = request.form.getlist('proj_desc[]')
    
    for i in range(len(project_titles)):
        if project_titles[i].strip():
            raw_desc = project_descriptions[i] if i < len(project_descriptions) else ''
            # Break the description into separate lines/bullet points
            desc_lines = [line.strip() for line in raw_desc.split('\n') if line.strip()]
            
            projects_list.append({
                'title': project_titles[i].strip(),
                'dates': project_dates[i].strip() if i < len(project_dates) else '',
                'description': desc_lines
            })
    cv_data['projects'] = projects_list

    # 5. Bring the data and the template together to create HTML
    rendered_cv_html = render_template('cv_template.html', **cv_data)
    
    # 6. Convert the HTML to a PDF using a headless browser (Playwright)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Load our HTML into the page
        page.set_content(rendered_cv_html)
        
        # Tell the browser we want to format for printing
        page.emulate_media(media="print")
        
        # Create the actual PDF bytes
        pdf_file = page.pdf(print_background=True, format="A4", prefer_css_page_size=True)
        
        # Always remember to close the browser
        browser.close()
    
    # 7. Decide on a suitable filename based on the person's name
    safe_name = cv_data['name'].replace(' ', '_') if cv_data['name'] else 'CV'
    download_filename = f"{safe_name}_CV.pdf"

    # 8. Send the PDF back to the user's browser
    return send_file(
        BytesIO(pdf_file),
        download_name=download_filename,
        as_attachment=False,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    # Start the server on port 5000
    app.run(debug=False, port=5000)
