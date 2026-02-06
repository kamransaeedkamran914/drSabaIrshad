import requests
from bs4 import BeautifulSoup
import time

def extract_publications(profile_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(profile_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page: {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.content, 'html.parser')
        publications = []
        
        # This is a generic scraper based on common RG structures. 
        # Since RG is dynamic, we look for publication items.
        # Note: Actual class names on RG are often obfuscated or dynamic.
        # We will look for common patterns in publication lists.
        
        # Searching for publication items
        # ResearchGate often uses specific containers for research items
        
        # Try to find the section with publications
        # In a real scenario, RG is hard to scrape due to anti-bot. 
        # We will simulate the extraction based on the user's request context 
        # if the direct scrape fails or is blocked, but let's try a best-effort parse.
        
        # Look for typical article containers
        articles = soup.find_all('div', class_=lambda x: x and 'nova-legacy-c-card' in x)
        
        if not articles:
             # Fallback to finding anything that looks like a title
             # This is a broad search for h2/h3 elements which often hold titles
             articles = soup.find_all(['div', 'a'], class_=lambda x: x and ('publication-item' in x or 'research-item' in x))

        for article in articles:
            # Extract Title
            title_elem = article.find(['a', 'div'], class_=lambda x: x and 'title' in x.lower())
            if not title_elem:
                continue
                
            title = title_elem.get_text(strip=True)
            
            # Extract Link
            link = ""
            if title_elem.name == 'a':
                link = "https://www.researchgate.net" + title_elem['href']
            
            # Extract Date/Type if available
            meta_elem = article.find('div', class_=lambda x: x and 'meta' in x.lower())
            meta = meta_elem.get_text(strip=True) if meta_elem else "Unknown Date"
            
            # Extract Abstract (snippet)
            abstract_elem = article.find('div', class_=lambda x: x and 'abstract' in x.lower())
            abstract = abstract_elem.get_text(strip=True) if abstract_elem else ""
            
            publications.append({
                'title': title,
                'link': link,
                'meta': meta,
                'abstract': abstract
            })
            
        return publications

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def save_to_markdown(publications, filename="publications.md"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Dr. Saba Irshad - Publications List\n\n")
        
        if not publications:
            f.write("No publications could be automatically extracted. Please manually verify the source or use the provided data.\n")
            # Since live scraping RG is difficult due to auth/anti-bot, 
            # I will output a template structure based on the USER's provided text snippet 
            # if the scrape returns nothing.
            f.write("\n## Extracted/Simulated Data based on User Input\n")
            
            # Simulated data from user prompt to ensure we have content
            data = [
                {
                    "title": "Novel mega-deletion in BFSP1 causing autosomal recessive juvenile cataract in a Pakistani consanguineous family",
                    "date": "Jan 2026",
                    "type": "Article",
                    "authors": "Neelam Saba, Ambreen Kanwal, Saba Irshad",
                    "abstract": "Background Juvenile cataract is characterized by the blurredness in eye lens which develops typically before the age of 18 years. Objective of the study was to delineate the underlying causative genetic defect for autosomal recessive juvenile cataract (ARJC) in an affected consanguineous multiplex, multigenerational Pakistani consanguineous family...",
                    "link": "https://www.researchgate.net/profile/Saba-Irshad-2"
                },
                 {
                    "title": "Pedigree of the family PK-CC6 with isoforms, ideogram, and gel bands...",
                    "date": "Unknown",
                    "type": "Data",
                    "authors": "Saba Irshad et al.",
                    "abstract": "",
                    "link": "https://www.researchgate.net/profile/Saba-Irshad-2"
                },
                 {
                    "title": "Structural modeling, exonic organization and predicted protein...",
                    "date": "Unknown",
                    "type": "Data",
                    "authors": "Saba Irshad et al.",
                    "abstract": "",
                    "link": "https://www.researchgate.net/profile/Saba-Irshad-2"
                },
                {
                    "title": "Traditional medicinal plants have served as crucial therapeutic agents for managing hypertension",
                    "date": "Unknown",
                    "type": "Article",
                    "authors": "Saba Irshad et al.",
                    "abstract": "Traditional medicinal plants have served as crucial therapeutic agents for managing hypertension, particularly in resource-constrained regions across the globe...",
                    "link": "https://www.researchgate.net/lab/Saba-Irshad-Lab"
                },
                {
                     "title": "Comparative study of nutritional status, minerals and heavy metals contents in tetra pack branded milk samples with fresh milk from selected milk producing animals",
                     "date": "2019",
                     "type": "Article",
                     "authors": "Batool, T., ... Saba Irshad, et al.",
                     "abstract": "",
                     "link": ""
                },
                {
                    "title": "In-Vitro Antibacterial Studies",
                    "date": "2011",
                    "type": "Article",
                    "authors": "Jamil, A., & Saba Irshad",
                    "abstract": "",
                    "link": ""
                },
                {
                    "title": "Genetic characterization of Idiopathic Hypogonadotropic Hypogonadism",
                    "date": "2022",
                    "type": "Conference Presentation",
                    "authors": "Saba Irshad",
                    "abstract": "International Seminar on Implementation of Genetic studies for Therapeutic interventions, CEMB, University of the Punjab.",
                    "link": ""
                }
            ]
            
            for pub in data:
                f.write(f"### {pub['title']}\n")
                f.write(f"- **Type:** {pub['type']}\n")
                f.write(f"- **Date:** {pub['date']}\n")
                if pub.get('authors'):
                    f.write(f"- **Authors:** {pub['authors']}\n")
                if pub.get('link'):
                    f.write(f"- **Link:** [View on ResearchGate]({pub['link']})\n")
                if pub.get('abstract'):
                    f.write(f"\n> {pub['abstract']}\n")
                f.write("\n---\n")
            
        else:
            for pub in publications:
                f.write(f"### {pub['title']}\n")
                f.write(f"- **Details:** {pub['meta']}\n")
                f.write(f"- **Link:** [View Publication]({pub['link']})\n")
                if pub['abstract']:
                    f.write(f"\n> {pub['abstract']}\n")
                f.write("\n---\n")

if __name__ == "__main__":
    url = "https://www.researchgate.net/profile/Saba-Irshad-2"
    # Note: Requests to RG will likely be blocked or return partial data without a browser driver.
    # We will attempt it, but fallback to the hardcoded data which is safer for this environment.
    extracted_data = extract_publications(url)
    save_to_markdown(extracted_data, "data_extraction/publications.md")
    print("Markdown generated at data_extraction/publications.md")
