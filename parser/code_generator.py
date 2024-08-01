
import re
import logging
from typing import Dict, Any, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self, model: str = "claude-3-5-sonnet-20240620"):
        self.chat = ChatAnthropic(model=model, api_key=settings.ANTHROPIC_API_KEY)

    def generate_code(self, api_info: Dict[str, Any]) -> Response:
        system_message = f"""
        You are a code generator. Your task is to generate Python code based on the given API documentation. Follow these strict rules:

        1. Read and analyze the provided API documentation carefully.
        2. Identify all API endpoints, required parameters, authentication methods, and response formats.
        3. Generate complete, executable Python code that does the following:
           a. Imports all necessary libraries (including csv, requests, and any others needed).
           b. Implements proper API authentication and headers as specified in the documentation.
           c. Makes API calls to all identified endpoints.
           d. Handles API responses, including both success and error scenarios.
           e. Includes clear, descriptive comments throughout the code.

        4. Ensure the generated code follows these guidelines:
           a. Adheres to PEP 8 style guidelines.
           b. Includes comprehensive error handling and logging.
           c. Is well-organized and modular.
           d. Uses appropriate variable names and follows Python best practices.

        5. Your response must contain only the complete Python code, enclosed in triple backticks and tagged as Python:
           ```python
           [Your generated Python code here]
           ```
        6. Do not include any explanations, discussions, or text outside of the code block.
        7. The code must be fully functional and ready to execute without any modifications.

        Remember, your entire response should be valid, executable Python code that fulfills all the above requirements based on the given API documentation. Any deviation from these instructions will be considered a failure.
        API documentation to parse: {{api_info}}
        """

        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=f"Generate Python code for the following API information:\n\n{api_info}")
        ]

        try:
            response = self.chat.invoke(messages)
            result = response.content
            logger.info("Generated code:\n%s", result)

            python_code = self._extract_python_code(result)
            if python_code:
                return Response({"generated_code": python_code}, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Failed to extract Python code block from the response.",
                    "raw_response": result
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.exception("An error occurred during code generation")
            return Response({
                "error": f"An error occurred during code generation: {str(e)}",
                "raw_response": result if 'result' in locals() else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _extract_python_code(self, response: str) -> Optional[str]:
        code_match = re.search(r'```python\n(.*?)```', response, re.DOTALL)
        return code_match.group(1) if code_match else None
