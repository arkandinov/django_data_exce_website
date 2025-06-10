$(document).ready(function () {
  // =========================================================================
  // KONFIGURASI GLOBAL & VARIABEL
  // =========================================================================
  let currentTableKey = "";
  let currentColumn = "";
  let lastKnownStartForSort = null; // Variabel untuk menyimpan 'start' sebelum sort

  // =========================================================================
  // FUNGSI UTILITAS / FORMATTER
  // =========================================================================
  function formatRupiah(angka) {
    if (
      angka === null ||
      angka === undefined ||
      angka === "" ||
      parseFloat(angka) === 0
    )
      return "";
    try {
      return (
        "Rp. " +
        parseFloat(angka)
          .toFixed(0)
          .toString()
          .replace(/\B(?=(\d{3})+(?!\d))/g, ".")
      );
    } catch (e) {
      return String(angka);
    }
  }

  function formatTanggalIndonesia(dateStr) {
    if (!dateStr) return "";
    const datePart = String(dateStr).split(" ")[0];
    const parts = datePart.split("-");
    if (parts.length === 3) {
      const date = new Date(parts[0], parts[1] - 1, parts[2]);
      if (!isNaN(date.getTime())) {
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
        return `${date.getDate()} ${
          months[date.getMonth()]
        } ${date.getFullYear()}`;
      }
    }
    return dateStr;
  }

  function renderDate(data, type) {
    return type === "display" ? formatTanggalIndonesia(data) : data;
  }

  function renderCurrency(data, type) {
    return type === "display" ? formatRupiah(data) : data;
  }

  // =========================================================================
  // KONFIGURASI TABEL-TABEL
  // =========================================================================
  const tableConfigs = {
    SPM1: {
      tableId: "#table_SPM1",
      filters: {},
      dataLoaded: false,
      dataTable: null,
      latestOpsiDropdown: {},
      columnDefinitions: [
        { data: "No_Invoice", name: "No_Invoice", orderable: false },
        {
          data: "Nama_Klien",
          name: "Nama_Klien",
          className: "nama-klien-font",
          orderable: false,
        },
        {
          data: "tgl_Invoice",
          name: "tgl_Invoice",
          render: renderDate,
          orderable: false,
        },
        {
          data: "tgl_klien_Terima_Invoice",
          name: "tgl_klien_Terima_Invoice",
          render: renderDate,
          orderable: false,
        },
        {
          data: "Total_Tagihan",
          name: "Total_Tagihan",
          className: "text-right",
          render: renderCurrency,
          orderable: false,
        },
        {
          data: "tgl_Pelunasan",
          name: "tgl_Pelunasan",
          render: renderDate,
          orderable: false,
        },
        {
          data: "Total_Pelunasan",
          name: "Total_Pelunasan",
          className: "text-right",
          render: renderCurrency,
          orderable: false,
        },
        {
          data: "Sisa_Tagihan",
          name: "Sisa_Tagihan",
          className: "text-right",
          render: renderCurrency,
          orderable: false,
        },
        {
          data: "Tgl_Jatuh_Tempo",
          name: "Tgl_Jatuh_Tempo",
          render: renderDate,
          orderable: false,
        },
        {
          data: "tanggal_SPM1",
          name: "tanggal_SPM1",
          render: renderDate,
          orderable: false,
        },
      ],
    },
    SPM2: {
      tableId: "#table_SPM2",
      filters: {},
      dataLoaded: false,
      dataTable: null,
      latestOpsiDropdown: {},
      columnDefinitions: [
        // LENGKAPI DENGAN 'name' DAN 'orderable: false'
        { data: "No_Invoice", name: "No_Invoice", orderable: false },
        {
          data: "Nama_Klien",
          name: "Nama_Klien",
          className: "nama-klien-font",
          orderable: false,
        },
        {
          data: "tgl_Invoice",
          name: "tgl_Invoice",
          render: renderDate,
          orderable: false,
        },
        {
          data: "tgl_klien_Terima_Invoice",
          name: "tgl_klien_Terima_Invoice",
          render: renderDate,
          orderable: false,
        },
        {
          data: "Total_Tagihan",
          name: "Total_Tagihan",
          className: "text-right",
          render: renderCurrency,
          orderable: false,
        },
        {
          data: "tgl_Pelunasan",
          name: "tgl_Pelunasan",
          render: renderDate,
          orderable: false,
        },
        {
          data: "Total_Pelunasan",
          name: "Total_Pelunasan",
          className: "text-right",
          render: renderCurrency,
          orderable: false,
        },
        {
          data: "Sisa_Tagihan",
          name: "Sisa_Tagihan",
          className: "text-right",
          render: renderCurrency,
          orderable: false,
        },
        {
          data: "Tgl_Jatuh_Tempo",
          name: "Tgl_Jatuh_Tempo",
          render: renderDate,
          orderable: false,
        },
        {
          data: "tanggal_SPM1",
          name: "tanggal_SPM1",
          render: renderDate,
          orderable: false,
        },
        {
          data: "tanggal_SPM2",
          name: "tanggal_SPM2",
          render: renderDate,
          orderable: false,
        },
      ],
    },
    SOMASI: {
      tableId: "#table_SOMASI",
      filters: {},
      dataLoaded: false,
      dataTable: null,
      latestOpsiDropdown: {},
      columnDefinitions: [
        // LENGKAPI DENGAN 'name' DAN 'orderable: false'
        { data: "No_Invoice", name: "No_Invoice", orderable: false },
        {
          data: "Nama_Klien",
          name: "Nama_Klien",
          className: "nama-klien-font",
          orderable: false,
        },
        {
          data: "tgl_Invoice",
          name: "tgl_Invoice",
          render: renderDate,
          orderable: false,
        },
        {
          data: "tgl_klien_Terima_Invoice",
          name: "tgl_klien_Terima_Invoice",
          render: renderDate,
          orderable: false,
        },
        {
          data: "Total_Tagihan",
          name: "Total_Tagihan",
          className: "text-right",
          render: renderCurrency,
          orderable: false,
        },
        {
          data: "tgl_Pelunasan",
          name: "tgl_Pelunasan",
          render: renderDate,
          orderable: false,
        },
        {
          data: "Total_Pelunasan",
          name: "Total_Pelunasan",
          className: "text-right",
          render: renderCurrency,
          orderable: false,
        },
        {
          data: "Sisa_Tagihan",
          name: "Sisa_Tagihan",
          className: "text-right",
          render: renderCurrency,
          orderable: false,
        },
        {
          data: "Tgl_Jatuh_Tempo",
          name: "Tgl_Jatuh_Tempo",
          render: renderDate,
          orderable: false,
        },
        {
          data: "tanggal_SPM1",
          name: "tanggal_SPM1",
          render: renderDate,
          orderable: false,
        },
        {
          data: "tanggal_SPM2",
          name: "tanggal_SPM2",
          render: renderDate,
          orderable: false,
        },
        {
          data: "tanggal_SOMASI",
          name: "tanggal_SOMASI",
          render: renderDate,
          orderable: false,
        },
      ],
    },
  };

  // =========================================================================
  // FUNGSI UTAMA UNTUK MEMUAT & MENAMPILKAN TABEL
  // =========================================================================
  function switchAndLoadTable(tableKeyToLoad, forceReload = false) {
    const targetTableKey = tableKeyToLoad.toUpperCase();
    const config = tableConfigs[targetTableKey];
    if (!config) {
      return;
    }

    currentTableKey = targetTableKey;

    $(config.tableId).show().closest(".dataTables_wrapper").show();

    $(".nav-tab-btn")
      .removeClass("active btn-primary")
      .addClass("btn-outline-secondary");
    $(`.nav-tab-btn[data-table="${currentTableKey}"]`)
      .addClass("active btn-primary")
      .removeClass("btn-outline-secondary");

    if (!config.dataLoaded || forceReload) {
      if (config.dataTable && $.fn.DataTable.isDataTable(config.tableId)) {
        config.dataTable.ajax.reload(null, false);
      } else {
        if ($.fn.DataTable.isDataTable(config.tableId)) {
          $(config.tableId).DataTable().destroy();
          $(config.tableId).empty();
        }

        config.dataTable = $(config.tableId).DataTable({
          processing: true,
          serverSide: true,
          ajax: {
            url: window.location.pathname,
            type: "GET",
            data: function (d) {
              if (
                d.order &&
                d.order.length > 0 &&
                lastKnownStartForSort !== null
              ) {
                d.start = lastKnownStartForSort;
                lastKnownStartForSort = null; // Reset setelah digunakan
              }
              d.table_key = currentTableKey;
              if (config.filters) {
                Object.keys(config.filters).forEach((filterKey) => {
                  if (
                    config.filters[filterKey] &&
                    config.filters[filterKey].length > 0
                  ) {
                    d[filterKey] = config.filters[filterKey];
                  }
                });
              }
              return d;
            },
            dataSrc: function (json) {
              if (json.error) {
                config.dataLoaded = false;
                return [];
              }

              // ==========================================================
              // === LOKASI YANG BENAR UNTUK MENGATUR SEMUANYA ===
              config.dataLoaded = true; // <-- PINDAHKAN KE SINI
              config.latestOpsiDropdown = json.opsi_dropdown || {};

              // Simpan opsi original saat pertama kali dimuat (jika belum ada)
              if (!config.originalOpsiDropdown) {
                config.originalOpsiDropdown = json.opsi_dropdown || {};
              }
              // ==========================================================

              return json.data || [];
            },
          },
          columns: config.columnDefinitions,
          scrollX: true,
          scrollCollapse: true,
          responsive: true,
          pageLength: 10,
          lengthMenu: [
            [10, 25, 50, "All"],
            [10, 25, 50, "Semua"],
          ],
          searching: false,
          ordering: true, // Biarkan 'saklar utama' sort aktif agar .order() API berfungsi
        });
      }
    }
  }

  // =========================================================================
  // EVENT HANDLERS
  // =========================================================================
  $(".processDataBtn").click(function () {
    const tableKey = $(this).data("table").toUpperCase();
    const config = tableConfigs[tableKey];
    if (config) {
      config.filters = {}; // Reset data filter

      // Tambahkan baris ini untuk menghapus warna hijau dari SEMUA header di tabel ini
      const wrapper = $(config.tableId).closest(".dataTables_wrapper");
      wrapper.find(".dataTables_scrollHead th").removeClass("filter-active ");
      $("#selectAll").prop("checked", false);
      $("#searchFilter").val("").trigger("input");
    }
    switchAndLoadTable(tableKey, true);
  });

  $(".nav-tab-btn").click(function () {
    const tableKey = $(this).data("table").toUpperCase();
    switchAndLoadTable(tableKey, false);
  });

$(document).on("click", ".filter-btn", function (e) {
  e.stopPropagation();
  currentTableKey = $(this).data("table").toUpperCase();
  currentColumn = $(this).data("column");
  const config = tableConfigs[currentTableKey];

  // Prasyarat (tidak berubah, ini sudah benar)
  if (!config || !config.dataLoaded) {
    alert("Silakan muat data tabel terlebih dahulu.");
    return;
  }

  $("#modalTitle").text(`Filter ${currentColumn.replace(/_/g, " ")}`);
  const checkboxList = $("#checkboxList");
  checkboxList.empty();

  // ==========================================================
  // === LOGIKA FINAL (GABUNGAN SEMUA ATURAN) DIMULAI DI SINI ===
  // ==========================================================
  let opsiUntukKolomIni;

  // 1. Buat salinan dari semua filter yang aktif untuk dianalisis
  const otherFilters = { ...config.filters };

  // 2. Hapus filter dari kolom yang sedang dibuka SAAT INI.
  //    Ini adalah triknya: kita hanya peduli pada filter-filter LAIN.
  delete otherFilters[currentColumn];

  // 3. Cek apakah di dalam 'otherFilters' ada setidaknya satu filter yang aktif.
  const isAnyOtherFilterActive = Object.values(otherFilters).some(
    (filterValues) => filterValues && filterValues.length > 0
  );

  if (isAnyOtherFilterActive) {
    // KASUS 2: CASCADING
    // Jika ADA filter lain yang aktif, gunakan opsi terbaru dari server
    // yang sudah difilter secara cascading.
    console.log("Mode CASCADING. Menggunakan opsi terbaru (latestOpsiDropdown).");
    opsiUntukKolomIni =
      config.latestOpsiDropdown && config.latestOpsiDropdown[currentColumn]
        ? [...config.latestOpsiDropdown[currentColumn]]
        : [];
  } else {
    // KASUS 1: FILTER PERTAMA
    // Jika TIDAK ADA filter lain yang aktif, gunakan opsi original yang lengkap.
    console.log("Mode FILTER PERTAMA. Menggunakan opsi asli (originalOpsiDropdown).");
    opsiUntukKolomIni =
      config.originalOpsiDropdown && config.originalOpsiDropdown[currentColumn]
        ? [...config.originalOpsiDropdown[currentColumn]]
        : [];
  }
  // ==========================================================
  // === LOGIKA FINAL SELESAI ===
  // ==========================================================

  // Sisa kode untuk sorting dan rendering (tidak ada perubahan, sudah benar)
  if (opsiUntukKolomIni.length > 0) {
    if (["Total_Tagihan", "Total_Pelunasan", "Sisa_Tagihan"].includes(currentColumn)) {
      opsiUntukKolomIni.sort((a, b) => parseFloat(a) - parseFloat(b));
    } else {
      opsiUntukKolomIni.sort((a, b) =>
        String(a).localeCompare(String(b), undefined, { sensitivity: "base" })
      );
    }
  }

  if (opsiUntukKolomIni.length === 0) {
    checkboxList.html('<li><span class="text-muted">Tidak ada opsi filter yang tersedia.</span></li>');
  } else {
    opsiUntukKolomIni.forEach((val) => {
      const asliValue = String(val);
      let displayText = asliValue;
      if (currentColumn.toLowerCase().includes("tgl") || currentColumn.toLowerCase().includes("tanggal")) {
        displayText = formatTanggalIndonesia(asliValue);
      } else if (["Total_Tagihan", "Total_Pelunasan", "Sisa_Tagihan"].includes(currentColumn)) {
        displayText = formatRupiah(asliValue);
      }
      const isChecked = config.filters[currentColumn] && config.filters[currentColumn].includes(asliValue);
      checkboxList.append(
        `<div class="form-check mt-2"><label class="form-check-label w-100" style="cursor:pointer;"><input type="checkbox" class="form-check-input" value="${asliValue}" ${
          isChecked ? "checked" : ""
        }> ${displayText}</label></div>`
      );
    });
  }
  $("#myModal").css("display", "flex");
});

  // --- Event Handler untuk Tombol Sort Kustom di Modal ---
  $(document).on("click", ".tombol-sort-halaman-kustom", function () {
    const sortDirection = $(this).data("sort-direction");

    if (!currentTableKey || !currentColumn) {
      alert("Kesalahan: Tabel atau kolom belum dipilih.");
      return;
    }
    const config = tableConfigs[currentTableKey];
    const dtInstance = config ? config.dataTable : null;
    if (!dtInstance) {
      alert("Tabel belum dimuat.");
      return;
    }

    const columnIndex = config.columnDefinitions.findIndex(
      (col) => col.name === currentColumn
    );
    if (columnIndex === -1) {
      alert(
        "Kolom untuk diurutkan tidak ditemukan. Pastikan 'name' ada di columnDefinitions."
      );
      return;
    }

    // Simpan 'start' halaman saat ini SEBELUM memicu draw()
    const pageInfo = dtInstance.page.info();
    lastKnownStartForSort = pageInfo.start;

    // Panggil order() untuk mengatur urutan, dan draw(false) untuk memicu AJAX
    dtInstance.order([columnIndex, sortDirection]).draw(false);

    $("#myModal").hide();
  });

  $("#submitSelection").on("click", function () {
    if (!currentTableKey || !currentColumn) return;
    const config = tableConfigs[currentTableKey];
    if (!config || !config.dataTable) return;

    const selectedValues = [];
    $('#checkboxList input[type="checkbox"]:checked').each(function () {
      selectedValues.push($(this).val());
    });

    if (!config.filters) {
      config.filters = {};
    }
    config.filters[currentColumn] = selectedValues;

    config.dataTable.ajax.reload(null, false);

    // ... (setelah Anda mendapatkan selectedValues)
    const filterButton = $(
      `.filter-btn[data-table="${currentTableKey}"][data-column="${currentColumn}"]`
    );
    const headerCell = filterButton.closest("th"); // Temukan sel header <th> induk

    if (selectedValues.length > 0) {
      // Jika ada filter yang dipilih, tambahkan warna hijau
      headerCell.addClass("filter-active");
    } else {
      // Jika tidak ada filter yang dipilih, hapus warna hijau
      headerCell.removeClass("filter-active");
    }

    $("#myModal").hide();
  });

  $(".close-button").on("click", () => {
    $("#myModal").hide();
    $("#searchFilter").val("").trigger("input");
  });
  $(window).on("click", function (e) {
    if ($(e.target).is("#myModal")) {
      $("#searchFilter").val("").trigger("input");
      $("#myModal").hide();
    }
  });

  $("#resetSelection").on("click", function () {
    if (!currentTableKey || !currentColumn) return;
    const config = tableConfigs[currentTableKey];
    if (!config || !config.dataTable) return;

    if (config.filters) {
      config.filters[currentColumn] = [];
    }
    // Tambahkan baris ini untuk menghapus warna hijau dari header yang di-reset
    const headerCell = $(
      `.filter-btn[data-table="${currentTableKey}"][data-column="${currentColumn}"]`
    ).closest("th");
    headerCell.removeClass("filter-active");

    config.dataTable.draw();
    config.dataTable.ajax.reload(null, false);

    $('#checkboxList input[type="checkbox"]').prop("checked", false);
    $("#selectAll").prop("checked", false);
    $("#searchFilter").val("").trigger("input");
  });

  $("#searchFilter").on("input", function () {
    const keyword = $(this).val().toLowerCase();
    $("#checkboxList div.form-check").each(function () {
      const textInLabel = $(this).find("label").text().toLowerCase();
      $(this).toggle(textInLabel.includes(keyword));
    });
  });
  $("#selectAll").on("change", function () {
    const isChecked = $(this).is(":checked");
    // Hanya pengaruhi checkbox yang terlihat (setelah search di modal)
    $('#checkboxList div.form-check:visible input[type="checkbox"]').prop(
      "checked",
      isChecked
    );
  });
});
