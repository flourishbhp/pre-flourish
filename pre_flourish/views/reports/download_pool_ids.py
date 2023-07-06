import csv
import ast
from django.http import HttpResponse


def download_pool_ids_view(request, patient_ids):
    # Process the patient_ids and generate the CSV data
    csv_data = [['Patient ID']]

    patient_ids = patient_ids.strip('""')

    # Evaluate the string literal and convert it to a list
    result = ast.literal_eval(patient_ids)
    # CSV header
    csv_data.extend([[patient_id] for patient_id in result])  # CSV rows

    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_ids.csv"'

    # Write the CSV data to the response
    writer = csv.writer(response)
    writer.writerows(csv_data)

    return response
