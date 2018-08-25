# Imports the Google Cloud client library
from google.cloud import vision


def detect_web_uri(uri):
    """Detects web annotations in the file located in Google Cloud Storage."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.web_detection(image=image)
    annotations = response.web_detection

    return annotations


def evaluate_candidate(annotations, candidate):
    """Matching candidates with Google Vision API"""
    for page in annotations.pages_with_matching_images:
        if 'https://www.imdb.com' in page.url:
            if candidate.imdb_id in page.url:
                return True
    return False


def google_vision_candidates(annotations, candidates):
    """Additional candidates returned by Google Vision API"""
    other_candidates = []
    for page in annotations.pages_with_matching_images:
        if 'https://www.imdb.com' in page.url:
            imdb_id = _extract_imdb_id(page.url)
            # Checking if candidate is in list of results
            if not any(candidate.imdb_id == imdb_id for candidate in candidates) and imdb_id not in other_candidates:
                imdb_id = _extract_imdb_id(page.url)
                other_candidates.append(imdb_id)
    return other_candidates


def _extract_imdb_id(link):
    """Extracting IMDB title ID"""
    return link.replace('https://www.imdb.com/title/', '').split('/')[0]
