// Add anchor to search form submission
document.getElementById('event-search-form').addEventListener('submit', function(e) {
  this.action = '/events#events-table';
});

// Table sorting functionality
const table = document.getElementById('browse-events-table');
if (table) {
  const sortBtns = table.querySelectorAll('.js-table-sort');
  let currentSort = { column: null, ascending: true };

  sortBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const th = this.parentElement;
      const column = parseInt(th.getAttribute('data-column'));
      const dataType = th.getAttribute('data-type') || 'string';
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));

      // Toggle sort direction if clicking the same column
      if (currentSort.column === column) {
        currentSort.ascending = !currentSort.ascending;
      } else {
        currentSort.column = column;
        currentSort.ascending = true;
      }

      // Sort rows
      rows.sort((a, b) => {
        let aValue, bValue;

        if (column === 0) {
          // Event name - get text from link
          aValue = a.querySelector('a').textContent.toLowerCase().trim();
          bValue = b.querySelector('a').textContent.toLowerCase().trim();
        } else {
          // Get value from TD at index
          const aTd = a.querySelectorAll('td')[column - 1];
          const bTd = b.querySelectorAll('td')[column - 1];
          aValue = aTd ? aTd.textContent.toLowerCase().trim() : '';
          bValue = bTd ? bTd.textContent.toLowerCase().trim() : '';
        }

        // Parse dates for date column
        if (dataType === 'date') {
          try {
            aValue = new Date(aValue).getTime() || 0;
            bValue = new Date(bValue).getTime() || 0;
          } catch (e) {
            aValue = 0;
            bValue = 0;
          }
        }

        // Compare values
        if (currentSort.ascending) {
          return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
        } else {
          return aValue < bValue ? 1 : aValue > bValue ? -1 : 0;
        }
      });

      // Re-append sorted rows
      rows.forEach(row => tbody.appendChild(row));
    });
  });
}