import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import logging
import traceback
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_url_content(url: str) -> requests.Response:
    """Fetch content from URL with proper headers"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    return requests.get(url, headers=headers, timeout=30)


def get_http_info(response: requests.Response) -> Dict[str, Any]:
    """Extract HTTP information from response"""
    return {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "encoding": response.encoding,
        "is_redirect": response.is_redirect,
        "url": response.url,
    }


def full_seo_audit(url: str) -> Dict[str, Any]:
    """Perform a full SEO audit of the given URL"""
    audit_result = {}

    try:
        response = fetch_url_content(url)

        final_url = response.url  # Final URL after all redirects
        using_https = final_url.startswith("https://")

        # Determine input type (Domain or URL with path)
        parsed_url = urlparse(url)
        input_type = "Domain" if parsed_url.path.strip("/") == "" else "URL with path"

        audit_result["Input"] = {
            "URL": url,
            "Input type": input_type,
        }

        # HTTP section
        audit_result["http"] = get_http_info(response)

        soup = BeautifulSoup(response.content, "html.parser")

        # Title analysis
        title_tag = soup.find("title")
        title_data = title_tag.string if title_tag else ""
        title_length = len(title_data)
        title_tag_number = len(soup.find_all("title"))

        audit_result["title"] = {
            "found": "Found" if title_tag else "Not found",
            "data": title_data,
            "length": title_length,
            "characters": len(title_data),
            "words": len(title_data.split()) if title_data else 0,
            "charPerWord": round(len(title_data) / len(title_data.split()), 2)
            if title_data and len(title_data.split()) > 0
            else 0,
            "tag number": title_tag_number,
        }

        # Meta description analysis
        description_tag = soup.find("meta", {"name": "description"})
        description_data = description_tag["content"] if description_tag else ""
        description_length = len(description_data)
        meta_description_number = len(soup.find_all("meta", {"name": "description"}))

        audit_result["meta_description"] = {
            "found": "Found" if description_tag else "Not found",
            "data": description_data,
            "length": description_length,
            "characters": len(description_data),
            "words": len(description_data.split()) if description_data else 0,
            "charPerWord": round(
                len(description_data) / len(description_data.split()), 2
            )
            if description_data and len(description_data.split()) > 0
            else 0,
            "number": meta_description_number,
        }

        # Metadata analysis
        metadata_info = {}
        charset_tag = soup.find("meta", {"charset": True})
        metadata_info["charset"] = charset_tag["charset"] if charset_tag else None

        canonical_tag = soup.find("link", {"rel": "canonical"})
        metadata_info["canonical"] = canonical_tag["href"] if canonical_tag else None

        favicon_tag = soup.find("link", {"rel": "icon"}) or soup.find(
            "link", {"rel": "shortcut icon"}
        )
        metadata_info["favicon"] = favicon_tag["href"] if favicon_tag else None

        viewport_tag = soup.find("meta", {"name": "viewport"})
        metadata_info["viewport"] = viewport_tag["content"] if viewport_tag else None

        keywords_tag = soup.find("meta", {"name": "keywords"})
        metadata_info["keywords"] = keywords_tag["content"] if keywords_tag else None

        audit_result["metadata_info"] = metadata_info

        # Headings analysis
        headings = {"H1": 0, "H2": 0, "H3": 0, "H4": 0, "H5": 0, "H6": 0}
        for key in headings:
            headings[key] = len(soup.find_all(key.lower()))

        h1_content = soup.find("h1").text if soup.find("h1") else ""

        audit_result["Page Headings summary"] = {
            **headings,
            "H1 count": len(soup.find_all("h1")),
            "H1 Content": h1_content,
        }

        # Word count analysis
        text_content = " ".join(list(soup.stripped_strings))
        words = re.findall(r"\b\w+\b", text_content.lower())
        word_count_total = len(words)

        anchor_elements = soup.find_all("a")
        anchor_text = " ".join(a.text for a in anchor_elements if a.text.strip())
        anchor_text_words = len(anchor_text.split())
        anchor_percentage = (
            round((anchor_text_words / word_count_total) * 100, 2)
            if word_count_total > 0
            else 0
        )

        audit_result["word_count"] = {
            "total": word_count_total,
            "Corrected word count": word_count_total,
            "Anchor text words": anchor_text_words,
            "Anchor Percentage": anchor_percentage,
        }

        # Links analysis
        total_links = len(soup.find_all("a"))
        external_links = sum(
            1
            for link in soup.find_all("a")
            if link.get("href", "").startswith(("http", "https"))
        )
        internal_links = total_links - external_links
        nofollow_count = sum(
            1 for link in soup.find_all("a") if "nofollow" in link.get("rel", [])
        )

        links = [
            {"href": link["href"], "text": link.text.strip()}
            for link in soup.find_all("a")
            if link.get("href")
        ]

        audit_result["links_summary"] = {
            "Total links": total_links,
            "External links": external_links,
            "Internal": internal_links,
            "Nofollow count": nofollow_count,
            "links": links,
        }

        # Image analysis
        images = soup.find_all("img")
        image_data = [
            {"src": img.get("src", ""), "alt": img.get("alt", "")} for img in images
        ]

        audit_result["images_analysis"] = {
            "summary": {
                "total": len(images),
                "No src tag": sum(1 for img in images if not img.get("src")),
                "No alt tag": sum(1 for img in images if not img.get("alt")),
            },
            "data": image_data,
        }

    except Exception as ex:
        logger.error(
            f"Error in full_seo_audit: {str(ex)}\nStack trace: {traceback.format_exc()}"
        )
        return {}

    return audit_result


# Example usage
if __name__ == "__main__":
    url = "https://www.americorpint.com"  # Replace with your target URL
    results = full_seo_audit(url)
    print(results)
