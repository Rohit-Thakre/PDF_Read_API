from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status

from PyPDF2 import PdfReader
from io import BytesIO
import csv
from io import StringIO
import re

class PDF_TO_CSV(APIView):

    def post(self, request): 
        try: 
            pdf_file = request.FILES['pdf']

            pdf_data = pdf_file.read()

            # Create a BytesIO object using the PDF data
            pdf_stream = BytesIO(pdf_data)

            # Use PdfReader to read the PDF data from the BytesIO object
            pdf = PdfReader(pdf_stream)

            page_size = len(pdf.pages)
            row = []

            # Prepare CSV output
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(['POSTING DATE','VALUE DATE', 'DESCRIPTION','AMOUNT','ACCOUNT BALANCE'])

            for no in range(page_size): 
                page_obj = pdf.pages[no]    
                # start_from 120
                page_text = page_obj.extract_text()[120:]

                page_list = re.split(r'OMR\n', page_text)
                # last me ORM add karn hai, since ORM\n se splite kr rahe hai to vo remove kiya hai 

                for line in page_list:
                    try:
                        posting_date = re.findall(r'\d{2}\s\w{3}\s\d{4}', line)[0]
                        value_date = re.findall(r'\d{2}\s\w{3}\s\d{4}', line)[1]

                        line = line+'OMR'

                        amt = re.findall(r'\-*\d{1,3}\.\d{1,}\sOMR', line)
                        amount = amt[0]
                        ac_bal = amt[1]

                        des = line[23: ]
                        des = re.sub(r"\-*\d{1,3}\.\d{1,}\sOMR", " ", des)
                        description = re.sub(r"\-*\d{1,3}\.\d{1,}\sOMR", " ", des)

                        row = [posting_date.strip() , value_date.strip(), description.strip(), amount.strip(), ac_bal.strip()]

                        csv_writer.writerow(row) 

                    except:
                        return Response({'msg' : 'Error occured while processing pdf file'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            
            # Return CSV file as a response
            response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="output.csv"'
           
            return response
        

        except: 
            return Response({'msg':'pdf files expected.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            


    
