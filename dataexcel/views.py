from django.db import connection
from decimal import Decimal
from django.shortcuts import render
from django.utils.dateformat import format as date_format
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.dateparse import parse_date
import json



def get_data_table_1():
    with connection.cursor() as cursor:
        # Ganti dengan query sesuai database kamu
        cursor.execute(
            """
                SELECT No_Invoice, Nama_Klien, tgl_Invoice, tgl_klien_Terima_Invoice,
                       Total_Tagihan, tgl_Pelunasan, Total_Pelunasan, Sisa_Tagihan,
                       Tgl_Jatuh_Tempo, tanggal_SPM1
                FROM View_WIBI_Tagihan_Belum_Lunas_Accurate_tanpa_TOP
                WHERE (tanggal_SPM1 <= { fn NOW() }) AND (tanggal_SPM2 > { fn NOW() })
                ORDER BY tanggal_SPM1
            """
        )
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    data = []
    hide_columns = set()

    for row in rows:
        row_dict = dict(zip(columns, row))
        for key, value in row_dict.items():
            if value is None:
                row_dict[key] = ''
        data.append(row_dict)

    return data

def get_data_table_2():
    with connection.cursor() as cursor:
        # Ganti dengan query sesuai database kamu
        cursor.execute(
            """
                SELECT No_Invoice, Nama_Klien, tgl_Invoice, tgl_klien_Terima_Invoice, Total_Tagihan, tgl_Pelunasan, Total_Pelunasan, Sisa_Tagihan, Tgl_Jatuh_Tempo, 
                tanggal_SPM1 , tanggal_SPM2 FROM View_WIBI_Tagihan_Belum_Lunas_Accurate_tanpa_TOP WHERE (tanggal_SOMASI > { fn NOW() }) AND (tanggal_SPM2 <= { fn NOW() }) ORDER BY tanggal_SPM2
            """
        )
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    data = []
    hide_columns = set()

    for row in rows:
        row_dict = dict(zip(columns, row))
        for key, value in row_dict.items():
            if value is None:
                row_dict[key] = ''
        data.append(row_dict)

    return data

def get_data_table_3():
    with connection.cursor() as cursor:
        # Ganti dengan query sesuai database kamu
        cursor.execute(
            """
SELECT No_Invoice, Nama_Klien, tgl_Invoice, tgl_klien_Terima_Invoice, Total_Tagihan, tgl_Pelunasan, Total_Pelunasan, Sisa_Tagihan, Tgl_Jatuh_Tempo, 
tanggal_SPM1 , tanggal_SPM2, tanggal_SOMASI FROM View_WIBI_Tagihan_Belum_Lunas_Accurate_tanpa_TOP WHERE  (tanggal_SOMASI <= { fn NOW() }) ORDER BY tanggal_SOMASI
            """
        )
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    data = []
    hide_columns = set()

    for row in rows:
        row_dict = dict(zip(columns, row))
        for key, value in row_dict.items():
            if value is None:
                row_dict[key] = ''
        data.append(row_dict)

    return data

def data_filter(request):
    # Ambil data dari SQL Server
    data_spm1 = get_data_table_1()
    data_spm2 = get_data_table_2()
    data_somasi = get_data_table_3()

    filter_columns = ['No_Invoice', 'Nama_Klien', 'tgl_Invoice', 'tgl_klien_Terima_Invoice', 'Total_Tagihan', 'tgl_Pelunasan', 'Total_Pelunasan', 'Sisa_Tagihan', 'Tgl_Jatuh_Tempo', 'tanggal_SPM1', 'tanggal_SPM2', 'tanggal_SOMASI']
    filters = {}    
    for kolom in filter_columns:
        values = request.GET.getlist(kolom)
        if values:
            filters[kolom] = values
    # Default data kosong kalau tidak ada filter dan bukan AJAX
    data_filtered1 = []
    data_filtered2 = []
    data_filtered3 = []

    # Kalau AJAX dan ada filter atau tombol process data (misal ada param process=1)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if filters:
            data_filtered1 = data_spm1
            data_filtered2 = data_spm2
            data_filtered3 = data_somasi
            for kolom, values in filters.items():
                data_filtered1 = [d for d in data_filtered1 if d.get(kolom) in values]
                data_filtered2 = [d for d in data_filtered2 if d.get(kolom) in values]
                data_filtered3 = [d for d in data_filtered3 if d.get(kolom) in values]
        elif request.GET.get('process') == '1':
            # Load semua data kalau ada param process=1 (tombol Process Data)
            data_filtered1 = data_spm1
            data_filtered2 = data_spm2
            data_filtered3 = data_somasi

        # Opsi dropdown tetap disiapkan untuk filter
        opsi_dropdown = {}
        for kolom in filter_columns:
            filters_except_current = {k: v for k, v in filters.items() if k != kolom}
            data_temp = data_spm1 + data_spm2 + data_somasi
            for k, v in filters_except_current.items():
                data_temp = [d for d in data_temp if d.get(k) in v]
            opsi_dropdown[kolom] = sorted(set(d.get(kolom) for d in data_temp if kolom in d))

        return JsonResponse({
            'data_spm1': data_filtered1,
            'data_spm2': data_filtered2,
            'data_somasi': data_filtered3,
            'opsi_dropdown': opsi_dropdown,
        })


    # Render template dengan data kosong saat load page pertama
    context = {
        'data_spm1': data_filtered1,
        'data_spm2': data_filtered2,
        'data_somasi': data_filtered3,
        'opsi_dropdown': {},  # bisa kosong atau sesuai kebutuhan
        'selected_filters': filters,
    }
    return render(request, 'BASE.html', context)
    

