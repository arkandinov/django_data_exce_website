from django.db import connection
from decimal import Decimal
from django.shortcuts import render
from django.utils.dateformat import format as date_format

def format_rupiah(angka):
    try:
        return f"{angka:,.0f}"
    except: 
        return angka

def process_data(request):
    data = []
    hide_columns = set()

    if request.method == 'POST':
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
            nominal_flags = {col: True for col in nominal_columns}  # Asumsinya semua kosong

            for row in rows:
                row_dict = dict(zip(columns, row))

                for key in row_dict:
                    value = row_dict[key]

                    if value is None:
                        row_dict[key] = ''
                    elif isinstance(value, (int, float, Decimal)) and ('Total' in key or 'Sisa' in key):
                        if value != 0:
                            nominal_flags[key] = False
                        row_dict[key] = format_rupiah(value)
                    elif 'tgl' in key.lower() or 'tanggal' in key.lower():
                        row_dict[key] = date_format(value, "d-m-y")

                data.append(row_dict)
            
            # Tentukan kolom nominal mana yang perlu disembunyikan
            for col, is_all_empty in nominal_flags.items():
                if is_all_empty:
                    hide_columns.add(col)

            # Hapus kolom yang disembunyikan dari tiap baris data
            for row in data:
                for col in hide_columns:
                    row.pop(col, None)

            selected_No_Invoice = request.GET.getlist('No_Invoice')
            selected_Nama_Klien = request.GET.getlist('Nama_Klien')
            selected_tgl_Invoice = request.GET.getlist('tgl_Invoice')
            selected_tgl_klien_Terima_Invoice = request.GET.getlist('tgl_klien_Terima_Invoice')
            selected_Total_Tagihan = request.GET.getlist('Total_Tagihan')
            selected_tgl_Pelunasan = request.GET.getlist('tgl_Pelunasan')
            selected_Sisa_Tagihan = request.GET.getlist('Sisa_Tagihan')
            selected_Tgl_Jatuh_Tempo = request.GET.getlist('Tgl_Jatuh_Tempo')
            selected_tanggal_SPM1 = request.GET.getlist('tanggal_SPM1')

            data_filtered = data
            if selected_No_Invoice:
                data_filtered = [d for d in data_filtered if d['No_Invoice'] in selected_No_Invoice]
            if selected_Nama_Klien:
                data_filtered = [d for d in data_filtered if d['Nama_Klien'] in selected_Nama_Klien]
            if selected_tgl_Invoice:
                data_filtered = [d for d in data_filtered if d['tgl_Invoice'] in selected_tgl_Invoice]
            if selected_tgl_klien_Terima_Invoice:
                data_filtered = [d for d in data_filtered if d['tgl_klien_Terima_Invoice'] in selected_tgl_klien_Terima_Invoice]
            if selected_Total_Tagihan:
                data_filtered = [d for d in data_filtered if d['Total_Tagihan'] in selected_Total_Tagihan]
            if selected_tgl_Pelunasan:
                data_filtered = [d for d in data_filtered if d['tgl_Pelunasan'] in selected_tgl_Pelunasan]
            if selected_Sisa_Tagihan:
                data_filtered = [d for d in data_filtered if d['Sisa_Tagihan'] in selected_Sisa_Tagihan]
            if selected_Tgl_Jatuh_Tempo:
                data_filtered = [d for d in data_filtered if d['Tgl_Jatuh_Tempo'] in selected_Tgl_Jatuh_Tempo]
            if selected_tanggal_SPM1:
                data_filtered = [d for d in data_filtered if d['tanggal_SPM1'] in selected_tanggal_SPM1]

            All_No_Invoice = sorted(set(
                d['No_Invoice'] for d in data if not selected_No_Invoice or d['Nama_Klien'] in selected_Nama_Klien or d['tgl_Invoice'] in selected_tgl_Invoice or d['tgl_klien_Terima_Invoice'] in selected_tgl_klien_Terima_Invoice or d['Total_Tagihan'] in selected_Total_Tagihan or d['tgl_Pelunasan'] in selected_tgl_Pelunasan or d['Sisa_Tagihan'] in selected_Sisa_Tagihan or d['Tgl_Jatuh_Tempo'] in selected_Tgl_Jatuh_Tempo or d['tanggal_SPM1'] in selected_tanggal_SPM1
            ))
            All_Nama_Klien = sorted(set(
                d['Nama_Klien'] for d in data if not selected_Nama_Klien or d['No_Invoice'] in selected_No_Invoice or d['tgl_Invoice'] in selected_tgl_Invoice or d['tgl_klien_Terima_Invoice'] in selected_tgl_klien_Terima_Invoice or d['Total_Tagihan'] in selected_Total_Tagihan or d['tgl_Pelunasan'] in selected_tgl_Pelunasan or d['Sisa_Tagihan'] in selected_Sisa_Tagihan or d['Tgl_Jatuh_Tempo'] in selected_Tgl_Jatuh_Tempo or d['tanggal_SPM1'] in selected_tanggal_SPM1
            ))
            All_tgl_Invoice = sorted(set(
                d['tgl_Invoice'] for d in data if not selected_tgl_Invoice or d['No_Invoice'] in selected_No_Invoice or d['Nama_Klien'] in selected_Nama_Klien or d['tgl_klien_Terima_Invoice'] in selected_tgl_klien_Terima_Invoice or d['Total_Tagihan'] in selected_Total_Tagihan or d['tgl_Pelunasan'] in selected_tgl_Pelunasan or d['Sisa_Tagihan'] in selected_Sisa_Tagihan or d['Tgl_Jatuh_Tempo'] in selected_Tgl_Jatuh_Tempo or d['tanggal_SPM1'] in selected_tanggal_SPM1
            ))
            All_tgl_klien_Terima_Invoice = sorted(set(
                d['tgl_klien_Terima_Invoice'] for d in data if not selected_tgl_klien_Terima_Invoice or d['No_Invoice'] in selected_No_Invoice or d['Nama_Klien'] in selected_Nama_Klien or d['tgl_Invoice'] in selected_tgl_Invoice or d['Total_Tagihan'] in selected_Total_Tagihan or d['tgl_Pelunasan'] in selected_tgl_Pelunasan or d['Sisa_Tagihan'] in selected_Sisa_Tagihan or d['Tgl_Jatuh_Tempo'] in selected_Tgl_Jatuh_Tempo or d['tanggal_SPM1'] in selected_tanggal_SPM1
            ))
            All_Total_Tagihan = sorted(set(
                d['Total_Tagihan'] for d in data if not selected_Total_Tagihan or d['No_Invoice'] in selected_No_Invoice or d['Nama_Klien'] in selected_Nama_Klien or d['tgl_Invoice'] in selected_tgl_Invoice or d['tgl_klien_Terima_Invoice'] in selected_tgl_klien_Terima_Invoice or d['tgl_Pelunasan'] in selected_tgl_Pelunasan or d['Sisa_Tagihan'] in selected_Sisa_Tagihan or d['Tgl_Jatuh_Tempo'] in selected_Tgl_Jatuh_Tempo or d['tanggal_SPM1'] in selected_tanggal_SPM1
            ))
            All_tgl_Pelunasan = sorted(set(
                d['tgl_Pelunasan'] for d in data if not selected_tgl_Pelunasan or d['No_Invoice'] in selected_No_Invoice or d['Nama_Klien'] in selected_Nama_Klien or d['tgl_Invoice'] in selected_tgl_Invoice or d['tgl_klien_Terima_Invoice'] in selected_tgl_klien_Terima_Invoice or d['Total_Tagihan'] in selected_Total_Tagihan or d['Sisa_Tagihan'] in selected_Sisa_Tagihan or d['Tgl_Jatuh_Tempo'] in selected_Tgl_Jatuh_Tempo or d['tanggal_SPM1'] in selected_tanggal_SPM1
            ))
            All_Sisa_Tagihan = sorted(set(
                d['Sisa_Tagihan'] for d in data if not selected_Sisa_Tagihan or d['No_Invoice'] in selected_No_Invoice or d['Nama_Klien'] in selected_Nama_Klien or d['tgl_Invoice'] in selected_tgl_Invoice or d['tgl_klien_Terima_Invoice'] in selected_tgl_klien_Terima_Invoice or d['Total_Tagihan'] in selected_Total_Tagihan or d['tgl_Pelunasan'] in selected_tgl_Pelunasan or d['Tgl_Jatuh_Tempo'] in selected_Tgl_Jatuh_Tempo or d['tanggal_SPM1'] in selected_tanggal_SPM1
            ))
            All_Tgl_Jatuh_Tempo = sorted(set(
                d['Tgl_Jatuh_Tempo'] for d in data if not selected_Tgl_Jatuh_Tempo or d['No_Invoice'] in selected_No_Invoice or d['Nama_Klien'] in selected_Nama_Klien or d['tgl_Invoice'] in selected_tgl_Invoice or d['tgl_klien_Terima_Invoice'] in selected_tgl_klien_Terima_Invoice or d['Total_Tagihan'] in selected_Total_Tagihan or d['tgl_Pelunasan'] in selected_tgl_Pelunasan or d['Sisa_Tagihan'] in selected_Sisa_Tagihan or d['tanggal_SPM1'] in selected_tanggal_SPM1
            ))
            All_tanggal_SPM1 = sorted(set(
                d['tanggal_SPM1'] for d in data if not selected_tanggal_SPM1 or d['No_Invoice'] in selected_No_Invoice or d['Nama_Klien'] in selected_Nama_Klien or d['tgl_Invoice'] in selected_tgl_Invoice or d['tgl_klien_Terima_Invoice'] in selected_tgl_klien_Terima_Invoice or d['Total_Tagihan'] in selected_Total_Tagihan or d['tgl_Pelunasan'] in selected_tgl_Pelunasan or d['Sisa_Tagihan'] in selected_Sisa_Tagihan or d['Tgl_Jatuh_Tempo'] in selected_Tgl_Jatuh_Tempo
            ))

            context = {
                'data': data,
                'data': data_filtered,
                'selected_No_Invoice': selected_No_Invoice,
                'selected_Nama_Klien': selected_Nama_Klien,
                'selected_tgl_Invoice': selected_tgl_Invoice,
                'selected_tgl_klien_Terima_Invoice': selected_tgl_klien_Terima_Invoice,
                'selected_Total_Tagihan': selected_Total_Tagihan,
                'selected_tgl_Pelunasan': selected_tgl_Pelunasan,
                'selected_Sisa_Tagihan': selected_Sisa_Tagihan,
                'selected_Tgl_Jatuh_Tempo': selected_Tgl_Jatuh_Tempo,
                'selected_tanggal_SPM1': selected_tanggal_SPM1,
                'All_No_Invoice': All_No_Invoice,
                'All_Nama_Klien': All_Nama_Klien,
                'All_tgl_Invoice': All_tgl_Invoice,
                'All_tgl_klien_Terima_Invoice': All_tgl_klien_Terima_Invoice,
                'All_Total_Tagihan': All_Total_Tagihan,
                'All_tgl_Pelunasan': All_tgl_Pelunasan,
                'All_Sisa_Tagihan': All_Sisa_Tagihan,
                'All_Tgl_Jatuh_Tempo': All_Tgl_Jatuh_Tempo,
                'All_tanggal_SPM1': All_tanggal_SPM1,
                'hide_columns': hide_columns,
                'nominal_flags': nominal_flags
            }
    return render(request, 'index.html', context)