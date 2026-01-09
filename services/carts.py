"""Carts endpoints helpers."""

from typing import Dict, List


class Carts:
    """Helper for getting all carts."""

    ENDPOINT = "/carts"
    SCHEMA = {
        "type": "object",
        "properties": {
            "carts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "products": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "title": {"type": "string"},
                                    "price": {"type": "number"},
                                    "quantity": {"type": "integer"},
                                    "total": {"type": "number"}
                                },
                                "required": ["id", "title", "price", "quantity", "total"]
                            }
                        },
                        "total": {"type": "number"},
                        "discountedTotal": {"type": "number"},
                        "userId": {"type": "integer"},
                        "totalProducts": {"type": "integer"},
                        "totalQuantity": {"type": "integer"}
                    },
                    "required": ["id", "products", "total", "userId"]
                }
            },
            "total": {"type": "integer"},
            "skip": {"type": "integer"},
            "limit": {"type": "integer"}
        },
        "required": ["carts", "total", "skip", "limit"]
    }

    @staticmethod
    def get_params(limit: int = 30, skip: int = 0) -> Dict:
        """Build query parameters for listing carts.

        Args:
            limit: Number of carts to return (default: 30)
            skip: Number of carts to skip for pagination (default: 0)

        Returns:
            Query parameters dictionary
        """
        return {"limit": limit, "skip": skip}


class CartGet:
    """Helper for getting a single cart by ID."""

    ENDPOINT = "/carts/"  # Use as /carts/{id} in steps
    SCHEMA = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "price": {"type": "number"},
                        "quantity": {"type": "integer"},
                        "total": {"type": "number"},
                        "discountPercentage": {"type": "number"},
                        "discountedTotal": {"type": "number"}
                    },
                    "required": ["id", "title", "price", "quantity", "total"]
                }
            },
            "total": {"type": "number"},
            "discountedTotal": {"type": "number"},
            "userId": {"type": "integer"},
            "totalProducts": {"type": "integer"},
            "totalQuantity": {"type": "integer"}
        },
        "required": ["id", "products", "total", "userId", "totalProducts", "totalQuantity"]
    }

    ERROR_404_SCHEMA = {
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": ["message"]
    }


class CartAdd:
    """Helper for creating a new cart."""

    ENDPOINT = "/carts/add"
    SCHEMA = CartGet.SCHEMA  # Same structure as single cart response

    @staticmethod
    def get_payload(user_id: int, products: List[Dict]) -> Dict:
        """Build request payload for creating a cart.

        Args:
            user_id: User ID for the cart
            products: List of product dictionaries with 'id' and 'quantity'
                     Example: [{"id": 1, "quantity": 2}, {"id": 5, "quantity": 1}]

        Returns:
            Cart creation request body dictionary
        """
        return {
            "userId": user_id,
            "products": products
        }


class CartUpdate:
    """Helper for updating an existing cart."""

    ENDPOINT = "/carts"  # Use as /carts/{id} in steps
    SCHEMA = CartGet.SCHEMA  # Same structure as single cart response

    @staticmethod
    def get_payload(products: List[Dict] = None) -> Dict:
        """Build request payload for updating a cart.

        Args:
            products: List of product dictionaries with 'id' and 'quantity'
                     Example: [{"id": 1, "quantity": 3}]

        Returns:
            Cart update request body dictionary
        """
        return {"products": products}


class CartDelete:
    """Helper for deleting a cart."""

    ENDPOINT = "/carts"  # Use as /carts/{id} in steps
    SCHEMA = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "products": {"type": "array"},
            "total": {"type": "number"},
            "discountedTotal": {"type": "number"},
            "userId": {"type": "integer"},
            "totalProducts": {"type": "integer"},
            "totalQuantity": {"type": "integer"},
            "isDeleted": {"type": "boolean"},
            "deletedOn": {"type": "string"}
        },
        "required": ["id", "isDeleted", "deletedOn"]
    }  # Returns deleted cart data
