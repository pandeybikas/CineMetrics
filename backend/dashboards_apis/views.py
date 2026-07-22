import logging
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from helper.serviceLayer import DatabaseQueryResult

logger= logging.getLogger(__name__)

class DashboardApi(APIView):
    service_layer= DatabaseQueryResult()

    def get(self, request):
        return self.executive_dashboard(request)
    
    def executive_dashboard(self, request):
        year= request.query_params.get("year")
        if year is None or '':
            return Response(
                {
                    'status': 'success',
                    'data': f'No data found for year {year}'
                }, status=status.HTTP_200_OK
            )
        executive_df= self.service_layer.get_executive_dashboard_data(year=year)
        movies_df= executive_df.copy()
        numeric_columns= ["budget", "revenue", "runtime", "popularity", "vote_average", "vote_count"]
        for column in numeric_columns:
            movies_df[column]= pd.to_numeric(movies_df[column], errors="coerce")
        movies_df["release_date"]= pd.to_datetime(movies_df["release_date"], errors="coerce")
        movies_df= movies_df.drop_duplicates(subset=["id"], keep="last")
        res= movies_df.to_dict(orient='records')
        return Response(
            {
                "message": "success",
                "data": res,


            }, status=status.HTTP_200_OK
        )
        