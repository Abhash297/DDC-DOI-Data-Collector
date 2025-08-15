from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import requests
import pandas as pd
import time
from itertools import islice
import io
import os
from datetime import datetime

app = Flask(__name__)

# Split a list into chunks of specified size
def chunk_list(iterable, size):
    it = iter(iterable)
    while True:
        chunk = list(islice(it, size))
        if not chunk:
            break
        yield chunk

# Clean DOI strings by removing common prefixes
def clean_doi(doi):
    prefixes_to_remove = [
        "https://doi.org/",
        "http://doi.org/",
        "doi.org/",
        "DOI:",
        "doi:",
        "https://dx.doi.org/",
        "http://dx.doi.org/",
    ]

    cleaned_doi = doi.strip()
    for prefix in prefixes_to_remove:
        if cleaned_doi.startswith(prefix):
            cleaned_doi = cleaned_doi[len(prefix) :]
            break

    return cleaned_doi

# Fetch publication metadata from OpenAlex API with retry mechanism
def get_publication_data(dois, retries=3, delay=5):
    all_results = []
    cleaned_dois = [clean_doi(doi) for doi in dois]
    
    for chunk in chunk_list(cleaned_dois, 50):
        pipe_separated_dois = "|".join(chunk)
        url = f"https://api.openalex.org/works?filter=doi:{pipe_separated_dois}&per-page=50"

        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    results = response.json().get("results", [])
                    all_results.extend(results)
                    break
                else:
                    time.sleep(delay)
            except requests.exceptions.RequestException as e:
                time.sleep(delay)

    return all_results

# Extract grant information from publication data safely
def extract_grants(publication):
    grants_extracted = []
    grants_data = publication.get("grants", [])

    if not isinstance(grants_data, list):
        return grants_extracted

    for grant in grants_data:
        if not isinstance(grant, dict):
            continue

        funder_info = grant.get("funder", {})
        if not isinstance(funder_info, dict):
            continue

        grants_extracted.append(
            {
                "funder": funder_info.get("display_name", None),
                "funder_id": funder_info.get("id", None),
                "award_id": grant.get("award_id", None),
            }
        )

    return grants_extracted

# Extract keywords as a list of display names
def extract_keywords(publication):
    kw_data = publication.get("keywords", [])
    if not isinstance(kw_data, list):
        return []

    keywords_list = []
    for kw in kw_data:
        if isinstance(kw, dict):
            display_name = kw.get("display_name")
            if display_name:
                keywords_list.append(display_name)

    return keywords_list

# Extract venue information from publication data
def extract_venue_info(publication):
    """Extract just the venue name/publication venue."""
    host_venue = publication.get("host_venue", {})
    primary_location = publication.get("primary_location", {})
    
    # Try host_venue first, then primary_location as fallback
    venue_data = host_venue if host_venue else primary_location
    
    if not isinstance(venue_data, dict):
        return None
    
    # Get venue name from display_name or source display_name
    venue_name = venue_data.get("display_name")
    if not venue_name:
        source_info = venue_data.get("source", {})
        if isinstance(source_info, dict):
            venue_name = source_info.get("display_name")
    
    return venue_name

# Country code to country name mapping
COUNTRY_CODE_TO_NAME = {
    "US": "USA",
    "GB": "United Kingdom",
    "CA": "Canada",
    "DE": "Germany",
    "FR": "France",
    "AU": "Australia",
    "JP": "Japan",
    "CN": "China",
    "IN": "India",
    "BR": "Brazil",
    "IT": "Italy",
    "ES": "Spain",
    "NL": "Netherlands",
    "SE": "Sweden",
    "CH": "Switzerland",
    "NP": "Nepal",
}

# Extract relevant metadata from publication list
def extract_publication_data(publication_data):
    publication_rows = []

    for publication in publication_data:
        authorships = publication.get("authorships", [])
        if not isinstance(authorships, list):
            continue

        keywords_list = extract_keywords(publication)
        venue_name = extract_venue_info(publication)

        all_authors = []
        all_affiliations = []
        all_countries = []

        for author in authorships:
            author_name = author.get("author", {}).get("display_name", None)
            if author_name:
                all_authors.append(author_name)

            author_affiliation = ""
            author_country = ""

            institution_info = author.get("institutions")
            if (
                institution_info
                and isinstance(institution_info, list)
                and len(institution_info) > 0
            ):
                primary_inst = institution_info[0]
                if isinstance(primary_inst, dict):
                    aff = primary_inst.get("display_name")
                    if aff:
                        author_affiliation = aff

                    ctry_code = primary_inst.get("country_code")
                    if ctry_code:
                        ctry_name = COUNTRY_CODE_TO_NAME.get(ctry_code, ctry_code)
                        author_country = ctry_name

            all_affiliations.append(author_affiliation)
            all_countries.append(author_country)

        publication_row = {
            "id": publication.get("id", None),
            "title": publication.get("title", None),
            "display_name": publication.get("display_name", None),
            "all_authors": "; ".join(all_authors) if all_authors else "",
            "all_affiliations": "; ".join(all_affiliations) if all_affiliations else "",
            "all_countries": "; ".join(all_countries) if all_countries else "",
            "doi": publication.get("doi", None),
            "publication_date": publication.get("publication_date", None),
            "publication_year": publication.get("publication_year", None),
            "type": publication.get("type", None),
            "language": publication.get("language", None),
            "venue": venue_name,
            "open_access": publication.get("open_access", {}).get("is_oa", None),
            "open_access_status": publication.get("open_access", {}).get("oa_status", None),
            "open_access_url": publication.get("open_access", {}).get("oa_url", None),
            "cited_by_count": publication.get("cited_by_count", None),
            "keywords": "; ".join(keywords_list) if keywords_list else "",
            "grants": (
                "; ".join(
                    [
                        grant.get("funder", "")
                        for grant in extract_grants(publication)
                        if grant.get("funder")
                    ]
                )
                if extract_grants(publication)
                else ""
            ),
        }

        publication_rows.append(publication_row)

    return publication_rows

