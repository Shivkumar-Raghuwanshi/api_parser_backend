from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from django.conf import settings
import json
import logging
from typing import Dict, Any

# Set up logging
logger = logging.getLogger(__name__)

class APIDocParser:
    def __init__(self, model: str = "claude-3-5-sonnet-20240620"):
        # Initialize the ChatAnthropic client with the specified model and API key
        self.chat = ChatAnthropic(
            model=model, api_key=settings.ANTHROPIC_API_KEY)

    def parse_documentation(self, documentation: str) -> Dict[str, Any]:
        # Define the system message for the AI to act as an API documentation parser
        system_message = """ You are an expert in API documentation parsing. Extract the endpoints, required parameters, authentication methods, and return data formats from the given API documentation. Your response should be a JSON object that is easily decodable"""

        # Prepare the messages for the AI, including the system message and the documentation to parse
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(
                content=f"Parse the following API documentation:\n\n{documentation}")
        ]

        try:
            # Invoke the AI to parse the documentation
            response = self.chat.invoke(messages)
            result = response.content
            logger.info("Raw parsed API documentation response: %s", result)

            # Attempt to parse the AI's response as JSON
            parsed_info = json.loads(result)
            return parsed_info
        except json.JSONDecodeError as e:
            # Log and handle JSON decoding errors
            logger.error("Failed to decode JSON: %s", e)
            return {
                "error": "Failed to decode JSON from the response.",
                "raw_response": result
            }
        except Exception as e:
            # Log and handle any other exceptions that may occur
            logger.error("An error occurred during parsing: %s", e)
            return {
                "error": f"An error occurred: {str(e)}",
                "raw_response": result if 'result' in locals() else None
            }