# SEO Audit Tool

A comprehensive Python-based SEO analysis tool that performs detailed audits of web pages. This tool analyzes various SEO elements including meta tags, headings, content structure, links, and images to provide actionable insights for SEO optimization.

## Features

- Title tag and meta description analysis
- Metadata validation (charset, canonical URL, favicon)
- Heading structure analysis (H1-H6)
- Word count and content analysis
- Internal and external link analysis
- Image optimization check (alt tags)
- HTTP response analysis
- Mobile viewport validation

## Requirements

```
beautifulsoup4>=4.9.3
requests>=2.25.1
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Daniel-Osman/python-seo-analyzer.git
cd seo-audit-tool
```

2. Create and activate a virtual environment (optional but recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

```python
from seo_audit import full_seo_audit

# Replace with your target URL
url = "https://www.example.com"
results = full_seo_audit(url)
print(results)
```

Example output:

```python
{
    "Input": {
        "URL": "https://www.example.com",
        "Input type": "Domain"
    },
    "title": {
        "found": "Found",
        "data": "Example Domain",
        "length": 13,
        # ... more details
    },
    # ... additional analysis results
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` file for more information.

## Contact

Daniel Osman 
X - https://x.com/_Daniel_Osman
linkedin - https://www.linkedin.com/in/danielosmancom/

Project Link: [https://github.com/Daniel-Osman/python-seo-analyzer.](https://github.com/Daniel-Osman/python-seo-analyzer.)