# Order DataFrame according to original DOI list and handle missing entries
def order_by_doi_sequence(df, original_dois):
    cleaned_original_dois = [clean_doi(doi) for doi in original_dois]

    if df.empty:
        na_rows = [
            {
                "id": "N/A",
                "title": "N/A",
                "display_name": "N/A",
                "all_authors": "N/A",
                "all_affiliations": "N/A",
                "all_countries": "N/A",
                "doi": f"https://doi.org/{doi}",
                "publication_date": "N/A",
                "publication_year": "N/A",
                "type": "N/A",
                "language": "N/A",
                "venue": "N/A",
                "open_access": "N/A",
                "open_access_status": "N/A",
                "open_access_url": "N/A",
                "cited_by_count": "N/A",
                "keywords": "N/A",
                "grants": "N/A",
            }
            for doi in cleaned_original_dois
        ]
        return pd.DataFrame(na_rows)

    def extract_doi_from_url(doi_url):
        if pd.isna(doi_url) or not doi_url:
            return ""
        return (
            doi_url.replace("https://doi.org/", "")
            if doi_url.startswith("https://doi.org/")
            else doi_url
        )

    found_dois = set(extract_doi_from_url(doi) for doi in df["doi"])

    missing_dois = [doi for doi in cleaned_original_dois if doi not in found_dois]

    na_rows = [
        {
            "id": "N/A",
            "title": "N/A",
            "display_name": "N/A",
            "all_authors": "N/A",
            "all_affiliations": "N/A",
            "all_countries": "N/A",
            "doi": f"https://doi.org/{doi}",
            "publication_date": "N/A",
            "publication_year": "N/A",
            "type": "N/A",
            "language": "N/A",
            "venue": "N/A",
            "open_access": "N/A",
            "open_access_status": "N/A",
            "open_access_url": "N/A",
            "cited_by_count": "N/A",
            "keywords": "N/A",
            "grants": "N/A",
        }
        for doi in missing_dois
    ]

    df_with_na = (
        pd.concat([df, pd.DataFrame(na_rows)], ignore_index=True) if na_rows else df
    )

    doi_to_order = {doi: i for i, doi in enumerate(cleaned_original_dois)}

    df_with_na["doi_order"] = df_with_na["doi"].apply(
        lambda x: doi_to_order.get(extract_doi_from_url(x), 999999)
    )

    df_ordered = (
        df_with_na.sort_values("doi_order")
        .drop(columns=["doi_order"])
        .reset_index(drop=True)
    )

    return df_ordered

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

@app.route('/extract', methods=['POST'])
def extract_metadata():
    try:
        data = request.get_json()
        dois = data.get('dois', [])
        
        if not dois:
            return jsonify({'error': 'No DOIs provided'}), 400
        
        # Clean and validate DOIs
        cleaned_dois = []
        for doi in dois:
            cleaned = clean_doi(doi.strip())
            if cleaned:
                cleaned_dois.append(cleaned)
        
        if not cleaned_dois:
            return jsonify({'error': 'No valid DOIs found'}), 400
        
        # Fetch publication data
        publication_data = get_publication_data(cleaned_dois)
        
        if not publication_data:
            # Create N/A rows for all DOIs
            df_final = order_by_doi_sequence(pd.DataFrame(), cleaned_dois)
        else:
            records = extract_publication_data(publication_data)
            df = pd.DataFrame(records)
            
            # Remove duplicates
            seen_ids = set()
            indices_to_keep = [
                i
                for i, pub_id in enumerate(df["id"])
                if not (pub_id in seen_ids or seen_ids.add(pub_id))
            ]
            
            df_deduplicated = df.iloc[indices_to_keep].reset_index(drop=True)
            df_final = order_by_doi_sequence(df_deduplicated, cleaned_dois)
        
        # Convert to JSON for preview
        results = df_final.to_dict('records')
        
        return jsonify({
            'success': True,
            'results': results,
            'total_publications': len(df_final),
            'message': f'Successfully processed {len(cleaned_dois)} DOIs'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_csv():
    try:
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({'error': 'No data to download'}), 400
        
        # Create DataFrame and CSV
        df = pd.DataFrame(results)
        
        # Ensure exact column order matching the original CSV format
        column_order = [
            'id', 'title', 'display_name', 'all_authors', 'all_affiliations', 
            'all_countries', 'doi', 'publication_date', 'publication_year', 
            'type', 'language', 'venue', 'open_access', 'open_access_status', 
            'open_access_url', 'cited_by_count', 'keywords', 'grants'
        ]
        
        # Reorder columns and fill any missing columns with N/A
        for col in column_order:
            if col not in df.columns:
                df[col] = 'N/A'
        
        df = df[column_order]
        
        # Create CSV in memory
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"publication_metadata_{timestamp}.csv"
        
        # Create response
        response = io.BytesIO()
        response.write(output.getvalue().encode('utf-8'))
        response.seek(0)
        
        return send_file(
            response,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
