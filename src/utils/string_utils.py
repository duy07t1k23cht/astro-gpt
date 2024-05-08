def extract_substring_between_braces(text: str) -> str:
    # Find the index of the first occurrence of '{'
    first_brace_index = text.find("{")

    # Find the index of the last occurrence of '}'
    last_brace_index = text.rfind("}")

    # Check if both indices are valid and the first index is before the last index
    if first_brace_index != -1 and last_brace_index != -1 and first_brace_index < last_brace_index:
        # Extract the substring between the indices
        return text[first_brace_index + 1 : last_brace_index]

    # Return an empty string if the conditions are not met
    return ""
