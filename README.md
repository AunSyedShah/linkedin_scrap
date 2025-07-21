# LinkedIn Profile Scraper

A Python-based web scraper that automatically extracts profile information from LinkedIn based on search phrases. The scraper uses Selenium WebDriver to automate Chrome browser interactions and exports the collected data to Excel files.

## Features

- **Automated LinkedIn Login**: Uses stored credentials to log in automatically
- **Configurable Search Terms**: Reads search phrases from a text file
- **Profile Data Extraction**: Collects name, designation, company, and email (when available)
- **Excel Export**: Saves all scraped data to timestamped Excel files
- **Logging**: Comprehensive logging for debugging and monitoring
- **Rate Limiting**: Built-in delays to avoid detection and respect LinkedIn's servers

## Extracted Information

For each profile found, the scraper extracts:
- Full Name
- Job Title/Designation
- Company Name
- Email Address (when publicly available)
- Profile URL
- Search phrase used to find the profile

## Requirements

- Python 3.7+
- Chrome browser installed
- Valid LinkedIn account
- Internet connection

## Installation

1. **Clone the repository or download the files**
2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```
   Or manually:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Configuration

### 1. LinkedIn Credentials
Edit `credentials.txt` and add your LinkedIn login information:
```
username=your_linkedin_email@example.com
password=your_linkedin_password
```

### 2. Search Phrases
Edit `search_phrases.txt` and add your search terms (one per line):
```
software engineer
data scientist
product manager
python developer
```

## Usage

1. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Run the scraper:**
   ```bash
   python app.py
   ```

3. **Monitor progress:**
   - Watch the console output for real-time updates
   - Check `linkedin_scraper.log` for detailed logs

4. **Results:**
   - Excel file will be created: `linkedin_scraped_data_YYYYMMDD_HHMMSS.xlsx`

## Project Structure

```
linkedin_scrap/
├── app.py                  # Main scraper application
├── credentials.txt         # LinkedIn login credentials
├── search_phrases.txt      # Search terms (one per line)
├── requirements.txt        # Python dependencies
├── setup.sh               # Setup script
├── README.md              # This file
├── linkedin_scraper.log   # Log file (created when run)
└── .venv/                 # Virtual environment
```

## Important Notes

### Legal and Ethical Considerations
- **Respect LinkedIn's Terms of Service**: This tool is for educational purposes
- **Rate Limiting**: The scraper includes delays to be respectful of LinkedIn's servers
- **Data Privacy**: Only scrape publicly available information
- **Use Responsibly**: Don't overload LinkedIn's servers

### Security
- Never commit `credentials.txt` to version control
- Use a dedicated LinkedIn account for scraping if possible
- Consider using environment variables for sensitive data

### Limitations
- Email addresses are only available if publicly displayed
- LinkedIn frequently updates their structure, which may require code updates
- Some profiles may be private or have restricted access
- Rate limiting may slow down the scraping process

## Error Handling

The scraper includes comprehensive error handling:
- **Login failures**: Checks credentials and connection
- **Network issues**: Retries and continues where possible
- **Element not found**: Uses multiple selectors as fallbacks
- **Rate limiting**: Implements random delays

## Troubleshooting

### Common Issues

1. **Login Failed**
   - Verify credentials in `credentials.txt`
   - Check if LinkedIn requires additional verification
   - Ensure stable internet connection

2. **Chrome Driver Issues**
   - The script automatically downloads the correct ChromeDriver
   - Ensure Chrome browser is installed and updated

3. **No Data Extracted**
   - LinkedIn may have changed their page structure
   - Check the log file for specific errors
   - Verify the profile URLs are accessible

4. **Rate Limiting**
   - LinkedIn may temporarily block requests
   - Increase delays in the code
   - Try again after some time

### Debug Mode
To enable more detailed logging, modify the logging level in `app.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Creating an Executable (EXE)

To create a standalone executable:

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Create the executable:**
   ```bash
   pyinstaller --onefile --windowed app.py
   ```

3. **The executable will be in the `dist/` folder**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes only. Please respect LinkedIn's Terms of Service and use responsibly.

## Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for ensuring compliance with LinkedIn's Terms of Service and applicable laws. The authors are not responsible for any misuse of this tool.