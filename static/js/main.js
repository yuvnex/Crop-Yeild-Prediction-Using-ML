document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle Logic
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    // Check local storage for theme preference
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark') {
        body.classList.add('dark-mode');
        if(themeToggle) themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    if(themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            let theme = 'light';
            if (body.classList.contains('dark-mode')) {
                theme = 'dark';
                themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            } else {
                themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            }
            localStorage.setItem('theme', theme);
        });
    }

    // Export to Excel
    const exportExcelBtn = document.getElementById('exportExcelBtn');
    if (exportExcelBtn) {
        exportExcelBtn.addEventListener('click', () => {
            const table = document.getElementById('historyTable');
            if (table) {
                // Clone table to remove Action column before export
                const cloneTable = table.cloneNode(true);
                const ths = cloneTable.querySelectorAll('th');
                if(ths.length > 0) ths[ths.length - 1].remove(); // remove last th (Action)
                
                const trs = cloneTable.querySelectorAll('tbody tr');
                trs.forEach(tr => {
                    const tds = tr.querySelectorAll('td');
                    if(tds.length > 0) tds[tds.length - 1].remove(); // remove last td (Action form)
                });

                const wb = XLSX.utils.table_to_book(cloneTable, { sheet: "Predictions" });
                XLSX.writeFile(wb, "CropYield_Predictions.xlsx");
            }
        });
    }

    // Export to PDF
    const exportPdfBtn = document.getElementById('exportPdfBtn');
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener('click', () => {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            
            doc.setFontSize(18);
            doc.text("CropYield AI - Prediction History", 14, 22);
            
            doc.setFontSize(11);
            doc.setTextColor(100);
            doc.text(`Generated on: ${new Date().toLocaleDateString()}`, 14, 30);
            
            doc.autoTable({
                html: '#historyTable',
                startY: 35,
                theme: 'grid',
                columns: [
                    { header: 'Date' },
                    { header: 'Crop' },
                    { header: 'Soil Type' },
                    { header: 'Area' },
                    { header: 'Predicted Yield' },
                    { header: 'Category' },
                    { header: 'Confidence' }
                ],
                // Hide the Action column
                columnStyles: {
                    7: { cellWidth: 0, halign: 'center', fontSize: 0 } // Hide action column
                },
                didParseCell: function(data) {
                    if (data.column.index === 7) {
                        data.cell.styles.fontSize = 0;
                        data.cell.styles.cellWidth = 0;
                        data.cell.styles.minCellWidth = 0;
                        data.cell.styles.textColor = [255, 255, 255];
                    }
                },
                headStyles: { fillColor: [25, 135, 84] },
            });
            
            doc.save("CropYield_Predictions.pdf");
        });
    }
});
