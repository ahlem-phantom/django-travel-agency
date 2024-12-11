import numpy as np
from .models import TravelPackage

def calculate_recommendations(user_preferences):
    if not user_preferences:
        return []

    # Get all travel packages
    packages = TravelPackage.objects.all()

    recommendations = []
    for package in packages:
        # Calculate the similarity score
        package_tags = package.tags  
        score = sum(
            user_preferences.get(tag, 0) * package_tags.get(tag, 0)
            for tag in user_preferences.keys()
        )
        recommendations.append((package, score))
    
    # Sort by score (highest first) and return
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [package for package, score in recommendations[:5]]  # Top 5 packages
