# Galileo Asset Tokeniser API

A mini API for tokenizing physical assets into pNFTs (physical NFTs) following the Galileo Protocol approach. This API allows users to create physical assets, tokenize them into pNFTs, and manage ownership transfers.

## Features

- ✅ Create physical assets with metadata
- ✅ Tokenize assets into pNFTs
- ✅ List all pNFTs with optional owner filtering
- ✅ Retrieve specific pNFT details
- ✅ Transfer pNFT ownership
- ✅ Automatic OpenAPI/Swagger documentation
- ✅ Input validation and error handling

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/JulienPul/galileo_tokeniser.git
cd galileo_tokeniser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the API:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/assets` | Create a physical asset |
| `POST` | `/pnfts` | Tokenize an existing asset |
| `GET` | `/pnfts` | List all pNFTs (with optional owner filter) |
| `GET` | `/pnfts/{id}` | Get pNFT details by ID |
| `POST` | `/pnfts/{id}/transfer` | Transfer pNFT ownership |

### Additional Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and available endpoints |
| `GET` | `/assets` | List all physical assets |
| `GET` | `/assets/{id}` | Get asset details by ID |

## Usage Examples

### 1. Create a Physical Asset

```bash
curl -X POST "http://localhost:8000/assets" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Montre Rolex Submariner",
    "serial_number": "RS12345678",
    "description": "Montre acier 40mm – édition 2020",
    "owner": "Alice Dupont"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Montre Rolex Submariner",
  "serial_number": "RS12345678",
  "description": "Montre acier 40mm – édition 2020",
  "owner": "Alice Dupont"
}
```

### 2. Tokenize an Asset

```bash
curl -X POST "http://localhost:8000/pnfts" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 1,
    "token_uri": "ipfs://QmYourTokenURIHere",
    "current_owner": "Alice Dupont"
  }'
```

**Response:**
```json
{
  "id": 1,
  "asset_id": 1,
  "token_uri": "ipfs://QmYourTokenURIHere",
  "issued_date": "2025-01-27T10:30:00.000000",
  "current_owner": "Alice Dupont"
}
```

### 3. List All pNFTs

```bash
curl -X GET "http://localhost:8000/pnfts"
```

### 4. Filter pNFTs by Owner

```bash
curl -X GET "http://localhost:8000/pnfts?owner=Alice%20Dupont"
```

### 5. Get Specific pNFT

```bash
curl -X GET "http://localhost:8000/pnfts/1"
```

### 6. Transfer pNFT Ownership

```bash
curl -X POST "http://localhost:8000/pnfts/1/transfer" \
  -H "Content-Type: application/json" \
  -d '{
    "new_owner": "Bob Martin"
  }'
```

## Data Models

### Asset
```json
{
  "id": 1,
  "name": "Montre Rolex Submariner",
  "serial_number": "RS12345678",
  "description": "Montre acier 40mm – édition 2020",
  "owner": "Alice Dupont"
}
```

### pNFT
```json
{
  "id": 1,
  "asset_id": 1,
  "token_uri": "ipfs://QmYourTokenURIHere",
  "issued_date": "2025-01-27T10:30:00.000000",
  "current_owner": "Alice Dupont"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `200 OK`: Successful request
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

Example error response:
```json
{
  "detail": "Asset with ID 999 not found"
}
```

## Technical Details

- **Framework**: FastAPI
- **Data Storage**: In-memory Python lists (no database required)
- **ID Generation**: Auto-incrementing counters for assets and pNFTs
- **Date Format**: ISO 8601 format for timestamps
- **Validation**: Pydantic models with automatic validation
- **Documentation**: Automatic OpenAPI/Swagger generation

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API

You can test the API using:
- The interactive docs at `/docs`
- cURL commands (examples above)
- Postman or any HTTP client
- Python requests library

## Project Structure

```
galileo_tokeniser/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

## License

This project is created for educational purposes as part of a mini-project assignment.
