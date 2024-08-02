import re
import logging
from typing import Dict, Any, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

# Set up logging
logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self, model: str = "claude-3-5-sonnet-20240620"):
        # Initialize the ChatAnthropic client with the specified model and API key
        self.chat = ChatAnthropic(model=model, api_key=settings.ANTHROPIC_API_KEY)

    def generate_code(self, api_info: Dict[str, Any]) -> Response:
        # Define the system message for the AI to act as a code generator
        system_message = f"""
        [System message content defining the code generation task and rules]
        """

        # Prepare the messages for the AI, including the system message and the API information
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=f"Generate Python code for the following API information:\n\n{api_info}")
        ]

        try:
            # Invoke the AI to generate the code
            response = self.chat.invoke(messages)
            result = response.content
            logger.info("Generated code:\n%s", result)

            # Extract the Python code from the AI's response
            python_code = self._extract_python_code(result)
            if python_code:
                return Response({"generated_code": python_code}, status=status.HTTP_200_OK)
            else:
                # Handle case where Python code couldn't be extracted
                return Response({
                    "error": "Failed to extract Python code block from the response.",
                    "raw_response": result
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Log and handle any exceptions that occur during code generation
            logger.exception("An error occurred during code generation")
            return Response({
                "error": f"An error occurred during code generation: {str(e)}",
                "raw_response": result if 'result' in locals() else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _extract_python_code(self, response: str) -> Optional[str]:
        # Use regex to extract the Python code block from the AI's response
        code_match = re.search(r'```python\n(.*?)```', response, re.DOTALL)
        return code_match.group(1) if code_match else None