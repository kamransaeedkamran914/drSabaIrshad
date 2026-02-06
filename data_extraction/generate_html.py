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
                <div class="card publication-card" style="margin-bottom: 16px; padding: 16px; display: flex; flex-direction: column; gap: 8px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.12); transition: box-shadow 0.2s, transform 0.2s;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
                        <h3 style="font-size: 1.1rem; margin: 0; color: var(--md-sys-color-primary); line-height: 1.4;">{title}</h3>
                        <span style="white-space: nowrap; background: var(--md-sys-color-secondary-container); color: var(--md-sys-color-on-secondary-container); padding: 4px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">{pub_type}</span>
                    </div>
                    
                    <div style="font-size: 0.85rem; color: var(--md-sys-color-on-surface-variant);">
                        <strong>{date}</strong> • {authors}
                    </div>

                    <p style="font-size: 0.9rem; color: var(--md-sys-color-on-surface-variant); margin: 0; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                        {abstract}
                    </p>

                    <div style="margin-top: auto; padding-top: 8px;">
                        <a href="{link}" target="_blank" style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--md-sys-color-primary); text-decoration: none; display: inline-flex; align-items: center; gap: 4px;">
                            Read Paper <i class="fas fa-arrow-right" style="font-size: 0.8em;"></i>
                        </a>
                    </div>
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
