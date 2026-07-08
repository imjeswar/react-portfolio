import os
import sys

# Add backend directory to Python system path to resolve imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.services.index_service import IndexService

def main():
    print("Initializing RAG Indexing for Portfolio...")
    try:
        res = IndexService.index_portfolio_data()
        if res["status"] == "success":
            print("Portfolio indexing completed successfully!")
            print(f"Indexed Chunks: {res['chunks_indexed']}")
            print(f"Collection Name: {res['collection_name']}")
            print(f"Embedding Dimension: {res['embedding_dimension']}")
        else:
            print(f"Error during indexing: {res['message']}")
    except Exception as e:
        print(f"Exception raised during indexing: {e}")

if __name__ == "__main__":
    main()
