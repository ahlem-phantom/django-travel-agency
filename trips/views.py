from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .recommendations import calculate_recommendations
from .models import TravelPackage
from .serializers import TravelPackageSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .forms import TravelPackageForm

class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    
    # Get trips package recommendations for the user
    def get(self, request):
        user = request.user
        recommendations = calculate_recommendations(user.preferences)
        serializer = TravelPackageSerializer(recommendations, many=True)
        return Response(serializer.data)


# List all trips packages
def package_list(request):
    packages = TravelPackage.objects.all()
    return render(request, 'package_list.html', {'packages': packages})

# View a single trips package
def package_detail(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)
    return render(request, 'package_detail.html', {'package': package})

# Create a new trips package
def package_create(request):
    if request.method == 'POST':
        form = TravelPackageForm(request.POST, request.FILES)  # Ensure the form is handling file uploads
        if form.is_valid():
            form.save()
            return redirect('trips:package_list')
    else:
        form = TravelPackageForm()
    return render(request, 'package_form.html', {'form': form})

# Update an existing trips package
def package_update(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)
    if request.method == 'POST':
        form = TravelPackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            return redirect('trips:package_list')
    else:
        form = TravelPackageForm(instance=package)
    return render(request, 'package_form.html', {'form': form})

# Delete a trips package
def package_delete(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)
    if request.method == 'POST':
        package.delete()
        return redirect('trips:package_list')
    return render(request, 'package_confirm_delete.html', {'package': package})


# View for displaying the trip details
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    
    # Check if the user has already rated this trip
    existing_rating = Rating.objects.filter(user=request.user, trip=trip).first()
    
    # Display the trip details with rating options
    return render(request, 'trip_detail.html', {
        'trip': trip,
        'existing_rating': existing_rating,
        'form': RatingForm()  # Rating form for new users to rate
    })