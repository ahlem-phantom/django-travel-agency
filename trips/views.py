from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .recommendations import calculate_recommendations
from .models import TravelPackage
from .serializers import TravelPackageSerializer

class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        recommendations = calculate_recommendations(user.preferences)
        serializer = TravelPackageSerializer(recommendations, many=True)
        return Response(serializer.data)
