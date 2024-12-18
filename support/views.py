# support/views.py
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("This is the support index.")
    
@csrf_exempt  
def handle_button_click(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if 'conversation_state' not in request.session:
            request.session['conversation_state'] = 'start' 

        conversation_state = request.session['conversation_state']
        
        if action == 'book':
            if conversation_state == 'start':
                response_message = 'Sure! Let me assist you with booking a trip. Can you please provide your destination?'
                request.session['conversation_state'] = 'booking_destination'
            elif conversation_state == 'booking_destination':
                response_message = 'Great! What dates are you planning to travel?'
                request.session['conversation_state'] = 'booking_dates'
            elif conversation_state == 'booking_dates':
                response_message = 'Awesome! I will now process your booking. Is there anything else you would like to know?'
                request.session['conversation_state'] = 'end_booking'
            else:
                response_message = 'Booking process completed. How else can I assist you?'
                request.session['conversation_state'] = 'start'
                
        elif action == 'travel-packages':
            if conversation_state == 'start':
                response_message = 'We have various travel packages. Are you looking for adventure, relaxation, or cultural experiences?'
                request.session['conversation_state'] = 'choosing_package'
            elif conversation_state == 'choosing_package':
                response_message = 'Here are some of our most popular packages. Would you like more details on any of them?'
                request.session['conversation_state'] = 'package_details'
            else:
                response_message = 'Can I assist you with anything else related to travel packages?'
                request.session['conversation_state'] = 'start'

        elif action == 'help':
            if conversation_state == 'start':
                response_message = 'How can I assist you today? Are you looking for trip bookings, travel packages, or something else?'
                request.session['conversation_state'] = 'help_inquiry'
            elif conversation_state == 'help_inquiry':
                response_message = 'I can help with booking trips or showing available travel packages. What would you prefer?'
                request.session['conversation_state'] = 'start'
            else:
                response_message = 'Please let me know how I can assist you further.'

        else:
            response_message = 'I am sorry, I didn’t understand that action. Can you please try again?'

        request.session.modified = True

        return JsonResponse({'message': response_message})

    return JsonResponse({'message': 'Invalid request'}, status=400)
