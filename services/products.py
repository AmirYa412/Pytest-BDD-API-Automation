"""Products endpoints helpers."""

from typing import Dict


class Products:
    """Helper for getting all products with pagination."""

    ENDPOINT = "/products"
    SCHEMA = {
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "price": {"type": "number"},
                        "category": {"type": "string"},
                        "stock": {"type": "integer"},
                        "brand": {"type": "string"},
                        "thumbnail": {"type": "string"}
                    },
                    "required": ["id", "title", "price", "category"]
                }
            },
            "total": {"type": "integer"},
            "skip": {"type": "integer"},
            "limit": {"type": "integer"}
        },
        "required": ["products", "total", "skip", "limit"]
    }

    @staticmethod
    def get_params(limit: int = 30, skip: int = 0, sort_by: str = None, order: str = None) -> Dict:
        """Build query parameters for listing products.

        Args:
            limit: Number of products to return (default: 30)
            skip: Number of products to skip for pagination (default: 0)
            sort_by: Field to sort by (e.g., 'title', 'price')
            order: Sort order ('asc' or 'desc')

        Returns:
            Query parameters dictionary
        """
        return {"limit": limit, "skip": skip, "sortBy": sort_by, "order": order}


class ProductGet:
    """Helper for getting a single product by ID."""

    ENDPOINT = "/products/"  # Use as /products/{id} in steps
    SCHEMA = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "price": {"type": "number"},
            "category": {"type": "string"},
            "stock": {"type": "integer"},
            "brand": {"type": "string"},
            "rating": {"type": "number"},
            "images": {"type": "array"},
            "thumbnail": {"type": "string"}
        },
        "required": ["id", "title", "description", "price", "category", "stock"]
    }

    ERROR_404_SCHEMA = {
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": ["message"]
    }


class ProductsSearch:
    """Helper for searching products by query."""

    ENDPOINT = "/products/search"
    SCHEMA = Products.SCHEMA  # Same structure as list response

    @staticmethod
    def get_params(query: str, limit: int = 30) -> Dict:
        """Build query parameters for searching products.

        Args:
            query: Search query string
            limit: Number of products to return (default: 30)

        Returns:
            Query parameters dictionary
        """
        return {"q": query, "limit": limit}


class ProductsCategory:
    """Helper for getting products by category."""

    ENDPOINT = "/products/category"  # Use as /products/category/{category} in steps
    SCHEMA = Products.SCHEMA  # Same structure as list response