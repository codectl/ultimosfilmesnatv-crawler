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
    matches = []
    # Looking for IMDb links
    if annotations.pages_with_matching_images:
        for page in annotations.pages_with_matching_images:
            if 'https://www.imdb.com' in page.url and candidate.imdb_id in page.url:
                matches.append(('imdb link', candidate.imdb_id))
                break

    # Looking for web entities
    if annotations.web_entities:
        for entity in annotations.web_entities:
            if entity.description and not any(entity.description in match[1] for match in matches) and \
                    len(entity.description) > 2:
                if entity.description.lower() in candidate.imdb_title.lower():
                    matches.append(('imdb title', entity.description))
                if any(entity.description.lower() == actor.lower() for actor in candidate.combine_all_actors()):
                    matches.append(('actors', entity.description))
                elif entity.description.lower() in candidate.plot.lower():
                    matches.append(('description', entity.description))
                if entity.description == candidate.year:
                    matches.append(('year', entity.description))
                if entity.description.lower() == candidate.director.lower():
                    matches.append(('director', entity.description))

    # Looking for best guesses
    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            if label.label.strip().lower().replace('-', ' ') in candidate.imdb_title.lower().replace('-', ' '):
                matches.append(('best guess', label.label))

    return matches


def google_vision_candidates(annotations, candidates):
    """Additional candidates returned by Google Vision API"""
    other_candidates = []
    if annotations.pages_with_matching_images:
        for page in annotations.pages_with_matching_images:
            if 'https://www.imdb.com' in page.url:
                imdb_id = _extract_imdb_id(page.url)
                # Checking if candidate is in list of results
                if not any(
                        candidate.imdb_id == imdb_id for candidate in candidates) and imdb_id not in other_candidates:
                    imdb_id = _extract_imdb_id(page.url)
                    other_candidates.append(imdb_id)
    return other_candidates


def _extract_imdb_id(link):
    """Extracting IMDB title ID"""
    return link.replace('https://www.imdb.com/title/', '').split('/')[0]
