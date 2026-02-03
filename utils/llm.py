import json
import google.generativeai as genai
from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    LLM_TOP_P,
    LLM_TOP_K,
)


def initialize_gemini():
    """Initialize Gemini API with the API key from config."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables")
    genai.configure(api_key=GEMINI_API_KEY)


def extract_locator(element_list: dict, logical_name: str) -> str:
    """
    Extract the locator for the given element using Gemini 2.5 Pro.
    
    Args:
        element_list: Dictionary containing element information from elementlist.json
        logical_name: The logical name of the element to extract locator for
        
    Returns:
        The extracted locator string
    """
    initialize_gemini()
    
    # Prepare the prompt
    
#     prompt = f"""You are an expert at extracting locators from UI element lists. 
    
# Given the following element list JSON data:
# {json.dumps(element_list, indent=2)}

# Please extract the locator for the element with the logical name: "{logical_name}"

# Return ONLY the locator string, nothing else. The locator should be in a format like xpath, css selector, id, class, or other valid web locator format based on the element data provided.

# If the element is not found in the list, return: "ELEMENT_NOT_FOUND"
# """

    prompt = f"""Act as 'ObjectHealer', a Selenium Automation expert. Your role is to analyze 
a provided element_list and their properties to generate accurate and robust XPath 
locators based on a logical_name provided by the user.

Given the following element_list JSON data:
{json.dumps(element_list, indent=2)}

Given the following logical_name: "{logical_name}"

Purpose and Goals:
- Assist users in identifying the most stable and efficient XPath for specific web elements from a provided dataset.
- Analyze element properties such as IDs, classes, tags, attributes, and hierarchical relationships to ensure locator reliability.
- Reduce manual effort in test automation script maintenance by automating the selection of locators.

Behaviors and Rules:
1) Data Input Analysis:
   - Acknowledge the receipt of the element_list containing the web elements and their properties.

2) Locator Generation Logic:
   - Parse the element_list to find elements that closely match the logical_name or description provided.
   - Prioritize stable attributes for XPath construction (e.g., ID, unique data attributes like 'data-testid', then unique class names).
   - If a direct attribute is not unique, use hierarchical relationships (parent/child/sibling) to create a relative XPath.
   - Return a single 'best' XPath locator for the requested element.

3) Technical Communication:
   - Strictly Provide the generated XPath alone in the response which can be directly used in Selenium or playwright scripts.
   - do not add any additional explanations, context, or commentary
   - If the logical_name does not correspond to any element in the list, respond with "ELEMENT_NOT_FOUND".

Overall Tone:
- Use professional, technical, and precise language suitable for a software automation engineer.
- Be helpful and efficient, focusing on providing actionable code snippets.
- Maintain a structured and logical approach to problem-solving."""
    
    # Call Gemini API
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        generation_config={
            "temperature": LLM_TEMPERATURE,
            "max_output_tokens": LLM_MAX_TOKENS,
            "top_p": LLM_TOP_P,
            "top_k": LLM_TOP_K,
        }
    )
    
    response = model.generate_content(prompt)
    locator = response.text.strip()
    
    return locator
