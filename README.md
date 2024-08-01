# API Parser backend

## Overview

API Parser is an advanced Django-based backend solution designed to streamline the process of interpreting API documentation, generating code, and processing API data. Leveraging the power of Django Rest Framework, integrating with the Anthropic API, and utilizing LangChain for enhanced language model capabilities, this project offers a robust set of features for developers and API enthusiasts.

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Key Components](#key-components)
4. [Technical Stack](#technical-stack)
5. [Installation and Setup](#installation-and-setup)
6. [Usage](#usage)
7. [API Endpoints](#api-endpoints)
8. [Data Models](#data-models)
9. [Error Handling](#error-handling)
10. [Security Considerations](#security-considerations)
11. [Contributing](#contributing)
12. [License](#license)

## Features

- **API Documentation Parsing**: Efficiently interpret and structure API documentation using advanced NLP techniques.
- **Automated Code Generation**: Generate code snippets based on parsed API information, leveraging LangChain's capabilities.
- **Data Processing and Storage**: Process API data and store it in structured formats for easy retrieval and analysis.
- **CSV Generation**: Automatically create CSV files from processed API data for easy export and sharing.
- **File Management**: Download generated code and CSV files with ease.
- **Comprehensive API**: RESTful endpoints for managing documents, code, and data throughout the parsing and generation process.
- **Integration with Anthropic API**: Utilize advanced AI capabilities for enhanced parsing and code generation.

## Architecture

The API Parser is built on a modular architecture, emphasizing separation of concerns:

- **Views**: Handle HTTP requests and responses, implementing the RESTful API.
- **Models**: Define data structures for API documents, generated code, and processed data.
- **Serializers**: Manage data serialization and deserialization for API interactions.
- **Parsers**: Interpret API documentation using advanced NLP techniques.
- **Generators**: Produce code based on parsed information, utilizing LangChain for enhanced generation capabilities.
- **Processors**: Handle data transformation and CSV generation.
- **Storage**: Manage file operations and storage of generated artifacts.

## Key Components

### Document Management
- `APIDocumentList` and `APIDocumentDetail`: CRUD operations for API documents.

### Code Generation
- `GeneratedCodeList` and `GeneratedCodeDetail`: Retrieve and list generated code.
- `LatestGeneratedCodeView`: Fetch the most recent generated code.

### Data Processing
- `APIDataList` and `APIDataDetail`: Manage processed API data.
- `LatestAPIDataView`: Access the latest processed data.

### Core Functionality
- `InterpretAPIDocumentation`: Orchestrates the document parsing, code generation, and data processing workflow.

### File Operations
- `DownloadGeneratedCode`: Retrieve generated code as a Python file.
- `DownloadCSVFile`: Download processed data in CSV format.
- `ListCSVFiles`: Enumerate available CSV files.

## Technical Stack

- **Framework**: Django , LangChain
- **API Framework**: Django Rest Framework 
- **Database**: SQLite
- **External APIs**: Anthropic API LLM
- **Language Model Integration**: LangChain
- **Language**: Python 3.11.5

## Installation and Setup

1. Clone the repository:

- git clone https://github.com/Shivkumar-Raghuwanshi/api_parser_backend.git
- cd api_parser_backend

2. Set up a virtual environment:
- python -m venv venv
- source venv/bin/activate  # On Windows use venv\Scripts\activate

3. Install dependencies:
- pip install -r requirements.txt

4. Configure environment variables:
ANTHROPIC_API_KEY=Your API Key

5. Run migrations:
- python manage.py migrate

6. Start the development server:
- python manage.py runserver

## Usage

Interact with the API Parser through its RESTful API endpoints. Here's a basic workflow:

1. Upload API documentation using the `/api/documents/` endpoint.
2. Trigger interpretation and code generation with `/api/interpret/`.
3. Retrieve generated code and processed data from respective endpoints.
4. Download CSV files or generated code as needed.

For detailed API usage, refer to the [API Endpoints](#api-endpoints) section.

## API Endpoints

- `POST /api-documents/`: Create a new API document
- `GET /api-documents/`: List all API documents
- `GET /api-documents/<int:pk>/`: Retrieve a specific API document
- `PUT /api-documents/<int:pk>/`: Update a specific API document
- `DELETE /api-documents/<int:pk>/`: Delete a specific API document

- `GET /generated-code/`: List all generated code
- `GET /generated-code/<int:pk>/`: Retrieve specific generated code
- `GET /generated-code/latest/`: Get the latest generated code

- `GET /api-data/`: List all processed API data
- `GET /api-data/<int:pk>/`: Retrieve specific API data
- `GET /api-data/latest/`: Get the latest processed API data

- `POST /interpret/`: Interpret API documentation and generate code
- `POST /execute/`: Execute generated code (Note: this endpoint may be disabled for security reasons)

- `GET /download-generated-code/<int:pk>/`: Download specific generated code
- `GET /download-latest-generated-code/`: Download the latest generated code

- `GET /download-csv/<int:pk>/`: Download specific CSV file
- `GET /download-latest-csv/`: Download the latest CSV file

- `GET /list-csv-files/`: List all available CSV files

- `GET /admin/`: Django admin interface (requires admin credentials)

## Data Models

- `APIDocument`: Stores API documentation content
- `GeneratedCode`: Contains generated code linked to API documents
- `APIData`: Holds processed API data and file paths

## Error Handling

The application implements comprehensive error handling:
- Validation errors return 400 Bad Request
- Not found errors return 404 Not Found
- Server errors return 500 Internal Server Error

All errors are logged for monitoring and debugging purposes.

## Security Considerations

- Code execution is disabled by default for security reasons
- Implement proper authentication and authorization before deployment
- Regularly update dependencies to patch security vulnerabilities
- Sanitize all input data to prevent injection attacks

## Contributing

We welcome contributions to the API Parser project. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code adheres to our coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.