"""
Custom OpenAPI schema for plain Django views
"""

def get_openapi_schema():
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "AI Prompt Library API",
            "version": "1.0.0",
            "description": "A production-grade REST API for managing and sharing AI prompts"
        },
        "servers": [
            {
                "url": "http://localhost:8000",
                "description": "Development server"
            }
        ],
        "paths": {
            "/prompts/": {
                "get": {
                    "summary": "List all prompts",
                    "description": "Returns a list of all prompts ordered by creation date (newest first)",
                    "operationId": "listPrompts",
                    "tags": ["Prompts"],
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/PromptList"
                                        }
                                    },
                                    "example": [
                                        {
                                            "id": 1,
                                            "title": "Write a Blog Post",
                                            "complexity": 5,
                                            "created_at": "2026-04-17T01:33:56.574734+00:00"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Create a new prompt",
                    "description": "Creates a new prompt with validation",
                    "operationId": "createPrompt",
                    "tags": ["Prompts"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/PromptCreate"
                                },
                                "example": {
                                    "title": "Write a Blog Post",
                                    "content": "Create an engaging blog post about artificial intelligence and its impact on modern society",
                                    "complexity": 5
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Prompt created successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/PromptDetail"
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Validation error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ValidationError"
                                    },
                                    "example": {
                                        "errors": {
                                            "title": "Title must be at least 3 characters",
                                            "content": "Content must be at least 20 characters",
                                            "complexity": "Complexity must be between 1 and 10"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/prompts/{id}/": {
                "get": {
                    "summary": "Get prompt details",
                    "description": "Returns detailed information about a specific prompt and increments its view count in Redis",
                    "operationId": "getPrompt",
                    "tags": ["Prompts"],
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "description": "Prompt ID",
                            "schema": {
                                "type": "integer"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/PromptDetailWithViews"
                                    },
                                    "example": {
                                        "id": 1,
                                        "title": "Write a Blog Post",
                                        "content": "Create an engaging blog post about artificial intelligence and its impact on modern society",
                                        "complexity": 5,
                                        "created_at": "2026-04-17T01:33:56.574734+00:00",
                                        "view_count": 3
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Prompt not found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Error"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "PromptList": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "Unique identifier"
                        },
                        "title": {
                            "type": "string",
                            "description": "Prompt title"
                        },
                        "complexity": {
                            "type": "integer",
                            "description": "Complexity rating (1-10)",
                            "minimum": 1,
                            "maximum": 10
                        },
                        "created_at": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Creation timestamp"
                        }
                    }
                },
                "PromptCreate": {
                    "type": "object",
                    "required": ["title", "content", "complexity"],
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Prompt title (min 3 characters)",
                            "minLength": 3
                        },
                        "content": {
                            "type": "string",
                            "description": "Prompt content (min 20 characters)",
                            "minLength": 20
                        },
                        "complexity": {
                            "type": "integer",
                            "description": "Complexity rating (1-10)",
                            "minimum": 1,
                            "maximum": 10
                        }
                    }
                },
                "PromptDetail": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "title": {
                            "type": "string"
                        },
                        "content": {
                            "type": "string"
                        },
                        "complexity": {
                            "type": "integer"
                        },
                        "created_at": {
                            "type": "string",
                            "format": "date-time"
                        }
                    }
                },
                "PromptDetailWithViews": {
                    "allOf": [
                        {
                            "$ref": "#/components/schemas/PromptDetail"
                        },
                        {
                            "type": "object",
                            "properties": {
                                "view_count": {
                                    "type": "integer",
                                    "description": "Number of times this prompt has been viewed"
                                }
                            }
                        }
                    ]
                },
                "ValidationError": {
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "string"
                            }
                        }
                    }
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
