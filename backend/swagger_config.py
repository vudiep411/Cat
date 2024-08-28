def get_swagger_config():
    return {
        'swagger': '2.0',
        'info': {
            'title': 'Cat API',
            'description': 'API to manage cats and user favorites',
            'version': '1.0.0'
        },
        'paths': {
            '/cats': {
                'get': {
                    'tags': ['Cats'],
                    'summary': 'Retrieve cat information with pagination',
                    'description': 'This endpoint retrieves cat information from the database with pagination.',
                    'parameters': [
                        {
                            'name': 'page',
                            'in': 'query',
                            'type': 'integer',
                            'default': 1,
                            'description': 'Page number to retrieve'
                        },
                        {
                            'name': 'limit',
                            'in': 'query',
                            'type': 'integer',
                            'default': 10,
                            'description': 'Number of cats per page'
                        },
                        {
                            'name': 'breed',
                            'in': 'query',
                            'type': 'string',
                            'default': '',
                            'description': 'Breed name to filter by'
                        },
                        {
                            'name': 'user_id',
                            'in': 'query',
                            'type': 'string',
                            'default': '',
                            'description': 'User ID to filter by'
                        },
                        {
                            'name': 'query',
                            'in': 'query',
                            'type': 'string',
                            'default': '',
                            'description': 'Search query'
                        }
                    ],
                    'responses': {
                        200: {
                            'description': 'A paginated list of cats',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'current_page': {'type': 'integer'},
                                    'total_pages': {'type': 'integer'},
                                    'total_cats': {'type': 'integer'},
                                    'cats': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {'type': 'string'},
                                                'image_url': {'type': 'string'},
                                                'breed_id': {'type': 'string'}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'post': {
                    'tags': ['Cats'],
                    'summary': 'Add a cat to user favorites',
                    'description': 'This endpoint allows a user to add a cat to their favorites by specifying the user ID, image ID, name, and description.',
                    'parameters': [
                        {
                            'name': 'body',
                            'in': 'body',
                            'description': 'Cat object that needs to be added to user favorites',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'user_id': {'type': 'integer', 'example': 1},
                                    'image_id': {'type': 'string', 'example': '12345'},
                                    'name': {'type': 'string', 'example': 'Fluffy'},
                                    'description': {'type': 'string', 'example': 'A cute fluffy cat'}
                                },
                                'required': ['user_id', 'image_id']
                            }
                        }
                    ],
                    'responses': {
                        200: {
                            'description': 'Cat added to favorites successfully',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'message': {'type': 'string'}
                                }
                            }
                        },
                        400: {
                            'description': 'Invalid input data',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'message': {'type': 'string'}
                                }
                            }
                        }
                    }
                },
            },
            '/cats/{id}': {
                'get': {
                    'tags': ['Cats'],
                    'summary': 'Retrieve a specific cat\'s details',
                    'description': 'This endpoint retrieves a specific cat\'s details based on its ID.',
                    'parameters': [
                        {
                            'name': 'id',
                            'in': 'path',
                            'type': 'string',
                            'required': True,
                            'description': 'The ID of the cat to retrieve'
                        }
                    ],
                    'responses': {
                        200: {
                            'description': 'Cat details retrieved successfully',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'string'},
                                    'image_url': {'type': 'string'},
                                    'breed': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {'type': 'string'},
                                            'name': {'type': 'string'},
                                            'weight': {'type': 'string'},
                                            'temperament': {'type': 'string'},
                                            'origin': {'type': 'string'},
                                            'description': {'type': 'string'},
                                            'life_span': {'type': 'string'},
                                            'indoor': {'type': 'integer'},
                                            'adaptability': {'type': 'integer'},
                                            'affection_level': {'type': 'integer'},
                                            'child_friendly': {'type': 'integer'},
                                            'dog_friendly': {'type': 'integer'},
                                            'energy_level': {'type': 'integer'},
                                            'grooming': {'type': 'integer'},
                                            'intelligence': {'type': 'integer'},
                                            'social_needs': {'type': 'integer'},
                                            'stranger_friendly': {'type': 'integer'}
                                        }
                                    }
                                }
                            }
                        },
                        404: {
                            'description': 'Cat not found',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'message': {'type': 'string'}
                                }
                            }
                        }
                    }
                },
                'put': {
                    'tags': ['Cats'],
                    'summary': 'Update a specific cat\'s details',
                    'description': 'This endpoint updates a specific cat\'s details based on its ID. Only fields that are provided will be updated.',
                    'parameters': [
                        {
                            'name': 'id',
                            'in': 'path',
                            'type': 'string',
                            'required': True,
                            'description': 'The ID of the cat to update'
                        },
                        {
                            'name': 'body',
                            'in': 'body',
                            'description': 'Cat object that needs to be updated',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'name': {'type': 'string'},
                                    'description': {'type': 'string'}
                                }
                            }
                        }
                    ],
                    'responses': {
                        200: {
                            'description': 'Cat details updated successfully',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'message': {'type': 'string'}
                                }
                            }
                        },
                        400: {
                            'description': 'Invalid input data',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'message': {'type': 'string'}
                                }
                            }
                        },
                        404: {
                            'description': 'Cat not found',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'message': {'type': 'string'}
                                }
                            }
                        }
                    }
                },
                'delete': {
                    'tags': ['Cats'],
                    'summary': 'Delete a cat from favorites',
                    'description': 'This endpoint removes a cat from the user\'s favorites by the favorite ID.',
                    'parameters': [
                            {
                                'name': 'id',
                                'in': 'path',
                                'type': 'string',
                                'required': True,
                                'description': 'The ID of the cat to retrieve'
                            }
                        ],
                    'responses': {
                        200: {
                            'description': 'Favorite cat successfully removed',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'message': {
                                        'type': 'string',
                                        'example': 'Favorite cat successfully removed'
                                    }
                                }
                            }
                        },
                        400: {
                            'description': 'Invalid ID provided',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'error': {
                                        'type': 'string',
                                        'example': 'Invalid favorite ID'
                                    }
                                }
                            }
                        },
                        404: {
                            'description': 'Favorite cat not found',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'error': {
                                        'type': 'string',
                                        'example': 'Favorite cat not found'
                                    }
                                }
                            }
                        }
                    }
                },
            },
            '/cats/favorite': {
                'get': {
                    'tags': ['Favorites'],
                    'summary': 'Retrieve a user\'s favorite cats',
                    'description': 'This endpoint retrieves a paginated list of a user\'s favorite cats.',
                    'parameters': [
                        {
                            'name': 'user_id',
                            'in': 'query',
                            'type': 'integer',
                            'required': True,
                            'description': 'The user ID to retrieve favorite cats for'
                        },
                        {
                            'name': 'page',
                            'in': 'query',
                            'type': 'integer',
                            'default': 1,
                            'description': 'Page number to retrieve'
                        },
                        {
                            'name': 'limit',
                            'in': 'query',
                            'type': 'integer',
                            'default': 10,
                            'description': 'Number of favorite cats per page'
                        }
                    ],
                    'responses': {
                        200: {
                            'description': 'A paginated list of favorite cats',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'current_page': {'type': 'integer'},
                                    'total_pages': {'type': 'integer'},
                                    'total_cats': {'type': 'integer'},
                                    'cats': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {'type': 'string'},
                                                'image_url': {'type': 'string'},
                                                'breed_name': {'type': 'string'},
                                                'weight': {'type': 'string'},
                                                'temperament': {'type': 'string'},
                                                'origin': {'type': 'string'},
                                                'description': {'type': 'string'},
                                                'life_span': {'type': 'string'},
                                                'indoor': {'type': 'integer'},
                                                'adaptability': {'type': 'integer'},
                                                'affection_level': {'type': 'integer'},
                                                'child_friendly': {'type': 'integer'},
                                                'dog_friendly': {'type': 'integer'},
                                                'energy_level': {'type': 'integer'},
                                                'grooming': {'type': 'integer'},
                                                'intelligence': {'type': 'integer'},
                                                'social_needs': {'type': 'integer'},
                                                'stranger_friendly': {'type': 'integer'}
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        400: {
                            'description': 'Invalid request parameters',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'message': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
