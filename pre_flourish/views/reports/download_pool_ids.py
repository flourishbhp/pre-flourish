import csv

from django.http import HttpResponse


def download_pool_ids_view(request, patient_ids):
    # Process the patient_ids and generate the CSV data
    csv_data = [['Patient ID']]
    pid_array = [pid.strip() for pid in patient_ids.split(',') if pid.strip()]
    # CSV header
    csv_data.extend([[patient_id] for patient_id in pid_array])  # CSV rows

    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_ids.csv"'

    # Write the CSV data to the response
    writer = csv.writer(response)
    writer.writerows(csv_data)

    return response
