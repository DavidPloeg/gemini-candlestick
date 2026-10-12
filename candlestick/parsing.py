"""Helpers for cleaning and parsing text returned by Gemini."""
import json
import re

# Headings that mark where generated meeting minutes begin
MINUTES_START_MARKERS = ["**Gemini", "# Gemini", "## Gemini", "### Gemini"]


def clean_minutes_text(text):
    # Check for the first occurrence of either substring
    start_index_list = [text.find(each) for each in MINUTES_START_MARKERS]

    # Find the first valid index
    start_index = -1
    for index in start_index_list:
        if index != -1 and (start_index == -1 or index < start_index):
            start_index = index

    # Extract the substring if one of the patterns is found
    if start_index != -1:
        updated_text = text[start_index:]
    else:
        updated_text = text  # Keep original if neither is found
    text = updated_text

    # Find the position of the substring "Munehisa Homma, Chairman"
    marker = ", Chairman"
    index = text.find(marker)
    if index != -1:
        # Get all text up to and including "Munehisa Homma, Chairman"
        text_with_marker = text[:index + len(marker)]
    else:
        # Handle case where marker is not found
        text_with_marker = text
    text = text_with_marker
    return text


def extract_json(text_response):
    """
    Extracts and returns a list of valid JSON objects found in the input string.

    Args:
        text_response (str): The input string from which to extract JSON objects.

    Returns:
        list: A list of extracted JSON objects, or None if no valid JSON objects are found.
    """

    # Find all potential JSON objects within the text
    json_objects = find_potential_json(text_response)

    # Return the list of JSON objects if any are found, otherwise return None
    return json_objects if json_objects else None


def find_potential_json(text_response):
    """
    Finds and returns a list of potential JSON objects within the input string.

    This method searches for strings that start with '{' and end with '}',
    and then attempts to parse them as JSON. If a JSONDecodeError occurs,
    it attempts to extend the search to include nested structures.

    Args:
        text_response (str): The input string from which to extract potential JSON objects.

    Returns:
        list: A list of extracted potential JSON objects. 
    """

    # This pattern matches a string that starts with '{' and ends with '}'
    pattern = r'\{[^{}]*\}'
    matches = re.finditer(pattern, text_response)
    json_objects = []
    for match in matches:
        json_str = match.group(0)
        try:
            # Validate if the extracted string is valid JSON
            json_obj = json.loads(json_str)
            json_objects.append(json_obj)
        except json.JSONDecodeError:
            # Extend the search for nested structures
            extended_json_str = extend_search(text_response, match.span())
            try:
                json_obj = json.loads(extended_json_str)
                json_objects.append(json_obj)
            except json.JSONDecodeError:
                # Handle cases where the extraction is not valid JSON
                continue
    return json_objects


def extend_search(text, span):
    """
    Extends the search range to capture potential nested JSON structures.

    This method starts from the given span and expands the search range
    until the correct nesting balance of '{' and '}' characters is found,
    indicating a complete JSON structure.

    Args:
        text (str): The input string being searched.
        span (tuple): A tuple containing the start and end indices of the initial match.

    Returns:
        str: The extended string that potentially contains a complete JSON structure.
    """

    start, end = span
    nest_count = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            nest_count += 1
        elif text[i] == '}':
            nest_count -= 1
            if nest_count == 0:
                return text[start:i+1]
    return text[start:end]
