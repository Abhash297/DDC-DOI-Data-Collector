# Publication Metadata Extractor Web Application

A modern web application that extracts comprehensive publication metadata from DOIs using the OpenAlex API. This application replicates the functionality of the original Jupyter notebook but provides a user-friendly web interface.

## Features

- **DOI Input**: Accepts single or multiple DOIs (one per line or comma-separated)
- **Comprehensive Metadata Extraction**: Fetches detailed publication information including:
  - Title, authors, affiliations, countries
  - Publication date, type, language
  - Open access status, citation counts, keywords
  - Grant information
- **Smart DOI Handling**: Automatically cleans and validates DOI inputs
- **Real-time Processing**: Shows loading states and progress
- **Results Preview**: Displays extracted data in a clean, sortable table
- **CSV Download**: Export results as a timestamped CSV file
- **Error Handling**: Gracefully handles missing data and API failures
- **Responsive Design**: Works on desktop and mobile devices

## Installation

### Option 1: Local Python Installation

1. **Clone or download the project files**
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Docker Installation (Recommended for Production)

1. **Ensure Docker and Docker Compose are installed**
2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Or build and run manually**:
   ```bash
   docker build -t ddc-publication-extractor .
   docker run -p 5000:5000 ddc-publication-extractor
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Enter DOIs** in the text area:
   - One DOI per line, or
   - Comma-separated DOIs
   - Supports various DOI formats (with/without prefixes)

4. **Click "Extract Metadata"** to process the DOIs

5. **View results** in the interactive table

6. **Download results** as a CSV file using the download button

## Example DOIs

Try these example DOIs to test the application:

```
10.1038/s41591-019-0726-6
10.1126/science.abc1234
https://doi.org/10.1000/123456
```

## API Endpoints

- `GET /` - Main application page
- `POST /extract` - Extract metadata from DOIs
- `POST /download` - Download results as CSV

## Data Fields Extracted

The application extracts the following metadata fields:

| Field | Description |
|-------|-------------|
| `id` | OpenAlex publication ID |
| `title` | Publication title |
| `display_name` | Display name |
| `all_authors` | All authors (semicolon-separated) |
| `all_affiliations` | All author affiliations |
| `all_countries` | All author countries |
| `doi` | Digital Object Identifier |
| `publication_date` | Publication date |
| `publication_year` | Publication year |
| `type` | Publication type |
| `language` | Publication language |
| `open_access` | Open access status |
| `open_access_status` | Detailed OA status |
| `open_access_url` | Open access URL |
| `cited_by_count` | Citation count |
| `keywords` | Publication keywords |
| `grants` | Grant information |

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5)
- **API**: OpenAlex API for publication metadata
- **Data Processing**: Pandas for data manipulation
- **Error Handling**: Comprehensive error handling with retry mechanisms
- **Rate Limiting**: Built-in delays to respect API limits
- **Containerization**: Docker support for easy deployment

## Docker Benefits

- **Consistent Environment**: Same runtime environment across all deployments
- **Easy Deployment**: Simple commands to deploy anywhere Docker runs
- **Production Ready**: Optimized for production use with health checks
- **Security**: Runs as non-root user with minimal attack surface
- **Scalability**: Easy to scale horizontally with load balancers
- **Portability**: Works identically on any platform that supports Docker

## OpenAlex API

This application uses the [OpenAlex API](https://docs.openalex.org/) to fetch publication metadata. The API is free to use and provides comprehensive academic publication data.

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Common Issues

1. **"No DOIs provided" error**: Make sure you've entered at least one DOI
2. **"No valid DOIs found" error**: Check that your DOIs are in the correct format
3. **Slow loading**: The API may take time to respond for large numbers of DOIs
4. **Download fails**: Ensure you have results before trying to download

### Performance Notes

- Processing time depends on the number of DOIs and API response times
- The application processes DOIs in chunks of 50 for optimal performance
- Failed requests are automatically retried up to 3 times

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## Support

If you encounter any issues or have questions, please check the troubleshooting section above or create an issue in the project repository.
