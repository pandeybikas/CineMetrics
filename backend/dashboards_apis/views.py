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
        year= self.request.query_params("year")
        if year is None or '':
            return Response(
                {
                    'status': 'success',
                    'data': f'No data found for year {year}'
                }, status=status.HTTP_200_OK
            )
        executive_df= self.service_layer.get_executive_dashboard_data(year=year)
        