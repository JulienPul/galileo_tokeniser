from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="Galileo Asset Tokeniser API",
    description="A mini API for tokenizing physical assets into pNFTs (physical NFTs)",
    version="1.0.0"
)

# In-memory storage
assets_db = []
pnfts_db = []

# Auto-incrementing counters
asset_counter = 0
pnft_counter = 0

# Data Models
class Asset(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., description="Name of the physical asset")
    serial_number: str = Field(..., description="Unique serial number of the asset")
    description: str = Field(..., description="Detailed description of the asset")
    owner: str = Field(..., description="Current owner of the asset")

class AssetCreate(BaseModel):
    name: str = Field(..., description="Name of the physical asset")
    serial_number: str = Field(..., description="Unique serial number of the asset")
    description: str = Field(..., description="Detailed description of the asset")
    owner: str = Field(..., description="Current owner of the asset")

class pNFT(BaseModel):
    id: Optional[int] = None
    asset_id: int = Field(..., description="ID of the associated physical asset")
    token_uri: str = Field(..., description="IPFS URI for the pNFT metadata")
    issued_date: str = Field(..., description="Date when the pNFT was issued (ISO 8601 format)")
    current_owner: str = Field(..., description="Current owner of the pNFT")

class pNFTCreate(BaseModel):
    asset_id: int = Field(..., description="ID of the physical asset to tokenize")
    token_uri: str = Field(..., description="IPFS URI for the pNFT metadata")
    current_owner: str = Field(..., description="Current owner of the pNFT")

class pNFTTransfer(BaseModel):
    new_owner: str = Field(..., description="New owner of the pNFT")

# Helper functions
def get_asset_by_id(asset_id: int) -> Optional[Asset]:
    """Find an asset by its ID"""
    for asset in assets_db:
        if asset.id == asset_id:
            return asset
    return None

def get_pnft_by_id(pnft_id: int) -> Optional[pNFT]:
    """Find a pNFT by its ID"""
    for pnft in pnfts_db:
        if pnft.id == pnft_id:
            return pnft
    return None

def generate_token_uri() -> str:
    """Generate a mock IPFS URI"""
    return f"ipfs://Qm{str(uuid.uuid4()).replace('-', '')[:44]}"

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Galileo Asset Tokeniser API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "POST /assets": "Create a physical asset",
            "POST /pnfts": "Tokenize an existing asset",
            "GET /pnfts": "List all pNFTs (with optional owner filter)",
            "GET /pnfts/{id}": "Get pNFT details by ID",
            "POST /pnfts/{id}/transfer": "Transfer pNFT ownership"
        }
    }

@app.post("/assets", response_model=Asset)
async def create_asset(asset: AssetCreate):
    """Create a new physical asset"""
    global asset_counter
    asset_counter += 1
    
    new_asset = Asset(
        id=asset_counter,
        name=asset.name,
        serial_number=asset.serial_number,
        description=asset.description,
        owner=asset.owner
    )
    
    assets_db.append(new_asset)
    return new_asset

@app.post("/pnfts", response_model=pNFT)
async def create_pnft(pnft: pNFTCreate):
    """Tokenize an existing asset into a pNFT"""
    global pnft_counter
    
    # Validate that the asset exists
    asset = get_asset_by_id(pnft.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail=f"Asset with ID {pnft.asset_id} not found")
    
    pnft_counter += 1
    
    new_pnft = pNFT(
        id=pnft_counter,
        asset_id=pnft.asset_id,
        token_uri=pnft.token_uri,
        issued_date=datetime.now().isoformat(),
        current_owner=pnft.current_owner
    )
    
    pnfts_db.append(new_pnft)
    return new_pnft

@app.get("/pnfts", response_model=List[pNFT])
async def list_pnfts(owner: Optional[str] = Query(None, description="Filter pNFTs by owner")):
    """List all pNFTs, optionally filtered by owner"""
    if owner:
        filtered_pnfts = [pnft for pnft in pnfts_db if pnft.current_owner == owner]
        return filtered_pnfts
    return pnfts_db

@app.get("/pnfts/{pnft_id}", response_model=pNFT)
async def get_pnft(pnft_id: int):
    """Get pNFT details by ID"""
    pnft = get_pnft_by_id(pnft_id)
    if not pnft:
        raise HTTPException(status_code=404, detail=f"pNFT with ID {pnft_id} not found")
    return pnft

@app.post("/pnfts/{pnft_id}/transfer", response_model=pNFT)
async def transfer_pnft(pnft_id: int, transfer: pNFTTransfer):
    """Transfer ownership of a pNFT"""
    pnft = get_pnft_by_id(pnft_id)
    if not pnft:
        raise HTTPException(status_code=404, detail=f"pNFT with ID {pnft_id} not found")
    
    # Update the pNFT's current owner
    pnft.current_owner = transfer.new_owner
    
    # Update in the database
    for i, stored_pnft in enumerate(pnfts_db):
        if stored_pnft.id == pnft_id:
            pnfts_db[i] = pnft
            break
    
    return pnft

# Additional utility endpoints
@app.get("/assets", response_model=List[Asset])
async def list_assets():
    """List all physical assets"""
    return assets_db

@app.get("/assets/{asset_id}", response_model=Asset)
async def get_asset(asset_id: int):
    """Get asset details by ID"""
    asset = get_asset_by_id(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail=f"Asset with ID {asset_id} not found")
    return asset

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
