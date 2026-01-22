// Add anchor to search form submission
document.getElementById('event-search-form')?.addEventListener('submit', function(e) {
  this.action = '/events#events-table';
});

// Show more/less functionality
const toggleBtn = document.querySelector('.js-toggle-show-events');
const truncatedBody = document.querySelector('tbody.js-events-truncated');
const allBody = document.querySelector('tbody.js-events-all');

if (toggleBtn) {
  toggleBtn.addEventListener('click', function() {
    const isHidden = truncatedBody.classList.contains('u-hide');
    if (isHidden) {
      truncatedBody.classList.remove('u-hide');
      allBody.classList.add('u-hide');
      toggleBtn.innerHTML = 'Show all events';
    } else {
      truncatedBody.classList.add('u-hide');
      allBody.classList.remove('u-hide');
      toggleBtn.innerHTML = 'Show less';
    }
  });
}

// Helper function to extract sort value from a cell
function getSortValue(cell, dataType) {
  let value;

  if (dataType === "link") {
    const link = cell?.querySelector('a');
    value = link ? link.textContent.toLowerCase().trim() : (cell ? cell.textContent.toLowerCase().trim() : '');
  } else if (dataType === "string" || dataType === "date") {
    value = cell ? cell.textContent.toLowerCase().trim() : '';
  }

  return value;
}

// Helper function to sort rows
function sortRows(rows, column, dataType, ascending) {
  return rows.sort((a, b) => {
    const aCells = a.querySelectorAll('td');
    const bCells = b.querySelectorAll('td');
    const aCell = aCells[column];
    const bCell = bCells[column];

    const aValue = getSortValue(aCell, dataType);
    const bValue = getSortValue(bCell, dataType);

    if (ascending) {
      return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
    } else {
      return aValue < bValue ? 1 : aValue > bValue ? -1 : 0;
    }
  });
}

// Table sorting functionality
const table = document.querySelector('.js-sortable-table');
if (table) {
  const sortBtns = table.querySelectorAll('.js-table-sort');
  let currentSort = { column: null, ascending: true };

  sortBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const th = this.parentElement;
      const column = parseInt(th.getAttribute('data-column'));
      const dataType = th.getAttribute('data-type') || 'string';

      // Toggle sort direction if clicking the same column
      if (currentSort.column === column) {
        currentSort.ascending = !currentSort.ascending;
      } else {
        currentSort.column = column;
        currentSort.ascending = true;
      }

      // Get table bodies
      const allBody = table.querySelector('tbody.js-events-all');
      const truncatedBody = table.querySelector('tbody.js-events-truncated');
      
      // If there are two table bodies, sort from the "all" tbody
      if (allBody && truncatedBody) {
        const allRows = sortRows(Array.from(allBody.querySelectorAll('tr')), column, dataType, currentSort.ascending);

        // Update "all" tbody
        allRows.forEach(row => allBody.appendChild(row));

        // Update truncated tbody with first 5 values
        const firstFive = allRows.slice(0, 5);
        truncatedBody.innerHTML = '';
        firstFive.forEach(row => truncatedBody.appendChild(row.cloneNode(true)));

      } else if (truncatedBody) {
        // Update truncated tbody only
        const rows = sortRows(Array.from(truncatedBody.querySelectorAll('tr')), column, dataType, currentSort.ascending);
        rows.forEach(row => truncatedBody.appendChild(row));
      }
    });
  });
}