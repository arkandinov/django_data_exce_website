from django.db import connection
from decimal import Decimal
from django.shortcuts import render
from django.utils.dateformat import format as date_format
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.dateparse import parse_date
import json



def format_rupiah(angka):
    try:
        return f"{angka:,.0f}"
    except: 
        return angka
def home(request):
    return render(request, 'index.html')

@csrf_exempt
def process_data(request):
    if request.method == 'GET':
        data = []
        hide_columns = set()

        with connection.cursor() as cursor:
            query = """
                SELECT No_Invoice, Nama_Klien, tgl_Invoice, tgl_klien_Terima_Invoice,
                       Total_Tagihan, tgl_Pelunasan, Total_Pelunasan, Sisa_Tagihan,
                       Tgl_Jatuh_Tempo, tanggal_SPM1
                FROM View_WIBI_Tagihan_Belum_Lunas_Accurate_tanpa_TOP
                WHERE (tanggal_SPM1 <= { fn NOW() }) AND (tanggal_SPM2 > { fn NOW() })
                ORDER BY tanggal_SPM1
            """
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

            nominal_columns = ['Total_Tagihan', 'Total_Pelunasan', 'Sisa_Tagihan']
            nominal_flags = {col: True for col in nominal_columns}

            for row in rows:
                row_dict = dict(zip(columns, row))

                for key, value in row_dict.items():
                    if value is None:
                        row_dict[key] = ''
                    elif isinstance(value, (int, float, Decimal)) and key in nominal_columns:
                        if value != 0:
                            nominal_flags[key] = False
                        row_dict[key] = format_rupiah(value)
                    elif 'tgl' in key.lower() or 'tanggal' in key.lower():
                        row_dict[key] = date_format(value, "d-m-Y")

                data.append(row_dict)

            for col, is_all_empty in nominal_flags.items():
                if is_all_empty:
                    hide_columns.add(col)

            for row in data:
                for col in hide_columns:
                    row.pop(col, None)

        return JsonResponse(data, safe=False)

