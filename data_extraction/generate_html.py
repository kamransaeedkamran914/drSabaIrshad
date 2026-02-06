import csv
import os
from bs4 import BeautifulSoup

def csv_to_html(csv_file, html_file):
    try:
        # Check files
        if not os.path.exists(csv_file):
            print(f"CSV file not found: {csv_file}")
            return
        if not os.path.exists(html_file):
            print(f"HTML file not found: {html_file}")
            return

        # Generate HTML cards
        cards_html = ""
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check for empty fields to avoid "None" or weird display
                title = row.get('Title', 'Untitled')
                authors = row.get('Authors', '')
                date = row.get('Date', '')
                pub_type = row.get('Type', '')
                abstract = row.get('Abstract', '')
                link = row.get('Link', '#')
                
                # Truncate abstract if too long
                if len(abstract) > 300:
                    abstract = abstract[:300] + "..."

                card = f"""
                <div class="card publication-card" style="margin-bottom: 20px;">
                    <h3>{title}</h3>
                    <p><strong>Authors:</strong> {authors}</p>
                    <p><strong>Date:</strong> {date} <span style="margin-left: 10px; background: var(--md-sys-color-secondary-container); color: var(--md-sys-color-on-secondary-container); padding: 2px 8px; border-radius: 4px; font-size: 0.8em;">{pub_type}</span></p>
                    <p><em>{abstract}</em></p>
                    <a href="{link}" target="_blank" class="btn btn-primary" style="font-size: 0.9rem; padding: 8px 16px;">View Paper</a>
                </div>
                """
                cards_html += card

        # Update HTML file
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Find the container
        container = soup.find('div', class_='card-grid')
        if container:
            # Clear existing content
            container.clear()
            # Insert new content (need to parse the new string as soup objects or insert as HTML)
            # BeautifulSoup 4 can handle string insertion if we parse it first or use append
            new_content_soup = BeautifulSoup(cards_html, 'html.parser')
            container.append(new_content_soup)
            
            # Write back
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Successfully updated {html_file} with publications.")
        else:
            print("Could not find div with class 'card-grid' in HTML.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Handle paths relative to where script is run
    import os
    base_dir = os.getcwd()
    
    # Assumptions: 
    # if run from data_extraction: csv is ./publications.csv, html is ../website/publications.html
    # if run from root: csv is data_extraction/publications.csv, html is website/publications.html
    
    if os.path.exists("publications.csv"):
        csv_path = "publications.csv"
        html_path = "../website/publications.html"
    elif os.path.exists("data_extraction/publications.csv"):
        csv_path = "data_extraction/publications.csv"
        html_path = "website/publications.html"
    else:
        print("Could not locate publications.csv")
        exit(1)
        
    csv_to_html(csv_path, html_path)
