import os
from dotenv import load_dotenv

load_dotenv()

server_url = os.getenv("SERVER_URL", "https://your-default-domain.com")

schema = {
    "openapi": "3.1.0",
    "info": {
        "title": "MCP Control Server",
        "version": "1.0.0",
        "description": "A FastAPI server that executes shell commands and manages files remotely"
    },
    "servers": [
        {
            "url": server_url
        }
    ],
    "paths": {
        "/run": {
            "post": {
                "operationId": "run_command",
                "summary": "Run a shell command without returning output",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "command": {
                                        "type": "string",
                                        "description": "Shell command to execute"
                                    }
                                },
                                "required": ["command"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Command sent"
                    }
                }
            }
        },
        "/run-and-capture": {
            "post": {
                "operationId": "run_command_and_capture",
                "summary": "Run a shell command and return the output",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "command": {
                                        "type": "string",
                                        "description": "Shell command to execute"
                                    }
                                },
                                "required": ["command"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Command output returned"
                    }
                }
            }
        },
        "/file/create": {
            "post": {
                "operationId": "create_file",
                "summary": "Create a file with optional content",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "path": {
                                        "type": "string",
                                        "description": "Path where the file will be created"
                                    },
                                    "content": {
                                        "type": "string",
                                        "description": "Content to write in the file"
                                    }
                                },
                                "required": ["path"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "File created"
                    }
                }
            }
        },
        "/file/delete": {
            "post": {
                "operationId": "delete_file",
                "summary": "Delete a file or directory",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "path": {
                                        "type": "string",
                                        "description": "Path to the file or directory"
                                    }
                                },
                                "required": ["path"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "File or directory deleted"
                    }
                }
            }
        },
        "/file/rename": {
            "post": {
                "operationId": "rename_file",
                "summary": "Rename or move a file or directory",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "path": {
                                        "type": "string",
                                        "description": "Original file or directory path"
                                    },
                                    "new_path": {
                                        "type": "string",
                                        "description": "New file or directory path"
                                    }
                                },
                                "required": ["path", "new_path"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Renamed or moved successfully"
                    }
                }
            }
        },
        "/file/copy": {
            "post": {
                "operationId": "copy_file",
                "summary": "Copy a file or directory",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "path": {
                                        "type": "string",
                                        "description": "Source path"
                                    },
                                    "new_path": {
                                        "type": "string",
                                        "description": "Destination path"
                                    }
                                },
                                "required": ["path", "new_path"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "File or directory copied"
                    }
                }
            }
        },
        "/file/update": {
            "post": {
                "operationId": "update_file",
                "summary": "Update contents of a file using regex replacements",
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "path": {
                                        "type": "string",
                                        "description": "Path to the file to update"
                                    },
                                    "updates": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "pattern": {
                                                    "type": "string"
                                                },
                                                "replacement": {
                                                    "type": "string"
                                                }
                                            },
                                            "required": ["pattern", "replacement"]
                                        }
                                    }
                                },
                                "required": ["path", "updates"]
                            }
                        }    
                    }
                },
                "responses": {
                    "200": {
                        "description": "File updated successfully"
                    }
                }
            }
        }
    }
}
