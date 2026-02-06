from bs4 import BeautifulSoup
import csv
import re

def parse_html(file_path, output_csv):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        publications = []

        # Find all publication items
        # The class name is quite long, let's look for the base class
        # Based on the user provided HTML snippet, items are in 'nova-legacy-v-publication-item'
        items = soup.find_all('div', class_=lambda x: x and 'nova-legacy-v-publication-item' in x)

        seen_titles = set()
        unique_publications = []

        for item in items:
            # Title and Link
            title_div = item.find('div', itemprop='headline')
            if not title_div:
                title_div = item.find('div', class_=lambda x: x and 'publication-item__title' in x)
            
            if not title_div:
                continue
                
            link_tag = title_div.find('a')
            title = link_tag.get_text(strip=True) if link_tag else title_div.get_text(strip=True)
            
            # Deduplication check
            if title in seen_titles:
                continue
            seen_titles.add(title)

            link = ""
            if link_tag and link_tag.has_attr('href'):
                href = link_tag['href']
                if href.startswith('http'):
                    link = href
                else:
                    link = "https://www.researchgate.net" + href

            # Type and Date (Meta)
            # Example structure: <div class="nova-legacy-v-publication-item__meta"><span class="nova-legacy-e-badge">Article</span><span>Jan 2026</span></div>
            meta_div = item.find('div', class_=lambda x: x and 'publication-item__meta' in x)
            pub_type = "Publication"
            pub_date = ""
            
            if meta_div:
                # Type is often in a badge
                badge = meta_div.find('span', class_=lambda x: x and 'badge' in x)
                if badge:
                    pub_type = badge.get_text(strip=True)
                
                # Date is often the text after the badge
                # We get all text lines
                text_content = meta_div.get_text(separator='|', strip=True).split('|')
                # Filter out the type
                dates = [t for t in text_content if t != pub_type]
                if dates:
                    pub_date = dates[0] # Usually the first thing after type is date

            # Authors
            # Usually in a person-list
            authors = []
            person_list = item.find('ul', class_=lambda x: x and 'person-list' in x)
            if person_list:
                for person in person_list.find_all('li'):
                    authors.append(person.get_text(strip=True))
            
            # If no list, try finding the person list container generally
            if not authors:
                 person_stack = item.find('div', class_=lambda x: x and 'person-list' in x)
                 if person_stack:
                     authors = [p.get_text(strip=True) for p in person_stack.find_all('a')]

            authors_str = ", ".join(authors) if authors else "Saba Irshad et al."

            # Abstract
            # Look for description
            abstract_div = item.find('div', class_=lambda x: x and 'description' in x)
            abstract = abstract_div.get_text(strip=True) if abstract_div else ""
            
            # Clean up abstract if it starts with "Background" or similar repetitive headers if needed
            # For now, raw extraction is safer.

            publications.append({
                'Title': title,
                'Link': link,
                'Authors': authors_str,
                'Date': pub_date,
                'Type': pub_type,
                'Abstract': abstract
            })

        # Write to CSV
        keys = ['Title', 'Authors', 'Date', 'Type', 'Link', 'Abstract']
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(publications)
            
        print(f"Extracted {len(publications)} publications to {output_csv}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import os
    # Determine if running from root or data_extraction
    if os.path.exists("data_extraction/source.html"):
        src = "data_extraction/source.html"
        dst = "data_extraction/publications.csv"
    elif os.path.exists("source.html"):
        src = "source.html"
        dst = "publications.csv"
    else:
        print("Could not find source.html")
        exit(1)
        
    parse_html(src, dst)
