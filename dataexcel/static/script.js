$(document).ready(function () {
  const tableConfigs = {
    SPM1: {
      tableId: "#table_SPM1",
      dataKey: "data_spm1",
      filters: {
        No_Invoice: [],
        Nama_Klien: [],
        tgl_Invoice: [],
        tgl_klien_Terima_Invoice: [],
        Total_Tagihan: [],
        tgl_Pelunasan: [],
        Total_Pelunasan: [],
        Sisa_Tagihan: [],
        Tgl_Jatuh_Tempo: [],
        tanggal_SPM1: [],
      },
      dataTable: null,
      fullData: [],
    },
    SPM2: {
      tableId: "#table_SPM2",
      dataKey: "data_spm2",
      filters: {
        No_Invoice: [],
        Nama_Klien: [],
        tgl_Invoice: [],
        tgl_klien_Terima_Invoice: [],
        Total_Tagihan: [],
        tgl_Pelunasan: [],
        Total_Pelunasan: [],
        Sisa_Tagihan: [],
        Tgl_Jatuh_Tempo: [],
        tanggal_SPM1: [],
        tanggal_SPM2: [],
      },
      dataTable: null,
      fullData: [],
    },
    SOMASI: {
      tableId: "#table_SOMASI",
      dataKey: "data_somasi",
      filters: {
        No_Invoice: [],
        Nama_Klien: [],
        tgl_Invoice: [],
        tgl_klien_Terima_Invoice: [],
        Total_Tagihan: [],
        tgl_Pelunasan: [],
        Total_Pelunasan: [],
        Sisa_Tagihan: [],
        Tgl_Jatuh_Tempo: [],
        tanggal_SPM1: [],
        tanggal_SPM2: [],
        tanggal_SOMASI: [],
      },
      dataTable: null,
      fullData: [],
    },
  };

  let currentTableKey = "";
  let currentColumn = "";

  function formatRupiah(angka) {
    if (!angka) return "Rp 0";
    return (
      "Rp " +
      parseInt(angka, 10)
        .toString()
        .replace(/\B(?=(\d{3})+(?!\d))/g, ".")
    );
  }

  function formatTanggalIndonesia(dateStr) {
    const months = [
      "Januari",
      "Februari",
      "Maret",
      "April",
      "Mei",
      "Juni",
      "Juli",
      "Agustus",
      "September",
      "Oktober",
      "November",
      "Desember",
    ];
    const date = new Date(dateStr);
    if (isNaN(date)) return dateStr;
    return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
  }
  function loadData(tableKey) {
    const config = tableConfigs[tableKey];
    Object.keys(config.filters).forEach((key) => (config.filters[key] = []));
    $.ajax({
      url: window.location.pathname,
      dataType: "json",
      headers: { "X-Requested-With": "XMLHttpRequest" },
      data: { process: "1" },
      success: function (response) {
        config.fullData = response[config.dataKey];
        $(config.tableId).show();

        if (config.dataTable) {
          config.dataTable.clear().rows.add(config.fullData).draw();
        } else {
          config.dataTable = $(config.tableId).DataTable({
            data: config.fullData,
            columns: Object.keys(config.filters).map((key) => {
              return {
                data: key,
                render: function (data, type, row) {
                  if (
                    key.toLowerCase().includes("tgl") ||
                    key.toLowerCase().includes("tanggal")
                  ) {
                    if (type === "display" || type === "filter")
                      return formatTanggalIndonesia(data);
                  }
                  if (
                    [
                      "Total_Tagihan",
                      "Total_Pelunasan",
                      "Sisa_Tagihan",
                    ].includes(key)
                  ) {
                    if (!data || parseFloat(data) === 0) return "";
                    return formatRupiah(data);
                  }
                  return data;
                },
              };
            }),
            scrollX: true,
            scrollCollapse: true,
            searching: false,
            responsive: true,
          });
        }
      },
    });
  }

  $(".processDataBtn").click(function () {
    const tableKey = $(this).data("table");
    currentTableKey = tableKey;
    loadData(tableKey);
  });

  $(document).on("click", ".filter-btn", function (e) {
    e.stopPropagation();
    e.stopImmediatePropagation();

    currentTableKey = $(this).data("table");
    currentColumn = $(this).data("column");
    const config = tableConfigs[currentTableKey];

    $("#modalTitle").text(`Filter ${currentColumn.replace("_", " ")}`);

    const filteredData = config.fullData.filter((row) => {
      return Object.keys(config.filters).every((col) => {
        if (col === currentColumn) return true;
        return (
          config.filters[col].length === 0 ||
          config.filters[col].includes(row[col])
        );
      });
    });

    const uniqueValues = [
      ...new Set(
        filteredData
          .map((row) => row[currentColumn])
          .filter((val) => {
            // Untuk nominal: jangan tampilkan 0, null, atau kosong
            if (
              ["Total_Tagihan", "Total_Pelunasan", "Sisa_Tagihan"].includes(
                currentColumn
              )
            ) {
              return val !== null && val !== "" && parseFloat(val) !== 0;
            }
            // Untuk kolom lain: hilangkan null/kosong
            return val !== null && val !== "";
          })
      ),
    ];
    const checkboxList = $("#checkboxList");
    checkboxList.empty();

    uniqueValues.forEach((val) => {
      const checked = config.filters[currentColumn].includes(val)
        ? "checked"
        : "";
      const displayText =
        currentColumn.toLowerCase().includes("tgl") ||
        currentColumn.toLowerCase().includes("tanggal")
          ? formatTanggalIndonesia(val)
          : ["Total_Tagihan", "Total_Pelunasan", "Sisa_Tagihan"].includes(
              currentColumn
            )
          ? formatRupiah(val)
          : val;

      checkboxList.append(`
        <div class="form-check mt-2">
          <label>
            <input type="checkbox" class="form-check-input" value="${val}" ${checked}> ${displayText}
          </label>
        </div>
      `);
    });

    $("#myModal").css("display", "flex");
    $("#searchFilter").val("");
    $("#selectAll").prop("checked", false);
  });
  $(".close-button").on("click", () => $("#myModal").hide());
  $(window).on("click", function (e) {
    if (e.target.id === "myModal") $("#myModal").hide();
  });

  $("#resetSelection").on("click", function () {
    $('#checkboxList input[type="checkbox"]').prop("checked", false);
    $("#selectAll").prop("checked", false);
  });

  $("#submitSelection").on("click", function () {
    const config = tableConfigs[currentTableKey];
    const selected = [];
    $('#checkboxList input[type="checkbox"]:checked').each(function () {
      selected.push($(this).val());
    });

    config.filters[currentColumn] = selected;

    const filteredData = config.fullData.filter((row) => {
      return Object.keys(config.filters).every((col) => {
        return (
          config.filters[col].length === 0 ||
          config.filters[col].includes(row[col])
        );
      });
    });

    config.dataTable.clear().rows.add(filteredData).draw();
    $("#myModal").hide();
  });

  $(document).on("change", "#selectAll", function () {
    const isChecked = $(this).is(":checked");
    $('#checkboxList input[type="checkbox"]').prop("checked", isChecked);
  });

  $(document).on("input", "#searchFilter", function () {
    const keyword = $(this).val().toLowerCase();
    $("#checkboxList div").each(function () {
      const text = $(this).text().toLowerCase();
      $(this).toggle(text.includes(keyword));
    });
  });
});
