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
                <div class="card publication-card" style="margin-bottom: 16px; padding: 20px; display: flex; flex-direction: column; gap: 8px; border-radius: 16px; border: 1px solid var(--md-sys-color-outline-variant); box-shadow: none; background: var(--md-sys-color-surface);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
                        <h3 style="font-size: 1.15rem; margin: 0; color: var(--md-sys-color-on-surface); line-height: 1.4; font-weight: 600;">{title}</h3>
                        <span style="white-space: nowrap; background: var(--md-sys-color-secondary-container); color: var(--md-sys-color-on-secondary-container); padding: 4px 10px; border-radius: 8px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">{pub_type}</span>
                    </div>
                    
                    <div class="authors" style="font-size: 0.9rem; color: var(--md-sys-color-primary); font-weight: 500;">
                        {authors}
                    </div>
                    
                    <div style="font-size: 0.85rem; color: var(--md-sys-color-on-surface-variant); margin-bottom: 4px;">
                        <i class="far fa-calendar-alt"></i> {date}
                    </div>

                    <p class="abstract" style="font-size: 0.95rem; color: var(--md-sys-color-on-surface-variant); margin: 0; line-height: 1.6;">
                        {abstract}
                    </p>

                    <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--md-sys-color-surface-variant); display: flex; justify-content: flex-end;">
                        <a href="{link}" target="_blank" style="font-size: 0.9rem; font-weight: 600; color: var(--md-sys-color-primary); text-decoration: none; display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 20px; background: var(--md-sys-color-primary-container);">
                            Read Paper <i class="fas fa-external-link-alt" style="font-size: 0.8em;"></i>
                        </a>
                    </div>
                </div>
                """
                cards_html += card

        # Update HTML file
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Find the container - Updated class name in new template is just 'card-grid' but inside pub-content
        # We need to be careful as BeautifulSoup might not find it if we just search for card-grid if there are multiple
        # In the new layout, it is <div class="card-grid" style="display: block; grid-template-columns: none;">
        
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
