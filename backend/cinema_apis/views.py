import logging
from datetime import date
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from helper.serviceLayer import DatabaseQueryResult 

logger= logging.getLogger(__name__)

class MovieApi(APIView):
     service_layer= DatabaseQueryResult()

     def get(self, request):
            return self.top_5_movies(request)
     def top_5_movies(self, request):
           """
        Fetch and refine the top five highest-grossing movies
        for the supplied year.
        """
           year= request.query_params.get("year")
           try:
                movies_df= self.service_layer.get_top_5_movies(year=year)
                if movies_df.empty:
                       return Response(
                             {
                                   'status': 'success',
                                   'message': f'No movie data was found for year {year}'
                             }, status= status.HTTP_200_OK
                       )
                res= movies_df.to_dict(orient='records')
                return Response({'data': res})
           except Exception:
            logger.exception(
                "Failed to retrieve top five movies "
                "for year %s.",
                year,
            )

            return Response(
                {
                    "status": "error",
                    "message": (
                        "An error occurred while retrieving "
                        "movie analytics."
                    ),
                    "year": year,
                    "data": [],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

