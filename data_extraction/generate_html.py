import csv

def csv_to_html(csv_file, output_file):
    html_content = ""
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                html_content += f"""
                <div class="card publication-card" style="margin-bottom: 20px;">
                    <h3>{row['Title']}</h3>
                    <p><strong>Authors:</strong> {row['Authors']}</p>
                    <p><strong>Date:</strong> {row['Date']} <span style="margin-left: 10px; background: var(--md-sys-color-secondary-container); color: var(--md-sys-color-on-secondary-container); padding: 2px 8px; border-radius: 4px; font-size: 0.8em;">{row['Type']}</span></p>
                    <p><em>{row['Abstract']}</em></p>
                    <a href="{row['Link']}" target="_blank" class="btn btn-primary" style="font-size: 0.9rem; padding: 8px 16px;">View Paper</a>
                </div>
                """
        
        # Read the existing HTML template
        with open(output_file, 'r', encoding='utf-8') as f:
            template = f.read()
            
        # Replace the placeholder content
        # We'll look for the card-grid div content
        start_marker = '<div class="card-grid" style="display: block;">'
        end_marker = '<!-- Publications List -->'
        
        # Simple replacement for now, aiming to inject into the specific area
        # Ideally we'd parse the HTML, but string replacement works for this controlled file
        
        # Let's just create a fragment file that the user can verify or we can manually inject
        # Actually, let's rewrite the whole file with the new content injected
        
        new_html = template.replace(
            '<!-- Publications List -->', 
            html_content
        )
        
        # Write back
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_html)
            
        print("HTML updated successfully.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    csv_to_html("data_extraction/publications.csv", "website/publications.html")
