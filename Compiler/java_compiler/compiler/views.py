from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def compiler(request):
    return render(request, 'compiler.html')

@csrf_exempt
def run_java_code(request):
    if request.method == 'POST':
        # Get the code from the frontend
        code = request.POST.get('code')

        # JDoodle API details
        client_id = '6febf10994f967e27484a5794427ad72'
        client_secret = 'fa0747fbffad99979b1011bbf4bc732002f386d37cc341198efd5bc27b7a4f7a'

        # Prepare the request data
        payload = {
            'script': code,
            'language': 'java',
            'versionIndex': '3',
            'clientId': client_id,
            'clientSecret': client_secret
        }

        # Make the request to JDoodle API
        response = requests.post('https://api.jdoodle.com/v1/execute', json=payload)

        # Process the API response
        if response.status_code == 200:
            result = response.json()
            output = result.get('output', 'No output available.')
            error = result.get('error', '')
            if error:
                output = error  # If there is an error, show the error message
        else:
            output = 'Error executing the code'

        # Return the result as context to render back into the template
        return render(request, 'compiler.html', {'output': output})

    return render(request, 'compiler.html', {'output': 'Invalid request method'})
