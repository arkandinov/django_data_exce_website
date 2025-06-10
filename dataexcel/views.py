from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
import datetime
import decimal
import math

# Pastikan fungsi-fungsi ini mengembalikan semua nilai sebagai string bersih
def get_data_table_1():
    with connection.cursor() as cursor:
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
    for row_values in rows:
        row_dict = {}
        for i, col_name in enumerate(columns):
            val = row_values[i]
            if isinstance(val, datetime.datetime):
                row_dict[col_name] = val.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(val, decimal.Decimal):
                row_dict[col_name] = str(val)
            elif val is None:
                row_dict[col_name] = ''
            else:
                row_dict[col_name] = str(val).strip()
        data.append(row_dict)
    return data

def get_data_table_2():
    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT No_Invoice, Nama_Klien, tgl_Invoice, tgl_klien_Terima_Invoice, Total_Tagihan, 
                       tgl_Pelunasan, Total_Pelunasan, Sisa_Tagihan, Tgl_Jatuh_Tempo, 
                       tanggal_SPM1, tanggal_SPM2 
                FROM View_WIBI_Tagihan_Belum_Lunas_Accurate_tanpa_TOP 
                WHERE (tanggal_SOMASI > { fn NOW() }) AND (tanggal_SPM2 <= { fn NOW() }) 
                ORDER BY tanggal_SPM2
            """
        )
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    data = []
    for row_values in rows:
        row_dict = {}
        for i, col_name in enumerate(columns):
            val = row_values[i]
            if isinstance(val, datetime.datetime):
                row_dict[col_name] = val.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(val, decimal.Decimal):
                row_dict[col_name] = str(val)
            elif val is None:
                row_dict[col_name] = ''
            else:
                row_dict[col_name] = str(val).strip()
        data.append(row_dict)
    return data

def get_data_table_3():
    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT No_Invoice, Nama_Klien, tgl_Invoice, tgl_klien_Terima_Invoice, Total_Tagihan, 
                       tgl_Pelunasan, Total_Pelunasan, Sisa_Tagihan, Tgl_Jatuh_Tempo, 
                       tanggal_SPM1, tanggal_SPM2, tanggal_SOMASI 
                FROM View_WIBI_Tagihan_Belum_Lunas_Accurate_tanpa_TOP 
                WHERE (tanggal_SOMASI <= { fn NOW() }) 
                ORDER BY tanggal_SOMASI
            """
        )
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    data = []
    for row_values in rows:
        row_dict = {}
        for i, col_name in enumerate(columns):
            val = row_values[i]
            if isinstance(val, datetime.datetime):
                row_dict[col_name] = val.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(val, decimal.Decimal):
                row_dict[col_name] = str(val)
            elif val is None:
                row_dict[col_name] = ''
            else:
                row_dict[col_name] = str(val).strip()
        data.append(row_dict)
    return data


def data_filter(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        draw = int(request.GET.get('draw', 0))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        if length == -1: 
            length = 1000000 
            
        order_column_index_str = request.GET.get('order[0][column]')
        order_dir = request.GET.get('order[0][dir]', 'asc')
        table_key = request.GET.get('table_key', '').upper()

        table_column_configs = {
            'SPM1': ['No_Invoice', 'Nama_Klien', 'tgl_Invoice', 'tgl_klien_Terima_Invoice', 'Total_Tagihan', 'tgl_Pelunasan', 'Total_Pelunasan', 'Sisa_Tagihan', 'Tgl_Jatuh_Tempo', 'tanggal_SPM1'],
            'SPM2': ['No_Invoice', 'Nama_Klien', 'tgl_Invoice', 'tgl_klien_Terima_Invoice', 'Total_Tagihan', 'tgl_Pelunasan', 'Total_Pelunasan', 'Sisa_Tagihan', 'Tgl_Jatuh_Tempo', 'tanggal_SPM1', 'tanggal_SPM2'],
            'SOMASI': ['No_Invoice', 'Nama_Klien', 'tgl_Invoice', 'tgl_klien_Terima_Invoice', 'Total_Tagihan', 'tgl_Pelunasan', 'Total_Pelunasan', 'Sisa_Tagihan', 'Tgl_Jatuh_Tempo', 'tanggal_SPM1', 'tanggal_SPM2', 'tanggal_SOMASI']
        }
        if not table_key or table_key not in table_column_configs:
            return JsonResponse({'error': 'table_key tidak valid.'}, status=400)

        current_table_cols = table_column_configs[table_key]
        raw_data = []
        if table_key == 'SPM1': raw_data = get_data_table_1()
        elif table_key == 'SPM2': raw_data = get_data_table_2()
        elif table_key == 'SOMASI': raw_data = get_data_table_3()
        
        records_total = len(raw_data)
        data_after_filters = list(raw_data) 

        # 2. Sanitasi & Terapkan Filter
        sanitized_raw_data = [{k: v for k, v in row.items()} for row in raw_data]
        data_after_filters = list(sanitized_raw_data)
        
        active_popup_filters = {}
        # Use current_table_cols instead of undefined canonical_cols
        for col_name in current_table_cols:
            filter_values = request.GET.getlist(col_name) or request.GET.getlist(col_name + '[]')
            if filter_values:
                cleaned_values = [val.strip().lower() for val in filter_values if val.strip()]
                if cleaned_values: active_popup_filters[col_name] = cleaned_values
        
        if active_popup_filters:
            for col_name, stripped_vals in active_popup_filters.items():
                if stripped_vals:
                    data_after_filters = [row for row in data_after_filters if str(row.get(col_name, '')).lower() in stripped_vals]
        
        records_total = len(sanitized_raw_data)
        records_filtered = len(data_after_filters)

        if length > 0 and records_filtered > 0 : 
            if start >= records_filtered:
                start = math.floor((records_filtered - 1) / length) * length
            if start < 0:
                start = 0
        elif records_filtered == 0: 
             start = 0 
        
        data_for_current_page = data_after_filters[start : start + length]
        paginated_data = list(data_for_current_page) 

        if order_column_index_str is not None:
            try:
                order_column_index = int(order_column_index_str)
                if 0 <= order_column_index < len(current_table_cols):
                    column_to_sort = current_table_cols[order_column_index]
                    def sort_key_func(item):
                        val_str = item.get(column_to_sort, '') 
                        if column_to_sort in ['Total_Tagihan', 'Total_Pelunasan', 'Sisa_Tagihan']:
                            try: return float(val_str) if val_str else float('-inf')
                            except ValueError: return float('-inf') 
                        return val_str.lower() 
                    paginated_data.sort(key=sort_key_func, reverse=(order_dir == 'desc'))
            except ValueError: pass

        opsi_dropdown = {}
        if sanitized_raw_data:
            for col_name in current_table_cols:
                data_untuk_opsi = list(sanitized_raw_data)
                for f_col, f_vals in active_popup_filters.items():
                    if f_col != col_name:
                        data_untuk_opsi = [row for row in data_untuk_opsi if str(row.get(f_col, '')).lower() in f_vals]
                unique_values = sorted(list(set(str(row.get(col_name, '')) for row in data_untuk_opsi if str(row.get(col_name, '')).strip() != '')))
                opsi_dropdown[col_name] = unique_values
            
        return JsonResponse({
            'draw': draw, 
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': paginated_data,
            'opsi_dropdown': opsi_dropdown,
        })

    context = {}
    return render(request, 'BASE.html', context)