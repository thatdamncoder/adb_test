from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json, logging, os
from pymongo import MongoClient
from bson.json_util import dumps

mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
db = MongoClient(mongo_uri)['test_db']

#MongoDB collection object used for persisting and retrieving todo items.
todo_collection = db['todos']

class TodoListView(APIView):

    def get(self, request):
        # Implement this method - return all todo items from db instance above.
        """
        Retrieves a list of all todo items from the MongoDB collection.
        The data is fetched, serialized to valid JSON format and returned to 
        the client.

        Args:
            request (Request): The incoming GET request.
        Returns:
            Response: A Response object containing a JSON array of todo items
                      with HTTP 200 OK status.
                      Example body: [{"_id": {"$oid": "..."}}, "description": "task 1", ...]
        Raises:
            Response (HTTP 500): If a database connection or query error occurs.
        """
        try:
            todo_items = todo_collection.find()
            json_data = dumps(todo_items)

            return Response(
                json.loads(json_data), 
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            logging.error(f"MongoDB GET error: {e}")
            return Response(
                {"error": "Failed to fetch todos GET"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def post(self, request):
        # Implement this method - accept a todo item in a mongo collection, persist it using db instance above.
        """ 
        Creates and persists a new todo item to the MongoDB collection.
        The 'completed' field is automatically set to False upon creation.

        Args:
            request (Request): The incoming POST request containing the data
                                Expected data: {"description": "Task details"}
        Returns:
            Response: A Response object with a message and the unique ID of the 
                      new To-Do, status 201 CREATED.
        Raises:
            Response (HTTP 400): If the required 'description' field is missing 
                                 in the request data.
            Response (HTTP 500): If a database insertion error occurs.
        """
        if 'description' not in request.data:
            return Response(
                {"error": "Field 'description' is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            todo_item = {
                "description": request.data['description'],
                "completed": False
            }
            result = todo_collection.insert_one(todo_item)

            return Response({
                "message": "Todo created successfully.",
                "id": str(result.inserted_id)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logging.error(f"MongoDB POST error: {e}")
            return Response(
                {"error": "Failed to create todo."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

